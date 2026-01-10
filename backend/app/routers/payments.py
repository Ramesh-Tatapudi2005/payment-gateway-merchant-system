from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import time
import os
import random

from .. import models, schemas, auth, database
from ..utils.id_generator import generate_custom_id
from ..utils.validation import validate_vpa, validate_luhn, detect_card_network, validate_expiry

router = APIRouter()

@router.get("", response_model=List[schemas.PaymentResponse])
def list_payments(
    db: Session = Depends(database.get_db),
    merchant: models.Merchant = Depends(auth.get_authenticated_merchant)
):
    return db.query(models.Payment).filter(
        models.Payment.merchant_id == merchant.id
    ).all()

@router.post("", response_model=schemas.PaymentResponse, status_code=201)
def create_payment(
    payment_in: schemas.PaymentCreate,
    db: Session = Depends(database.get_db),
    merchant: models.Merchant = Depends(auth.get_authenticated_merchant)
):
    # --- STEP 1: DELAY FIRST (Requirement: Simulate Bank Latency) ---
    # We move this to the top so even "Bad Requests" show the processing state
    test_mode = os.getenv("TEST_MODE", "false").lower() == "true"
    if test_mode:
        delay_ms = int(os.getenv("TEST_PROCESSING_DELAY", "1000"))
        time.sleep(delay_ms / 1000.0)
    else:
        time.sleep(random.uniform(5, 10))

    # --- STEP 2: ORDER VERIFICATION ---
    order = db.query(models.Order).filter(
        models.Order.id == payment_in.order_id,
        models.Order.merchant_id == merchant.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail={
            "error": {"code": "NOT_FOUND_ERROR", "description": "Order not found"}
        })

    # --- STEP 3: VALIDATION ---
    card_network = None
    card_last4 = None
    is_valid = True
    error_info = {"code": None, "desc": None}

    if payment_in.method == "upi":
        if not payment_in.vpa or not validate_vpa(payment_in.vpa):
            is_valid = False
            error_info = {"code": "BAD_REQUEST_ERROR", "desc": "Invalid VPA format"}
    
    elif payment_in.method == "card":
        if not payment_in.card:
            is_valid = False
            error_info = {"code": "BAD_REQUEST_ERROR", "desc": "Card details required"}
        elif not validate_luhn(payment_in.card.number):
            is_valid = False
            error_info = {"code": "INVALID_CARD", "desc": "Invalid card number"}
        elif not validate_expiry(payment_in.card.expiry_month, payment_in.card.expiry_year):
            is_valid = False
            error_info = {"code": "EXPIRED_CARD", "desc": "Card has expired"}
        
        if is_valid and payment_in.card:
            card_network = detect_card_network(payment_in.card.number)
            card_last4 = payment_in.card.number[-4:]

    # Stop here if the data format was fundamentally broken (400 error)
    if not is_valid and error_info["code"] == "BAD_REQUEST_ERROR":
        raise HTTPException(status_code=400, detail={"error": error_info})

    # --- STEP 4: DETERMINE SUCCESS ---
    if test_mode:
        is_success = os.getenv("TEST_PAYMENT_SUCCESS", "true").lower() == "true"
    else:
        success_chance = 0.90 if payment_in.method == "upi" else 0.95
        is_success = random.random() < success_chance

    # If format was okay but bank/Luhn failed, mark as "failed" status
    if not is_valid:
        is_success = False

    # --- STEP 5: RECORD TRANSACTION ---
    payment_id = generate_custom_id("pay_")
    status = "success" if is_success else "failed"
    
    new_payment = models.Payment(
        id=payment_id,
        order_id=order.id,
        merchant_id=merchant.id,
        amount=order.amount,
        currency=order.currency,
        method=payment_in.method,
        vpa=payment_in.vpa if payment_in.method == "upi" else None,
        card_network=card_network,
        card_last4=card_last4,
        status=status,
        error_code=None if is_success else (error_info["code"] or "PAYMENT_FAILED"),
        error_description=None if is_success else (error_info["desc"] or "Bank declined the transaction")
    )

    if is_success:
        order.status = "paid"

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    return new_payment

@router.get("/{payment_id}", response_model=schemas.PaymentResponse)
def get_payment(
    payment_id: str, 
    db: Session = Depends(database.get_db),
    merchant: models.Merchant = Depends(auth.get_authenticated_merchant)
):
    payment = db.query(models.Payment).filter(
        models.Payment.id == payment_id,
        models.Payment.merchant_id == merchant.id
    ).first()

    if not payment:
        raise HTTPException(status_code=404, detail={
            "error": {"code": "NOT_FOUND_ERROR", "description": "Payment not found"}
        })
    return payment
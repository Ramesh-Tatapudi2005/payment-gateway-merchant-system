from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import time
import os
import random

from .. import auth

from .. import models, schemas, database
from ..utils.id_generator import generate_custom_id
from ..utils.validation import validate_vpa, validate_luhn, detect_card_network, validate_expiry

router = APIRouter()


def execute_payment_processing(payment_in: schemas.PaymentCreate, db: Session, order: models.Order):

    payment_id = generate_custom_id("pay_")
    
    card_network = None
    card_last4 = None
    if payment_in.method == "card" and payment_in.card:
        card_network = detect_card_network(payment_in.card.number)
        card_last4 = payment_in.card.number[-4:]

    new_payment = models.Payment(
        id=payment_id,
        order_id=order.id,
        merchant_id=order.merchant_id,
        amount=order.amount,
        currency=order.currency,
        method=payment_in.method,
        vpa=payment_in.vpa if payment_in.method == "upi" else None,
        card_network=card_network,
        card_last4=card_last4,
        status="processing"  # Starts in processing state as required
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    # --- STEP 2: SIMULATE BANK LATENCY ---
    # Now everyone waits, even if the card is wrong!
    test_mode = os.getenv("TEST_MODE", "false").lower() == "true"
    delay_ms = int(os.getenv("TEST_PROCESSING_DELAY", "1000")) if test_mode else random.uniform(5000, 10000)
    time.sleep(delay_ms / 1000.0)

    # --- STEP 3: PERFORM VALIDATION & DETERMINE OUTCOME ---
    error_info = None

    # Check for validation errors first
    if payment_in.method == "upi":
        if not payment_in.vpa or not validate_vpa(payment_in.vpa):
            error_info = {"code": "INVALID_VPA", "desc": "VPA format invalid"}
    
    elif payment_in.method == "card":
        if not payment_in.card:
            error_info = {"code": "BAD_REQUEST_ERROR", "desc": "Card details required"}
        elif not validate_luhn(payment_in.card.number):
            error_info = {"code": "INVALID_CARD", "desc": "Card validation failed"}
        elif not validate_expiry(payment_in.card.expiry_month, payment_in.card.expiry_year):
            error_info = {"info": "EXPIRED_CARD", "desc": "Card expiry date invalid"}

    # --- STEP 4: UPDATE FINAL STATUS ---
    if error_info:
        # It's a validation failure (after the delay)
        new_payment.status = "failed"
        new_payment.error_code = error_info["code"]
        new_payment.error_description = error_info["desc"]
    else:
        # Valid data, check for success vs bank decline
        is_success = os.getenv("TEST_PAYMENT_SUCCESS", "true").lower() == "true" if test_mode else (random.random() < 0.95)
        
        if is_success:
            new_payment.status = "success"
            order.status = "paid"
        else:
            new_payment.status = "failed"
            new_payment.error_code = "PAYMENT_FAILED"
            new_payment.error_description = "Bank declined the transaction"

    db.commit()
    db.refresh(new_payment)

    # If it was a validation error, we still raise the Exception for the API response
    if error_info:
        raise HTTPException(status_code=400, detail={"error": error_info})

    return new_payment

# --- 1. PUBLIC ENDPOINT (Checkout Page) ---
# FIX: No 'auth' dependency here so Postman/Frontend can call it without a secret key.
@router.post("/public", response_model=schemas.PaymentResponse, status_code=201)
def create_public_payment(payment_in: schemas.PaymentCreate, db: Session = Depends(database.get_db)):
    order = db.query(models.Order).filter(models.Order.id == payment_in.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail={"error": {"code": "NOT_FOUND_ERROR", "description": "Order not found"}})
    return execute_payment_processing(payment_in, db, order)


# --- 2. PRIVATE ENDPOINT (Merchant Backend) ---
@router.post("", response_model=schemas.PaymentResponse, status_code=201)
def create_private_payment(
    payment_in: schemas.PaymentCreate, 
    db: Session = Depends(database.get_db),
    merchant: models.Merchant = Depends(auth.get_authenticated_merchant)
):
    order = db.query(models.Order).filter(
        models.Order.id == payment_in.order_id, 
        models.Order.merchant_id == merchant.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail={"error": {"code": "NOT_FOUND_ERROR"}})
    
    return execute_payment_processing(payment_in, db, order)


# --- 3. DASHBOARD ENDPOINTS ---
@router.get("", response_model=List[schemas.PaymentResponse])
def list_payments(db: Session = Depends(database.get_db), merchant: models.Merchant = Depends(auth.get_authenticated_merchant)):
    return db.query(models.Payment).filter(models.Payment.merchant_id == merchant.id).all()

# Added /public suffix to allow the checkout page to check status without a key
@router.get("/{payment_id}/public", response_model=schemas.PaymentResponse)
def get_public_payment_status(payment_id: str, db: Session = Depends(database.get_db)):
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail={"error": {"code": "NOT_FOUND_ERROR"}})
    return payment
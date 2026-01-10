from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class OrderCreate(BaseModel):
    amount: int = Field(..., ge=100) # Minimum 100 paise (₹1.00)
    currency: str = "INR"
    receipt: Optional[str] = None
    notes: Optional[Dict[str, Any]] = None

class OrderResponse(BaseModel):
    id: str
    merchant_id: UUID
    amount: int
    currency: str
    receipt: Optional[str]
    notes: Optional[Dict[str, Any]]
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PaymentCreateCard(BaseModel):
    number: str
    expiry_month: int
    expiry_year: int
    cvv: str
    holder_name: str

class PaymentCreate(BaseModel):
    order_id: str
    method: str  # "upi" or "card"
    vpa: Optional[str] = None
    # Updated: Use the PaymentCreateCard class to group card fields
    card: Optional[PaymentCreateCard] = None 

class PaymentResponse(BaseModel):
    id: str
    order_id: str
    merchant_id: Any
    amount: int
    currency: str
    method: str
    status: str
    vpa: Optional[str] = None
    card_network: Optional[str] = None
    card_last4: Optional[str] = None
    created_at: datetime
    # Added: Required to convert SQLAlchemy models to Pydantic responses
    model_config = ConfigDict(from_attributes=True)
import uuid
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from .database import Base

class Merchant(Base):
    __tablename__ = "merchants"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    api_key = Column(String(64), unique=True, nullable=False)
    api_secret = Column(String(64), nullable=False)
    webhook_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"
    id = Column(String(64), primary_key=True) # Format: order_ + 16 chars
    merchant_id = Column(UUID(as_uuid=True), ForeignKey("merchants.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    currency = Column(String(3), default='INR')
    receipt = Column(String(255), nullable=True)
    notes = Column(JSON, nullable=True)
    status = Column(String(20), default='created')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Payment(Base):
    __tablename__ = "payments"
    id = Column(String(64), primary_key=True) # Format: pay_ + 16 chars
    order_id = Column(String(64), ForeignKey("orders.id"), nullable=False)
    merchant_id = Column(UUID(as_uuid=True), ForeignKey("merchants.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    currency = Column(String(3), default='INR')
    method = Column(String(20), nullable=False)
    status = Column(String(20), default='processing')
    vpa = Column(String(255), nullable=True)
    card_network = Column(String(20), nullable=True)
    card_last4 = Column(String(4), nullable=True)
    error_code = Column(String(50), nullable=True)
    error_description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
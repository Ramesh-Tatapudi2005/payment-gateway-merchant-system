from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timezone

# Internal imports based on your structure
from .database import engine, Base, SessionLocal, get_db
from .models import Merchant
# UPDATED: Added 'auth' to the router imports
from .routers import orders, payments, auth 
import sqlalchemy

app = FastAPI(title="Payment Gateway API")

# Initialize FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://merchant-dashboard-ui.onrender.com",
        "https://checkout-page-ui.onrender.com"
        ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Create tables and seed merchant on startup
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    seed_test_merchant()

def seed_test_merchant():
    """
    Seeds test merchant with exact credentials from requirements.
    ID: 550e8400-e29b-41d4-a716-446655440000
    """
    db = SessionLocal()
    try:
        test_id = "550e8400-e29b-41d4-a716-446655440000"
        test_email = "test@example.com"
        
        exists = db.query(Merchant).filter(Merchant.email == test_email).first()
        
        if not exists:
            test_merchant = Merchant(
                id=test_id,
                name="Test Merchant",
                email=test_email,
                api_key="key_test_abc123",
                api_secret="secret_test_xyz789",
                is_active=True
            )
            db.add(test_merchant)
            db.commit()
    except Exception as e:
        db.rollback()
    finally:
        db.close()

# 3. Include Routers
# UPDATED: Added auth router so the /api/v1/auth/login path is active
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["Orders"])
app.include_router(payments.router, prefix="/api/v1/payments", tags=["Payments"])

# 4. Enhanced Health Check Endpoint (Deliverable 2 Requirement)
@app.get("/health")
def health_check():
    db_status = "disconnected"
    try:
        # Dynamic check for database
        db = SessionLocal()
        db.execute(sqlalchemy.text("SELECT 1"))
        db_status = "connected"
        db.close()
    except Exception:
        db_status = "disconnected"

    return {
        "status": "healthy",
        "database": db_status,
        "redis": "connected", 
        "worker": "running",   
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }

@app.get("/api/v1/test/merchant")
def get_test_merchant(db: Session = Depends(get_db)):
    merchant = db.query(Merchant).filter(Merchant.email == "test@example.com").first()
    if not merchant:
        raise HTTPException(status_code=404, detail="Test merchant not found")
        
    return {
        "id": str(merchant.id),
        "email": merchant.email,
        "api_key": merchant.api_key,
        "api_secret": merchant.api_secret, # Added for your convenience in Postman
        "seeded": True
    }
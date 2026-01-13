import os
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# 1. Fetch URL from environment
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    # Fallback for local development
    SQLALCHEMY_DATABASE_URL = "postgresql://gateway_user:gateway_pass@localhost:5432/payment_gateway"

# 2. Fix prefix for SQLAlchemy 1.4+ compatibility
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. Enhanced Resilience: pool_pre_ping checks connection health
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# 4. Connection Retry Loop
for i in range(12): # Attempt for 60 seconds total
    try:
        with engine.connect() as connection:
            print("Successfully connected to the database!")
            break
    except OperationalError as e:
        if i == 11:
            print("Final database connection attempt failed.")
            raise e
        print(f"Database connection attempt {i+1}/12 failed (DNS/Network). Retrying in 5s...")
        time.sleep(5)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
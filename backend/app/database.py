import os
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# 1. Get the URL from environment or use the local default
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://gateway_user:gateway_pass@postgres:5432/payment_gateway"
)

# 2. Fix prefix for SQLAlchemy compatibility (postgres:// to postgresql://)
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. Connection Resilience: Retry connection up to 5 times
# This fixes the "could not translate host name" error during cold starts
engine = create_engine(SQLALCHEMY_DATABASE_URL)

for attempt in range(5):
    try:
        # Try to connect to verify the host is reachable
        connection = engine.connect()
        connection.close()
        break
    except OperationalError as e:
        if attempt == 4: # Final attempt failed
            raise e
        print(f"Database DNS not ready, retrying in 5s... ({attempt + 1}/5)")
        time.sleep(5)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
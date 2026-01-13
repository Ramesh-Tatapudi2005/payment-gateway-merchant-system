import os
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# 1. Fetch the URL from environment
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://gateway_user:gateway_pass@postgres:5432/payment_gateway"
)

# 2. Fix the prefix for SQLAlchemy compatibility
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. Connection Resilience Loop
# This explicitly waits for the Render internal DNS to propagate
engine = create_engine(SQLALCHEMY_DATABASE_URL)

for i in range(10): # Try up to 10 times
    try:
        # Test the connection
        with engine.connect() as connection:
            print("Successfully connected to the database!")
            break
    except OperationalError:
        print(f"Database DNS not ready, retrying in 5 seconds... ({i+1}/10)")
        time.sleep(5)
else:
    # Final failure if all retries fail
    raise Exception("Could not connect to database after several attempts.")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
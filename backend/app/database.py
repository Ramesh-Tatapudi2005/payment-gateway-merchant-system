import os
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# 1. Fetch the URL from environment
# If no env var is found, it falls back to a local postgres container
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://gateway_user:gateway_pass@localhost:5432/payment_gateway"
)

# 2. Fix prefix for SQLAlchemy compatibility (postgres:// -> postgresql://)
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. Connection Resilience Loop
# We create the engine once and then test the connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

for i in range(10): 
    try:
        # We use a simple connection test
        with engine.connect() as connection:
            print("Successfully connected to the database!")
            break
    except OperationalError as e:
        if i == 9: # Last attempt
            print("Final attempt failed. Error details:", e)
            raise e
        print(f"Database connection attempt {i+1}/10 failed. Retrying in 5s...")
        time.sleep(5)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
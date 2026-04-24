from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Toggle this to turn DB on or off
USE_DB = os.getenv("USE_DB", "false").lower() == "true"

DATABASE_URL = os.getenv("DATABASE_URL")  # e.g. postgresql://user:password@localhost:5432/analyticsengine

if USE_DB:
    if not DATABASE_URL:
        raise ValueError("USE_DB is enabled but DATABASE_URL environment variable is not set.")
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    engine = None
    SessionLocal = None

Base = declarative_base()

def get_db():
    if not USE_DB or SessionLocal is None:
        yield None
        return
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
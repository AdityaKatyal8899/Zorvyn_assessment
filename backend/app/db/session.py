# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

# Keep it generic (SQLite for local dev if needed, or PostgreSQL placeholder)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create engine (sqlite workaround for parallel access is not needed here)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

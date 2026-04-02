# app/core/security.py
from passlib.context import CryptContext
from typing import Optional
from datetime import datetime, timedelta

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT Placeholder (as requested, only a structure, no full implementation)
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    # This is a mock function, it returns a fake token for now
    return "mock_access_token_placeholder"

def decode_access_token(token: str) -> dict:
    # This is a mock function, it returns mock data
    return {"sub": "admin@example.com", "role": "admin"}

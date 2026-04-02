from passlib.context import CryptContext
from typing import Optional
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    return "mock_access_token_placeholder"

def decode_access_token(token: str) -> dict:
    return {"sub": "admin@example.com", "role": "admin"}

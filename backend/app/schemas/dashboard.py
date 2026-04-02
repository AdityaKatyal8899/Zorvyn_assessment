# app/schemas/dashboard.py
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import date
from app.models.record import RecordType

class SummaryResponse(BaseModel):
    """High-level financial overview."""
    total_income: float
    total_expense: float
    net_balance: float

class CategoryResponse(BaseModel):
    """Category-wise breakdown of financial data."""
    # Using a simple dictionary response as requested
    __root__: Dict[str, float]

class RecentRecordResponse(BaseModel):
    """Minimal record fields for dashboard view."""
    amount: float
    type: RecordType
    category: str
    date: date

    class Config:
        orm_mode = True
        from_attributes = True

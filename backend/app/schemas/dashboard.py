from pydantic import BaseModel, RootModel
from typing import Dict, List, Optional
from datetime import date
from app.models.record import RecordType

class SummaryResponse(BaseModel):
    """High-level financial overview."""
    total_income: float
    total_expense: float
    net_balance: float


class CategoryResponse(RootModel):
    """Category-wise breakdown of financial data."""
    root: Dict[str, float]

    
class RecentRecordResponse(BaseModel):
    """Minimal record fields for dashboard view."""
    amount: float
    type: RecordType
    category: str
    date: date
    class Config:
        orm_mode = True
        from_attributes = True

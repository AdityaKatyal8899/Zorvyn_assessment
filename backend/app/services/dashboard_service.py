from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict
from app.models.record import Record, RecordType
from app.schemas.dashboard import SummaryResponse

def get_summary(db: Session) -> SummaryResponse:
    """Provide a high-level financial overview through database-side aggregation."""
    total_income = db.query(func.sum(Record.amount)).filter(Record.type == RecordType.income).scalar() or 0.0
    total_expense = db.query(func.sum(Record.amount)).filter(Record.type == RecordType.expense).scalar() or 0.0
    
    net_balance = float(total_income) - float(total_expense)
    return SummaryResponse(
        total_income=float(total_income),
        total_expense=float(total_expense),
        net_balance=net_balance
    )


def get_category_breakdown(db: Session) -> Dict[str, float]:
    """Provide a category-wise breakdown of financial data through database-side aggregation."""
    results = db.query(Record.category, func.sum(Record.amount)).group_by(Record.category).all()
    return {category: float(amount) for category, amount in results}


def get_recent_records(db: Session, limit: int = 5) -> List[Record]:
    """Provide the most recent financial activity, ordered by creation date."""
    return db.query(Record).order_by(Record.created_at.desc()).limit(limit).all()

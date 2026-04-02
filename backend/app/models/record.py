import enum
from sqlalchemy import Column, Integer, Numeric,String, Float, ForeignKey, Enum, Date, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class RecordType(str, enum.Enum):
    income = "income"
    expense = "expense"


class Record(Base):
    __tablename__ = "records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    type = Column(Enum(RecordType), nullable=False)
    category = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="records")

__table_args__ = (
    CheckConstraint('amount >= 0', name='check_amount_positive'),
)

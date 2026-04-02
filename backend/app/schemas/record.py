from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from app.models.record import RecordType

class RecordBase(BaseModel):
    amount: float
    type: RecordType
    category: str
    date: date
    notes: Optional[str] = None


class RecordCreate(RecordBase):
    pass


class RecordUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[RecordType] = None
    category: Optional[str] = None
    date: Optional[datetime] = None
    notes: Optional[str] = None

    
class RecordResponse(RecordBase):
    id: int
    user_id: int
    created_at: datetime
    class Config:
        orm_mode = True
        from_attributes = True
        json_encoders = {
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat()
        }

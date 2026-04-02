# app/services/record_service.py
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.record import Record
from app.schemas.record import RecordCreate, RecordUpdate
from app.models.user import User

def create_record(db: Session, record: RecordCreate, current_user: User) -> Record:
    """Create a new record with user_id from the authenticated user."""
    db_record = Record(
        user_id=current_user.id,
        amount=record.amount,
        type=record.type,
        category=record.category,
        date=record.date,
        notes=record.notes
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_records(db: Session, skip: int = 0, limit: int = 100) -> List[Record]:
    """Fetch multiple records with offset and limit."""
    return db.query(Record).offset(skip).limit(limit).all()

def get_record_by_id(db: Session, record_id: int) -> Optional[Record]:
    """Fetch a single record by its ID."""
    return db.query(Record).filter(Record.id == record_id).first()

def update_record(db: Session, record_id: int, record_update: RecordUpdate) -> Optional[Record]:
    """Update only provided fields of an existing record."""
    db_record = get_record_by_id(db, record_id)
    if not db_record:
        return None
    
    update_data = record_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_record, key, value)
    
    db.commit()
    db.refresh(db_record)
    return db_record

def delete_record(db: Session, record_id: int) -> bool:
    """Delete a record by its ID and return success status."""
    db_record = get_record_by_id(db, record_id)
    if not db_record:
        return False
    
    db.delete(db_record)
    db.commit()
    return True

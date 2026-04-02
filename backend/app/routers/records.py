from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.record import RecordCreate, RecordUpdate, RecordResponse
from app.services import record_service
from app.core.rbac import admin_only, admin_analyst
from app.models.user import User


router = APIRouter(prefix="/records", tags=["records"])


@router.post("/", response_model=RecordResponse, status_code=status.HTTP_201_CREATED)
def create_record(
    record: RecordCreate, 
    db: Session = Depends(get_db),
    current_user: User = admin_only
):
    """
    Create a new financial record.
    # RBAC: Admin only
    """
    return record_service.create_record(db=db, record=record, current_user=current_user)


@router.get("/", response_model=List[RecordResponse])
def list_records(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = admin_analyst
):
    """
    Fetch a paginated list of all records.
    # RBAC: Admin + Analyst (read-only access)
    """
    return record_service.get_records(db=db, skip=skip, limit=limit)


@router.get("/{record_id}", response_model=RecordResponse)
def get_record(
    record_id: int, 
    db: Session = Depends(get_db),
    current_user: User = admin_analyst
):
    """
    Fetch a single record by ID.
    # RBAC: Admin + Analyst (read-only access)
    """
    db_record = record_service.get_record_by_id(db=db, record_id=record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    return db_record


@router.patch("/{record_id}", response_model=RecordResponse)
def update_record(
    record_id: int, 
    record_update: RecordUpdate, 
    db: Session = Depends(get_db),
    current_user: User = admin_only
):
    """
    Update an existing record.
    # RBAC: Admin only
    """
    db_record = record_service.update_record(db=db, record_id=record_id, record_update=record_update)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    return db_record


@router.delete("/{record_id}")
def delete_record(
    record_id: int, 
    db: Session = Depends(get_db),
    current_user: User = admin_only
):
    """
    Delete a record by ID.
    # RBAC: Admin only
    """
    success = record_service.delete_record(db=db, record_id=record_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    return {"message": "Record deleted successfully"}

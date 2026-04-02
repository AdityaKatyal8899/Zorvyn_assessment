# app/routers/dashboard.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from app.db.session import get_db
from app.schemas.dashboard import SummaryResponse, RecentRecordResponse
from app.services import dashboard_service
from app.core.rbac import require_role
from app.models.user import UserRole

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/summary", response_model=SummaryResponse)
def get_summary(db: Session = Depends(get_db), current_user: dict = require_role([UserRole.admin, UserRole.analyst, UserRole.viewer])):
    """
    Provide high-level financial overview.
    # RBAC: Accessible by admin, analyst, viewer (shared endpoint)
    """
    return dashboard_service.get_summary(db=db)

@router.get("/categories", response_model=Dict[str, float])
def get_category_breakdown(db: Session = Depends(get_db), current_user: dict = require_role([UserRole.admin, UserRole.analyst])):
    """
    Provide category-wise breakdown of financial data.
    # RBAC: Accessible by admin and analyst only (restricted endpoint)
    """
    return dashboard_service.get_category_breakdown(db=db)

@router.get("/recent", response_model=List[RecentRecordResponse])
def get_recent_activity(db: Session = Depends(get_db), current_user: dict = require_role([UserRole.admin, UserRole.analyst])):
    """
    Provide recent financial activity.
    # RBAC: Accessible by admin and analyst only (restricted endpoint)
    """
    return dashboard_service.get_recent_records(db=db, limit=5)

# app/routers/dashboard.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Dict
from app.db.session import get_db
from app.schemas.dashboard import SummaryResponse, RecentRecordResponse
from app.services import dashboard_service
from app.core.rbac import admin_analyst, all_roles
from app.models.user import User

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/summary", response_model=SummaryResponse)
def get_summary(
    db: Session = Depends(get_db), 
    current_user: User = all_roles
):
    """
    Provide high-level financial overview.
    # RBAC: All roles (summary view)
    """
    return dashboard_service.get_summary(db=db)

@router.get("/categories", response_model=Dict[str, float])
def get_category_breakdown(
    db: Session = Depends(get_db), 
    current_user: User = admin_analyst
):
    """
    Provide category-wise breakdown of financial data.
    # RBAC: Admin + Analyst (read-only access)
    """
    return dashboard_service.get_category_breakdown(db=db)

@router.get("/recent", response_model=List[RecentRecordResponse])
def get_recent_activity(
    db: Session = Depends(get_db), 
    current_user: User = admin_analyst
):
    """
    Provide recent financial activity.
    # RBAC: Admin + Analyst (read-only access)
    """
    return dashboard_service.get_recent_records(db=db, limit=5)

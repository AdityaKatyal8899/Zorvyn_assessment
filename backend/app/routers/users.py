from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services import user_service
from app.core.rbac import admin_only
from app.models.user import User


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate, 
    db: Session = Depends(get_db),
    current_user: User = admin_only
):
    """
    Create a new user.
    # RBAC: Admin only
    """
    return user_service.create_user(db=db, user=user)


@router.get("/", response_model=List[UserResponse])
def list_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = admin_only
):
    """
    Fetch a list of all users.
    # RBAC: Admin only
    """
    return user_service.get_users(db=db, skip=skip, limit=limit)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int, 
    user_update: UserUpdate, 
    db: Session = Depends(get_db),
    current_user: User = admin_only
):
    """
    Update user status or role.
    # RBAC: Admin only
    """
    db_user = user_service.update_user(db=db, user_id=user_id, user_update=user_update)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

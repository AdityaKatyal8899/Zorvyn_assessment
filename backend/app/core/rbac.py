# app/core/rbac.py
from fastapi import HTTPException, Depends, status
from app.models.user import User, UserRole, UserStatus
from typing import List
# Mock function as requested - for now, just returns a mock user with "admin" role
# In a real app, this would decode a JWT and fetch the user from the database

class CurrenUser:
    def __init__(self, id: int, role: UserRole, status: UserStatus):
        self.id = id
        self.role = role
        self.status = status

def get_current_user() -> User:
    # Creating a mock admin user for demonstration
    mock_user = User(
        id=1,
        role=UserRole.admin,
        status=UserStatus.active
    )
    return mock_user

class RoleChecker:
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )
        return user

def require_role(allowed_roles: list):
    return Depends(RoleChecker(allowed_roles))

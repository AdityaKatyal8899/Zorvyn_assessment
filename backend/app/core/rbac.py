from fastapi import HTTPException, Depends, status, Request
from app.models.user import User, UserRole, UserStatus
from typing import List
class CurrentUser:
    def __init__(self, id: int, role: UserRole, status: UserStatus):
        self.id = id
        self.role = role
        self.status = status
def get_current_user(request: Request):
    role_header = request.headers.get("x-mock-role", "admin")
    try:
        role = UserRole(role_header)
    except ValueError:
        role = UserRole.admin
    return CurrentUser(
        id=1,
        role=role,
        status=UserStatus.active
    )
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
admin_only = require_role([UserRole.admin])
admin_analyst = require_role([UserRole.admin, UserRole.analyst])
all_roles = require_role([UserRole.admin, UserRole.analyst, UserRole.viewer])

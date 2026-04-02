import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class UserRole(str, enum.Enum):
    admin = "admin"
    analyst = "analyst"
    viewer = "viewer"

class UserStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole, name="user_role"), default=UserRole.viewer, nullable=False)

    status = Column(Enum(UserStatus, name="user_status"), default=UserStatus.active, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    records = relationship("Record", back_populates="user", cascade="all, delete-orphan")

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.enums import UserRole


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.MEMBER


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    active: Optional[bool] = None


class UserResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    organization_id: int
    name: str
    email: EmailStr
    role: UserRole
    active: bool
    must_change_password: bool
    created_at: datetime
    updated_at: datetime
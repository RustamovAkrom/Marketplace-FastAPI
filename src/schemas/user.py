from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from db.models.users import UserRole


class UserBaseScheme(BaseModel):
    username: str = Field(
        ..., min_length=3, max_length=50, description="The user's username"
    )
    full_name: Optional[str] = None
    email: EmailStr = Field(..., description="The user's email address")
    phone: str

    model_config = ConfigDict(from_attributes=True)


class UserCreateScheme(UserBaseScheme):
    pass


class UserUpdateScheme(BaseModel):
    full_name: Optional[str | None] = None
    username: Optional[str | None] = None
    email: str
    phone: str


class UserOutScheme(UserBaseScheme):
    id: int
    role: UserRole
    is_active: bool
    is_superuser: bool
    is_email_verified: bool
    is_phone_verified: bool


__all__ = (
    "UserBaseScheme",
    "UserCreateScheme",
    "UserUpdateScheme",
)

from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBaseScheme(BaseModel):
    id: int
    username: str = Field(
        ..., min_length=3, max_length=50, description="The user's username"
    )
    email: EmailStr = Field(..., description="The user's email address")

    model_config = ConfigDict(from_attributes=True)


class UserCreateScheme(UserBaseScheme):
    full_name: Optional[str] = None


class UserUpdateScheme(BaseModel):
    full_name: Optional[str | None] = None
    username: Optional[str | None] = None


__all__ = (
    "UserBaseScheme",
    "UserCreateScheme",
    "UserUpdateScheme",
)

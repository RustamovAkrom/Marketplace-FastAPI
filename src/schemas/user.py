from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from db.models.users import UserRole


class UserBaseScheme(BaseModel):
    username: str = Field(
        ..., min_length=3, max_length=50, description="The user's username"
    )
    email: EmailStr = Field(..., description="The user's email address")


class TokenResponse(BaseModel):
    access_token: str = Field(
        ..., description="Token used for accessing protected resources"
    )
    refresh_token: str = Field(
        ..., description="Token used to refresh the access token"
    )
    token_type: str = "bearer"


class UserCreate(UserBaseScheme):
    password: str = Field(..., min_length=8, description="The user's password")


class UserOut(UserBaseScheme):
    id: int = Field(..., description="The unique identifier of the user")
    is_active: bool = Field(..., description="Indicates if the user is active")
    role: UserRole = Field(..., description="The role assigned to the user")

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user: UserOut = Field(..., description="The user details")
    tokens: TokenResponse = Field(..., description="Authentication tokens for the user")


class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="The user's email address")
    password: str = Field(..., description="The user's password")


class UserUpdate(UserBaseScheme):
    password: Optional[str] = Field(
        None, min_length=8, description="The user's new password"
    )
    is_active: Optional[bool] = Field(
        None, description="Indicates if the user is active"
    )

    class Config:
        from_attributes = True


class UserInDB(UserBaseScheme):
    id: int = Field(..., description="The unique identifier of the user")
    hashed_password: str = Field(..., description="The hashed password of the user")
    is_active: bool = Field(..., description="Indicates if the user is active")

    class Config:
        from_attributes = True


__all__ = (
    "UserResponse",
    "TokenResponse",
    "UserBaseScheme",
    "UserCreate",
    "UserOut",
    "UserLogin",
    "UserUpdate",
    "UserInDB",
)

from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from db.models.users import UserRole


class RegistrationScheme(BaseModel):
    full_name: Optional[str] = None
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    phone: str = Field(..., min_length=13, max_length=20)
    password: str = Field(..., min_length=8)


class RegisterOutScheme(BaseModel):
    id: int
    full_name: Optional[str] = None
    username: str
    email: EmailStr
    phone: str
    is_active: bool
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class LoginScheme(BaseModel):
    username: str
    password: str


class TokenResponseScheme(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenScheme(BaseModel):
    token: str


class RefreshTokenScheme(BaseModel):
    refresh_token: str


class LoginOutScheme(BaseModel):
    user: RegisterOutScheme
    tokens: TokenResponseScheme


class LogoutScheme(BaseModel):
    refresh_token: str


class LogoutResponseScheme(BaseModel):
    detail: str = "Successfully logged out"


class ForgotPasswordScheme(BaseModel):
    email: EmailStr


class PasswordResetScheme(BaseModel):
    token: str
    new_password: str

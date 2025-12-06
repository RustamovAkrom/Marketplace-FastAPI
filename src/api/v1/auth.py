from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.dependencies.sessions import get_db_session
from schemas.auth import (
    ForgotPasswordScheme,
    LoginOutScheme,
    LoginScheme,
    PasswordResetScheme,
    RefreshTokenScheme,
    RegisterOutScheme,
    RegistrationScheme,
    TokenScheme,
)
from schemas.user import UserCreateScheme
from services.auth_service import AuthService
from services.password_service import PasswordService, get_password_service

router = APIRouter()


async def get_auth_service(
    session: AsyncSession = Depends(get_db_session),
) -> AuthService:
    return AuthService(session)


@router.post("/register", response_model=UserCreateScheme)
async def register_user(
    data: RegistrationScheme,
    auth_service: AuthService = Depends(get_auth_service),
) -> RegisterOutScheme:
    """
    User registration endpoint
    """
    return await auth_service.register(data)


@router.post("/login", response_model=LoginOutScheme)
async def login_user(
    data: LoginScheme,
    auth_service: AuthService = Depends(get_auth_service),
) -> LoginOutScheme:
    """
    User login endpoint
    """
    return await auth_service.login(data)


@router.post("/logout")
async def logout_user(
    data: RefreshTokenScheme, auth_service: AuthService = Depends(get_auth_service)
):
    """
    Logout and invalidate refresh token
    """
    return await auth_service.logout(data)


@router.post("/forgot-password")
async def forgot_password(
    data: ForgotPasswordScheme,
    password_service: PasswordService = Depends(get_password_service),
) -> dict[str, str]:
    return await password_service.forgot_password(data)


@router.post("/reset-password")
async def reset_password(
    data: PasswordResetScheme,
    password_service: PasswordService = Depends(get_password_service),
):
    """
    Reset password endpoint
    """
    return await password_service.reset_password(data)


@router.post("/refresh-token")
async def refresh_token(
    data: RefreshTokenScheme = Body(...),
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Refresh access token using refresh token
    """
    return await auth_service.refresh_access_token(data.refresh_token)


@router.post("/verify")
async def verify(
    type_: str = Body(..., embed=True),  # "email" or "phone"
    data: TokenScheme = Body(...),
    auth_service: AuthService = Depends(get_auth_service),
) -> dict:
    if type_ == "email":
        return await auth_service.verify_email(data.token)
    elif type_ == "phone":
        return await auth_service.verify_phone(data.token)
    else:
        raise HTTPException(status_code=400, detail="Invalid verification type")


@router.post("/resend-verification")
async def resend_verification(
    user_id: int = Body(...),
    type_: str = Body(...),
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Resend email or phone verification token
    """
    return await auth_service.resend_verification(user_id, type_)


__all__ = ("router",)

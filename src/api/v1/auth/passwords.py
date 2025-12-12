from fastapi import APIRouter, Body, Depends

from schemas.auth import (
    ForgotPasswordScheme,
    PasswordResetScheme,
    RefreshTokenScheme,
)
from services.auth_service import AuthService, get_auth_service
from services.password_service import PasswordService, get_password_service

router = APIRouter()


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

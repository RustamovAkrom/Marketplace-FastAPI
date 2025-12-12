from fastapi import APIRouter, Depends

from schemas.auth import (
    LoginOutScheme,
    LoginScheme,
    RefreshTokenScheme,
    RegisterOutScheme,
    RegistrationScheme,
)
from services.auth_service import AuthService, get_auth_service

router = APIRouter()


@router.post("/register", response_model=RegisterOutScheme)
async def register_user(
    data: RegistrationScheme,
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    User registration endpoint
    """
    return await auth_service.register(data)


@router.post("/login", response_model=LoginOutScheme)
async def login_user(
    data: LoginScheme,
    auth_service: AuthService = Depends(get_auth_service),
):
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

from fastapi import APIRouter, Depends

from schemas.auth import (
    LoginOutScheme,
    LoginScheme,
    RegisterOutScheme,
    RegistrationScheme,
)
from schemas.user import UserCreateScheme
from services.user_service import UserService

router = APIRouter()


@router.post("/register", response_model=UserCreateScheme)
async def register_user(
    data: RegistrationScheme,
    user_service: UserService = Depends(),
) -> RegisterOutScheme:
    return await user_service.register(data)


@router.post("/login", response_model=LoginOutScheme)
async def login_user(
    data: LoginScheme,
    user_service: UserService = Depends(),
) -> LoginOutScheme:
    return await user_service.login(data)


__all__ = ("router",)

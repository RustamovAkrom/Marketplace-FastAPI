from fastapi import APIRouter, Depends

from schemas.user import UserCreate, UserLogin, UserOut, UserResponse
from services.user_service import UserService

router = APIRouter()


@router.post("/register", response_model=UserOut)
async def register_user(
    data: UserCreate,
    user_service: UserService = Depends(),
) -> UserOut:
    return await user_service.register(data)


@router.post("/login", response_model=UserResponse)
async def login_user(
    data: UserLogin,
    user_service: UserService = Depends(),
) -> UserResponse:
    return await user_service.login(data)


__all__ = ("router",)

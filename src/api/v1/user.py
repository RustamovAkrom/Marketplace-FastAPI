from fastapi import APIRouter, Depends

from db.dependencies.auth import get_current_user, require_roles
from db.models.users import User, UserRole
from schemas.auth import (
    LoginOutScheme,
    LoginScheme,
    RegisterOutScheme,
    RegistrationScheme,
)
from schemas.user import UserCreateScheme
from services.user_service import UserService

router = APIRouter()


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "role": current_user.role,
    }


@router.get("/dashboard")
async def dashboard(current_user: User = Depends(get_current_user)):
    return {"message": f"Welcome, {current_user.username}"}


@router.get("/admin/stats")
async def admin_stats(admin_user: User = Depends(require_roles(UserRole.admin.value))):
    return {"status": "ok", "admin": admin_user.username}


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

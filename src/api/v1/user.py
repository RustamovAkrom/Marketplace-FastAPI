from fastapi import APIRouter, Body, Depends

from db.dependencies.auth import get_current_user, require_roles
from db.models.users import User, UserRole
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
from services.password_service import PasswordService
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


@router.post("/logout")
async def logout_user(data: RefreshTokenScheme, user_service: UserService = Depends()):
    """
    Logout and invalidate refresh token
    """
    return await user_service.logout(data.refresh_token)


@router.post("/forgot-password")
async def forgot_password(
    data: ForgotPasswordScheme, password_service: PasswordService = Depends()
) -> dict[str, str]:
    return await password_service.forgot_password(data)


@router.post("/reset-password")
async def reset_password(
    data: PasswordResetScheme, password_service: PasswordService = Depends()
):
    return await password_service.reset_password(data)


@router.post("/refresh-token")
async def refresh_token(
    data: RefreshTokenScheme = Body(...), user_service: UserService = Depends()
):
    """
    Refresh access token using refresh token
    """
    return await user_service.refresh_access_token(data.refresh_token)


@router.post("/verify-email")
async def verify_email(
    data: TokenScheme = Body(...), user_service: UserService = Depends()
):
    """
    Verify user email via token
    """
    return await user_service.verify_email(data.token)


@router.post("/verify-phone")
async def verify_phone(
    data: TokenScheme = Body(...), user_service: UserService = Depends()
):
    """
    Verify user phone via token
    """
    return await user_service.verify_phone(data.token)


@router.post("/resend-verification")
async def resend_verification(
    user_id: int = Body(...),
    type_: str = Body(...),
    user_service: UserService = Depends(),
):
    """
    Resend email or phone verification token
    """
    return await user_service.resend_verification(user_id, type_)


__all__ = ("router",)

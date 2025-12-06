# src/dependencies/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import decode_token
from db.crud.token import TokenCRUD
from db.crud.user import UserCRUD
from db.dependencies.sessions import get_db_session
from db.models.users import User, UserRole

http_bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(get_db_session),
) -> User:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    token = credentials.credentials

    try:
        payload = decode_token(token)
    except ValueError as exc:
        reason = str(exc)
        if reason == "token_expired":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is not access token"
        )

    jti = payload.get("jti")
    token_crud = TokenCRUD(session)
    if await token_crud.exists(jti):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked"
        )

    user_crud = UserCRUD(session)
    user = await user_crud.get_by_id(int(payload.get("sub")))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return user


def require_roles(*allowed_roles: str):
    """
    Example:
      - require_roles("admin")
      - require_roles("admin", "manager")
    """

    async def role_checker(user: User = Depends(get_current_user)):
        user_role = getattr(user, "role", None)

        if user_role is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User has no role assigned",
            )

        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {allowed_roles}",
            )

        return user

    return role_checker


# READY-TO-USE SHORTCUTS
require_admin = require_roles(UserRole.admin.value)
require_seller = require_roles(UserRole.seller.value)
require_buyer = require_roles(UserRole.buyer.value)
require_courier = require_roles(UserRole.courier.value)

from datetime import datetime

from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import APIException
from core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from db.crud.token import TokenCRUD
from db.crud.user import UserCRUD
from db.dependencies.sessions import get_db_session
from schemas.auth import (
    LoginOutScheme,
    LoginScheme,
    LogoutResponseScheme,
    LogoutScheme,
    RegisterOutScheme,
    RegistrationScheme,
    TokenResponseScheme,
)


class UserService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_db_session),
    ):
        self.session = session
        self.user_crud = UserCRUD(self.session)
        self.token_crud = TokenCRUD(self.session)

    async def register(self, data: RegistrationScheme) -> RegisterOutScheme:

        if await self.user_crud.get_by_email(data.email):
            raise APIException(
                "Email already registered", status_code=status.HTTP_400_BAD_REQUEST
            )

        if await self.user_crud.get_by_username(data.username):
            raise APIException(
                "Username already taken", status_code=status.HTTP_409_CONFLICT
            )

        hashed_password = hash_password(data.password)
        user = await self.user_crud.create(data, hashed_password)

        return RegisterOutScheme.model_validate(user)

    async def login(self, data: LoginScheme) -> LoginOutScheme:
        user = await self.user_crud.get_by_email(
            data.username
        ) or await self.user_crud.get_by_username(data.username)

        if not user:
            raise APIException(
                "Invalid credentials, username not found!",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        if not verify_password(data.password, user.hashed_password):
            raise APIException(
                "Invalid credentials, password didn't match!",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        # create tokens using subject (user id) to avoid nested 'sub' fields
        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)

        tokens = TokenResponseScheme(
            access_token=access_token, refresh_token=refresh_token
        )

        return LoginOutScheme(
            user=RegisterOutScheme.model_validate(user), tokens=tokens
        )

    async def logout(self, data: LogoutScheme) -> LogoutResponseScheme:
        try:
            payload = decode_token(data.refresh_token)
        except ValueError:
            return LogoutResponseScheme(detail="Token invalid or expired")

        if payload.get("type") != "refresh":
            raise APIException(
                "Provided toke is not a refresh token",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        jti = payload.get("jti")
        if not jti:
            return LogoutResponseScheme(detail="Invalid refresh token")

        if await self.token_crud.exists(jti):
            return LogoutResponseScheme(detail="Already logged out")

        exp_ts = payload.get("exp")
        expires_at = datetime.utcfromtimestamp(exp_ts) if exp_ts else datetime.utcnow()

        user_id = int(payload.get("sub")) if payload.get("sub") else None

        await self.token_crud.add(
            jti=jti, token_type="refresh", expires_at=expires_at, user_id=user_id
        )

        return LogoutResponseScheme(detail="Successfully logged out")


__all__ = ("UserService",)

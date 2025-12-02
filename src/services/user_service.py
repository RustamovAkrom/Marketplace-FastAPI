from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import APIException
from core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from db.crud.user import UserCRUD
from db.dependencies import get_db_session
from schemas.auth import (
    LoginOutScheme,
    LoginScheme,
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

    async def register(self, data: RegistrationScheme) -> RegisterOutScheme:

        if await self.user_crud.get_by_email(data.email):
            raise APIException(
                "Email already registered",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if await self.user_crud.get_by_username(data.username):
            raise APIException(
                "Username already taken",
                status_code=status.HTTP_409_CONFLICT,
            )

        hashed_password = hash_password(data.password)

        user = await self.user_crud.create(data, hashed_password)

        return RegisterOutScheme.model_validate(user)

    async def login(self, data: LoginScheme) -> LoginOutScheme:
        user = await self.user_crud.get_by_email(data.username)

        if not user:
            user = await self.user_crud.get_by_username(data.username)

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

        tokens = TokenResponseScheme(
            access_token=create_access_token({"sub": str(user.id)}),
            refresh_token=create_refresh_token({"sub": str(user.id)}),
        )

        return LoginOutScheme(
            user=RegisterOutScheme.model_validate(user), tokens=tokens
        )


__all__ = ("UserService",)

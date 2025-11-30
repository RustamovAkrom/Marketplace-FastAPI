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
from schemas.user import TokenResponse, UserCreate, UserLogin, UserOut, UserResponse


class UserService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_db_session),
    ):

        self.session = session
        self.user_crud = UserCRUD(self.session)

    async def register(self, data: UserCreate) -> UserOut:
        if await self.user_crud.get_by_email(data.email):
            raise APIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        if await self.user_crud.get_by_username(data.username):
            raise APIException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
            )

        hashed_password = hash_password(data.password)
        user = await self.user_crud.create(data, hashed_password)

        return UserOut.model_validate(user)

    async def login(self, data: UserLogin) -> UserResponse:
        user = await self.user_crud.get_by_email(data.email)
        if not user:
            raise APIException(
                status_code=401,
                detail="Invalid credentials",
                code="invalid_credentials",
            )

        if not verify_password(data.password, user.hashed_password):
            raise APIException(
                status_code=401,
                detail="Invalid credentials",
                code="invalid_credentials",
            )

        access = create_access_token({"sub": str(user.id)})
        refresh = create_refresh_token({"sub": str(user.id)})

        tokens = TokenResponse(access_token=access, refresh_token=refresh)
        user_out = UserOut.model_validate(user)

        return UserResponse(user=user_out.model_dump(), tokens=tokens)

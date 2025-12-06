from typing import Sequence

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import hash_password
from db.dependencies.sessions import get_db_session
from db.models.users import User
from schemas.auth import RegistrationScheme


class UserCRUD:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def all(self) -> Sequence[User]:
        result = await self.session.execute(select(User))
        return result.scalars().all()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get_by_username(self, username: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        return result.scalars().first()

    async def get_by_phone(self, phone: str) -> User | None:
        result = await self.session.execute(select(User).where(User.phone == phone))
        return result.scalars().first()

    async def create(self, data: RegistrationScheme, hashed_password: str) -> User:
        user_data = data.dict()
        user_data.pop("password", None)
        user = User(
            **user_data,
            hashed_password=hashed_password,
        )
        try:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user

        except IntegrityError:
            raise HTTPException(status_code=400, detail="Category already exists")

    async def delete(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.commit()

    async def update(self, user: User, **kwargs) -> User:
        for key, value in kwargs.items():
            setattr(user, key, value)
        try:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Category already exists")

    async def get_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def update_password(self, user: User, new_password) -> User:
        user.hashed_password = hash_password(new_password)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def mark_email_verified(self, user: User) -> User:
        user.is_email_verified = True
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def mark_phone_verified(self, user: User) -> User:
        user.is_phone_verified = True
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

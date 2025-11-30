from functools import cache

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.config import settings


@cache
def get_async_db_engine() -> AsyncEngine:
    return create_async_engine(
        settings.DATABASE_URL,
        echo=settings.ENV == "dev",
        future=True,
    )


@cache
def get_async_session_maker() -> async_sessionmaker[AsyncSession]:
    engine = get_async_db_engine()
    return async_sessionmaker(
        engine,
        expire_on_commit=False,
    )

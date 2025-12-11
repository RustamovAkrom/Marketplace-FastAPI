from functools import cache

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.settings import settings


@cache
def get_async_db_engine() -> AsyncEngine:
    url = settings.DATABASE_URL
    if not url:
        raise RuntimeError("DATABASE_URL is not configured")
    return create_async_engine(
        url,
        echo=(settings.ENV == "dev"),
        future=True,
    )


@cache
def get_async_session_maker() -> async_sessionmaker[AsyncSession]:
    engine = get_async_db_engine()
    return async_sessionmaker(
        engine,
        expire_on_commit=False,
    )

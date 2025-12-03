from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from core.database import get_async_session_maker


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """Dependency that provides a database session."""
    async_session_maker = get_async_session_maker()
    session = async_session_maker()

    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()

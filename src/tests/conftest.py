# tests/conftest.py

from collections.abc import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.app import create_app
from src.core.config import get_app_settings
from src.db.dependencies.sessions import get_db_session
from src.db.meta import meta
from src.db.models import load_all_models


# -------------------------
# DATABASE ENGINE FIXTURE
# -------------------------
@pytest.fixture(scope="session")
async def _engine() -> AsyncGenerator[AsyncEngine, None]:
    """Создаёт тестовый движок и создаёт таблицы в памяти."""
    settings = get_app_settings()

    load_all_models()  # <-- обязательно, иначе модели не загрузятся

    engine = create_async_engine(str(settings.DATABASE_URL))

    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)

    try:
        yield engine
    finally:
        await engine.dispose()


# -------------------------
# DATABASE SESSION FIXTURE
# -------------------------
@pytest.fixture
async def dbsession(_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """
    Создаёт сессию в SAVEPOINT, чтобы каждый тест был изолирован.
    """
    connection = await _engine.connect()
    transaction = await connection.begin()

    session_maker = async_sessionmaker(connection, expire_on_commit=False)
    session = session_maker()

    try:
        yield session
    finally:
        await session.close()
        await transaction.rollback()
        await connection.close()


# -------------------------
# FASTAPI APP FIXTURE
# -------------------------
@pytest.fixture
async def fastapi_app(dbsession: AsyncSession) -> FastAPI:
    """Создаёт FastAPI приложение с заменённым get_db_session."""

    app = create_app()
    app.dependency_overrides[get_db_session] = lambda: dbsession

    return app


# -------------------------
# ANYIO BACKEND
# -------------------------
@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """Указывает pytest-anyio какой backend использовать."""
    return "asyncio"


# -------------------------
# CLIENT FIXTURE
# -------------------------
@pytest.fixture
async def client(
    fastapi_app: FastAPI, anyio_backend: str
) -> AsyncGenerator[AsyncClient, None]:
    """
    HTTP клиент, используемый в тестах.
    """
    transport = ASGITransport(app=fastapi_app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.database import get_async_db_engine
from core.requests import get_http_transport


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_engine = get_async_db_engine()
    app.state.http_transport = get_http_transport()
    yield
    await app.state.db_engine.dispose()
    await app.state.http_transport.aclose()

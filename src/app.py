from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from api.routers import api_router
from core.config import settings
from core.exceptions import register_error_handler
from core.lifespan import lifespan
from core.logger import configure_logger


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        lifespan=lifespan,
        docs_url="/docs" if settings.ENV != "prod" else None,
        redoc_url="/redoc" if settings.ENV != "prod" else None,
        openapi_url="/openapi.json" if settings.ENV != "prod" else None,
        default_response_class=ORJSONResponse,
    )

    # Configure logger
    configure_logger()

    # Register exception handlers
    register_error_handler(app)

    # Include API router
    app.include_router(api_router, prefix="/api/v1")

    # Set up CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

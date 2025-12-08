from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles

from api.routers import api_router
from core.config import MEDIA_ROOT, MEDIA_URL, settings
from core.exceptions import register_error_handler
from core.lifespan import lifespan
from core.logger import configure_logger
from core.monitoring import router as monitoring_router
from core.prometheus import MetricsMiddleware
from core.sentry import init_sentry
from middlewares.request_id_middleware import RequestIDMiddleware


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    # Configure logger
    configure_logger()

    # Initialize Sentry (if configured)
    init_sentry()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        lifespan=lifespan,
        docs_url="/docs" if settings.ENV != "prod" else None,
        redoc_url="/redoc" if settings.ENV != "prod" else None,
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
        openapi_url="/openapi.json" if settings.ENV != "prod" else None,
        default_response_class=ORJSONResponse,
    )
    # Request ID middleware (must be first)
    app.add_middleware(RequestIDMiddleware)

    # Only add metrics middleware in environments where Prometheus scraping is expected
    if settings.PROMETHEUS_ENABLED:
        app.add_middleware(MetricsMiddleware)

    # Set up CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(api_router, prefix="/api/v1")
    app.include_router(router=monitoring_router)  # /monitoring/*

    # Register error handlers
    register_error_handler(app)

    # Include API router

    # Static files (media)
    try:
        app.mount(MEDIA_URL, StaticFiles(directory=MEDIA_ROOT), name="media")
    except Exception:
        # don't crash if media doesn't exists at startup
        pass

    return app

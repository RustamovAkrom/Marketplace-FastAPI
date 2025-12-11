from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class BaseAppConfig(BaseSettings):
    MEDIA_ROOT: Path = BASE_DIR / "media"
    MEDIA_URL: str = "/media/"

    ENV: str = "dev"  # dev, prod, test
    DEBUG: bool = True

    APP_NAME: str = "Marketplace API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "An e-commerce marketplace API built with FastAPI."
    API_V1_PREFIX: str = "/api/v1"
    SERVER_HOST: str = "0.0.0.0"  # nosec B104
    SERVER_PORT: int = 8000  # nosec B104
    RELOAD: bool = True
    LOG_LEVEL: str = "INFO"

    CORS_ORIGINS: list[str] = ["*"]

    SENTRY_DSN: str | None = None

    PROMETHEUS_ENABLED: bool = True
    PROMETHEUS_PATH: str = "/metrics"
    PROMETHEUS_METRICS_KEY: str = "secret"

    model_config = SettingsConfigDict(
        validate_assignment=True,
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
    )

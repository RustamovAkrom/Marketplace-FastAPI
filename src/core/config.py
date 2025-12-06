from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class BaseAppSettings(BaseSettings):
    # ENVIRONMENT
    ENV: str = "dev"  # dev, prod, test
    DEBUG: bool = True

    # APPLICATION
    APP_NAME: str = "Marketplace API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "An e-commerce marketplace API built with FastAPI."
    API_V1_PREFIX: str = "/api/v1"
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    RELOAD: bool = True
    LOG_LEVEL: str = "INFO"

    # CORS
    CORS_ORIGINS: list[str] = ["*"]

    # JWT
    SECRET_KEY: str = "SECRET_KEY"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    JWT_REFRESH_TOKEN_EXPIRES_DAYS: int = 7
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 15

    # DATABASE (dynamic)
    DB_ENGINE: str = "sqlite"  # sqlite | postgres
    DB_NAME: str = "database"
    DB_HOST: str | None = None
    DB_PORT: str | None = None
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None

    @property
    def DATABASE_URL(self) -> str:
        if self.ENV == "dev":
            return f"sqlite+aiosqlite:///{BASE_DIR / self.DB_NAME}.db"
        return (
            "postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}@"
            "{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # REDIS / RABBITMQ
    BROKER: str = "redis"  # redis | rabbitmq

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    RABBITMQ_USER: str | None = None
    RABBITMQ_PASSWORD: str | None = None
    RABBITMQ_HOST: str | None = None
    RABBITMQ_PORT: int | None = None
    RABBITMQ_VHOST: str = "/"

    @property
    def CELERY_BROKER_URL(self):
        if self.BROKER == "redis":
            return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

        return (
            "amqp://"
            f"{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}"
            f"@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/{self.RABBITMQ_VHOST}"
        )

    @property
    def CELERY_RESULT_BACKEND(self):
        return self.CELERY_BROKER_URL

    # EMAIL SETTINGS
    EMAIL_FROM: str = "admin@example.com"
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "test@example.com"
    SMTP_PASSWORD: str = "testpassword"
    SMTP_TLS: bool = True

    # Social Auth
    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None
    GOOGLE_REDIRECT_URI: str = (
        "http://localhost:8000/api/v1/social_auth/google/callback"
    )

    @property
    def OAUTH_PROVIDERS(self):
        return {
            "google": {
                "client_id": self.GOOGLE_CLIENT_ID,
                "client_secret": self.GOOGLE_CLIENT_SECRET,
                "authorize_url": "https://accounts.google.com/o/oauth2/v2/auth",
                "token_url": "https://oauth2.googleapis.com/token",
                "userinfo_url": "https://openidconnect.googleapis.com/v1/userinfo",
                "redirect_uri": self.GOOGLE_REDIRECT_URI,
            }
        }

    # Pydantic config
    model_config = SettingsConfigDict(
        validate_assignment=True,
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache()
def get_app_settings() -> BaseAppSettings:
    return BaseAppSettings()


settings = get_app_settings()

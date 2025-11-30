from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class BaseAppSettings(BaseSettings):
    ENV: str = "dev"  # dev, prod, test

    APP_NAME: str = "Marketplace API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "An e-commerce marketplace API built with FastAPI."

    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    DEBUG: bool = True
    RELOAD: bool = True

    SECRET_KEY: str = "SECRET_KEY"
    LOG_LEVEL: str = "INFO"

    CORS_ORIGINS: list[str] = ["*"]

    API_V1_PREFIX: str = "/api/v1"

    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    JWT_REFRESH_TOKEN_EXPIRES_DAYS: int = 7

    # DATABASE_URL: str
    DB_ENGINE: str = "sqlite"
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

from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class DatabaseConfig(BaseSettings):
    DB_ENGINE: str = "sqlite"
    DB_NAME: str = "database"
    DB_HOST: str | None = None
    DB_PORT: str | None = None
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None

    ENV: str = "dev"

    @property
    def DATABASE_URL(self):
        if self.ENV == "dev" or self.DB_ENGINE == "sqlite":
            db_path = BASE_DIR / f"{self.DB_NAME}.db"
            return f"sqlite+aiosqlite:///{db_path}"

        return (
            "postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

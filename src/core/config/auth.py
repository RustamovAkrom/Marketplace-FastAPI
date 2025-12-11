from pydantic_settings import BaseSettings


class AuthConfig(BaseSettings):
    SECRET_KEY: str = "SECRET_KEY"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    JWT_REFRESH_TOKEN_EXPIRES_DAYS: int = 7
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 15

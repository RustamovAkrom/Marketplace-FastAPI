from pydantic_settings import BaseSettings


class EmailConfig(BaseSettings):
    EMAIL_FROM: str = "admin@example.com"
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "test@example.com"
    SMTP_PASSWORD: str = "testpassword"
    SMTP_TLS: bool = True

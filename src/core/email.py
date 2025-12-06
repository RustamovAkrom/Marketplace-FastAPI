# core/email.py
from fastapi_mail import ConnectionConfig, FastMail

from core.config import settings

# Валидация, чтобы не было None
if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
    raise ValueError("SMTP_USER and SMTP_PASSWORD must be set in environment")

conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.EMAIL_FROM,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_STARTTLS=settings.SMTP_TLS,
    MAIL_SSL_TLS=not settings.SMTP_TLS,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    # TEMPLATE_FOLDER="templates/email",  # если используешь шаблоны
)

fast_mail = FastMail(conf)

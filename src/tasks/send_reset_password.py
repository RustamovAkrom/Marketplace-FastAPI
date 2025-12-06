from celery import shared_task
from fastapi_mail import MessageSchema, MessageType, NameEmail

from core.email import fast_mail


@shared_task
async def send_reset_password_task(email: str, token: str) -> None:
    message = MessageSchema(
        subject="Reset your password",
        recipients=[NameEmail(name="", email=email)],
        body=f"Reset link: https://your-app/reset?token={token}",
        subtype=MessageType.html,
    )
    await fast_mail.send_message(message)

from celery import shared_task
from fastapi_mail import MessageSchema, MessageType, NameEmail

from core.email import fast_mail


@shared_task
async def send_email_verification_task(email: str, token: str) -> str:
    message = MessageSchema(
        subject="Email Verification",
        recipients=[NameEmail(name="", email=email)],
        body=f"Confirm your email: https://your-app.com/verify-email?token={token}",
        subtype=MessageType.html,
    )
    await fast_mail.send_message(message)

    return f"Verification email sent to {email}"


@shared_task
async def send_phone_verification_task(phone: str, code: str) -> str:
    # TODO: Create send sms to phone: Twilio, Nexmo, Eskiz, etc.
    print(f"Sending SMS to {phone}: code={code}")
    return f"SMS sent to {phone}"

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

async def send_registration_email(email_to: str, token: str):
    """Sends a confirmation email with a unique verification link."""
    verification_url = f"{settings.DOMAIN}/auth/verify/{token}"
    
    message = MessageSchema(
        subject="Confirm your Blog Account",
        recipients=[email_to],
        body=f"Click here to verify your account: {verification_url}",
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)


async def send_password_reset_email(email_to: str, token: str):
    """Sends a password reset email with a unique verification link."""
    verification_url = f"{settings.DOMAIN}/auth/password-reset/{token}"
    
    message = MessageSchema(
        subject="Confirm password reset for your Blog Account",
        recipients=[email_to],
        body=f"Click here to confirm your choice: {verification_url}",
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)


async def send_forgot_password_email(email_to: str, token: str):
    """Sends a password reset email with a unique verification link."""
    verification_url = f"{settings.DOMAIN}/auth/forgot-password/{token}"
    
    message = MessageSchema(
        subject="Confirm password reset for your Blog Account",
        recipients=[email_to],
        body=f"Click here to confirm your choice: {verification_url}",
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)

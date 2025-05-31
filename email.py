from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
import os

conf = ConnectionConfig(
    MAIL_USERNAME="viktoriia0333@meta.ua",
    MAIL_PASSWORD="secretPassword",
    MAIL_FROM=EmailStr("viktoriia0333@meta.ua"),
    MAIL_PORT=465,
    MAIL_SERVER="smtp.meta.ua",
    MAIL_FROM_NAME="Desired Name",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)


async def send_verification_email(email: EmailStr, token: str):
    verify_link = f"http://localhost:8000/api/auth/verify?token={token}"
    message = MessageSchema(
        subject="Verify your email",
        recipients=[email],
        body=f"<h4>Click to verify your email:</h4><a href='{verify_link}'>{verify_link}</a>",
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)

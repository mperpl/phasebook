from fastapi import BackgroundTasks
from pydantic import EmailStr
from sqlalchemy import select
from services.email.service import send_forgot_password_email
from services.redis_token.TokenPrefix import TokenPrefix
from services.redis_token.generate_redis_token import generate_redis_token
from sqlalchemy.ext.asyncio import AsyncSession
from models import User


async def forgot_password_email(email: EmailStr, background_tasks: BackgroundTasks, db: AsyncSession):
    stmt = select(User).where(User.email == email)
    user = (await db.execute(stmt)).scalar_one_or_none()
    if user:
        token = await generate_redis_token(user.id, TokenPrefix.FORGOT_PASSWORD, 300)
        background_tasks.add_task(send_forgot_password_email, email, token)

    return {'message': 'If user exists, password reset email has been sent'}
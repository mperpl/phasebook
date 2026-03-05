from fastapi import HTTPException
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.exc import SQLAlchemyError
from core.security import get_password_hash
from database.models.user import User
from schemas.user import UserForgotPassword
from services.redis_token.TokenPrefix import TokenPrefix
from services.redis_token.get_user_id_by_key import get_user_id_by_key
from sqlalchemy.ext.asyncio import AsyncSession


async def forgot_password_reset(password_data: UserForgotPassword, token: str, db: AsyncSession):
    new_password = password_data.new_password.get_secret_value()
    confirm_new_password = password_data.confirm_new_password.get_secret_value()

    if new_password != confirm_new_password:
        raise HTTPException(status_code=400, detail="Passwords don't match")

    key = f'{TokenPrefix.FORGOT_PASSWORD}:{token}'
    user_id = await get_user_id_by_key(key)

    if user_id is None:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token")

    user = await db.get(User, int(user_id))
    new_hashed_password = await run_in_threadpool(get_password_hash, new_password)
    user.hashed_password = new_hashed_password
    
    try:
        await db.commit()
        await db.refresh(user)
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Password reset failed")

    return True
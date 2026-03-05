from fastapi import BackgroundTasks, HTTPException
from fastapi.concurrency import run_in_threadpool
from core.security import get_password_hash, verify_password
from database.models.user import User
from schemas.user import UserPasswordReset, UserSessionContext
from services.email.service import send_password_reset_email
from services.redis_token.TokenPrefix import TokenPrefix
from services.redis_token.generate_redis_token import generate_redis_token
from sqlalchemy.ext.asyncio import AsyncSession


# TODO option to add password for oauth users
async def password_reset_cache(cached_user: UserSessionContext, password_data: UserPasswordReset, db: AsyncSession, background_tasks: BackgroundTasks):
    user_model: User = await db.get(User, cached_user.id)
    if not user_model.hashed_password:
        raise HTTPException(status_code=400, detail="Password not set")
    
    new_pwd = password_data.new_password.get_secret_value()
    repeat_pwd = password_data.confirm_new_password.get_secret_value()
    if new_pwd != repeat_pwd:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    old_pwd_raw = password_data.old_password.get_secret_value()
    
    is_valid = await run_in_threadpool(verify_password, old_pwd_raw, user_model.hashed_password)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid old password")

    is_same = await run_in_threadpool(verify_password, new_pwd, user_model.hashed_password)
    if is_same:
        raise HTTPException(status_code=400, detail="New password must be different")

    new_hashed = await run_in_threadpool(get_password_hash, new_pwd)
    
    token = await generate_redis_token(
        f"{user_model.id}:{new_hashed}", 
        TokenPrefix.PASSWORD_RESET, 
        300
    )

    background_tasks.add_task(send_password_reset_email, user_model.email, token)

    return True
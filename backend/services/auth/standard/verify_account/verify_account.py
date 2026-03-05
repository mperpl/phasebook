from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import load_only
from database.models.user import User
from database.redis import redis_client
from sqlalchemy.ext.asyncio import AsyncSession
from services.redis_token.TokenPrefix import TokenPrefix
from services.redis_token.get_user_id_by_key import get_user_id_by_key
from core.config import settings

async def verify_account(db: AsyncSession, token: str) -> bool:
    key = f'{TokenPrefix.VERIFY_EMAIL}:{token}'

    user_id = await get_user_id_by_key(key)
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token")
    
    user_id = int(user_id)

    stmt = select(User).where(User.id == user_id).options(load_only(User.is_verified))
    user = (await db.execute(stmt)).scalar_one_or_none()
    
    if not user or user.is_verified:
        raise HTTPException(status_code=400, detail="User not found or already verified")
    
    user.is_verified = True
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Failed to update database")

    profile_key = f"user_profile:{user_id}"
    
    if await redis_client.exists(profile_key):
        async with redis_client.pipeline(transaction=False) as pipe:
            pipe.hset(profile_key, "is_verified", "1")
            pipe.expire(profile_key, settings.USER_REDIS_SESSION_TTL)
            await pipe.execute()

    return True
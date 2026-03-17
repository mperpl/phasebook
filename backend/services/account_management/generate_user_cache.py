from fastapi import HTTPException
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.user import User
from core.config import settings

async def generate_user_cache(db: AsyncSession, user_id: int, redis_client: Redis) -> bool:
    stmt = select(User).where(User.id == user_id)
    user = (await db.execute(stmt)).scalar_one_or_none()
        
    if not user:
       raise HTTPException(400, 'User not found')

    profile_key = f"user_profile:{user.id}"
    
    user_profile_data = {
        "id": str(user.id),
        "email": user.email,
        "username": user.username or "",
        "is_verified": "1" if user.is_verified else "0",
        "bio": user.bio or ""
    }

    async with redis_client.pipeline(transaction=False) as pipe:
        pipe.hset(profile_key, mapping=user_profile_data)
        pipe.expire(profile_key, settings.USER_REDIS_SESSION_TTL)

        await pipe.execute()
    
    return True
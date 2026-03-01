from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from database.redis import redis_client
from core.config import settings
from schemas import UserRead

async def find_user_by_id(db: AsyncSession, id: int) -> UserRead:
    profile_key = f"user_profile:{id}"
    user_data = await redis_client.hgetall(profile_key)
    
    if user_data:
        try:
            return UserRead.model_validate(user_data)
        except ValidationError:
            pass

    # miss
    user = await db.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_read = UserRead.model_validate(user)
    redis_data = user_read.model_dump()
    redis_data["is_verified"] = "1" if user_read.is_verified else "0"

    async with redis_client.pipeline(transaction=True) as pipe:
        pipe.hset(profile_key, mapping=redis_data)
        pipe.expire(profile_key, settings.USER_REDIS_SESSION_TTL)

        await pipe.execute()
    
    return user_read
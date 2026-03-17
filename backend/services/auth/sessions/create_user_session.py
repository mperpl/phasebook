from time import time
import uuid
from fastapi import HTTPException, Response
from redis.asyncio import Redis
from core.config import settings
from database.models.user import User


async def create_user_session(response: Response, user: User, redis_client: Redis) -> str:
    session_uuid = str(uuid.uuid4())

    session_key = f"session:{session_uuid}"
    user_sessions_set = f"user_sessions:{user.id}"
    user_profile_key = f"user_profile:{user.id}"

    user_profile_data = {
        "id": str(user.id),
        "email": user.email,
        "username": user.username or "",
        "is_verified": "1" if user.is_verified else "0",
        "bio": user.bio or ""
    }

    session_metadata = {
        "user_id": str(user.id),
        "last_refresh": str(int(time()))
    }

    try:
        async with redis_client.pipeline(transaction=True) as pipe:
            pipe.hset(user_profile_key, mapping=user_profile_data)
            pipe.expire(user_profile_key, settings.USER_REDIS_SESSION_TTL)

            pipe.hset(session_key, mapping=session_metadata)
            pipe.expire(session_key, settings.USER_REDIS_SESSION_TTL)

            pipe.sadd(user_sessions_set, session_uuid)
            pipe.expire(user_sessions_set, settings.USER_REDIS_SESSION_TTL)
            
            await pipe.execute()

        response.set_cookie(
            key="session_uuid",
            value=session_uuid,
            httponly=True,
            max_age=settings.USER_COOKIE_SESSION_TTL,
            samesite="lax",
            secure=settings.COOKIE_SECURE,
            path='/'
        )

        return session_uuid

    except Exception:
        raise HTTPException(
            status_code=500, 
            detail="Internal server error during session creation"
        )
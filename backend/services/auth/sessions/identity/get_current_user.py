from time import time
from typing import Annotated
from fastapi import Depends, HTTPException, Request, status
from database.database import DB_SESSION
from database.redis import redis_client
from core.config import settings
from schemas import UserSessionContext
from models import User
from sqlalchemy import select

async def get_current_user(request: Request, db: DB_SESSION) -> UserSessionContext:
    session_uuid = request.cookies.get("session_uuid")
    if not session_uuid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    session_key = f"session:{session_uuid}"
    session_data = await redis_client.hgetall(session_key)
    
    if not session_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired")

    user_id = session_data['user_id']
    user_profile_key = f"user_profile:{user_id}"

    user_data = await redis_client.hgetall(user_profile_key)
    # cache miss - pull from postgres
    if not user_data:
        result = await db.execute(select(User).where(User.id == int(user_id)))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User no longer exists")
        
        user_data = {
            "id": str(user.id),
            "email": user.email,
            "username": user.username or "",
            "is_verified": "1" if user.is_verified else "0",
            "bio": user.bio or ""
        }

        await redis_client.hset(user_profile_key, mapping=user_data)
        await redis_client.expire(user_profile_key, settings.USER_REDIS_SESSION_TTL)

    last_refresh = int(session_data.get('last_refresh', 0))
    now = int(time())
    
    if now - last_refresh > (settings.ACCOUNT_REDIS_SESSION_TTL // 3):
        async with redis_client.pipeline(transaction=True) as pipe:
            pipe.hset(session_key, "last_refresh", str(now))
            pipe.expire(session_key, settings.USER_REDIS_SESSION_TTL)

            pipe.expire(user_profile_key, settings.USER_REDIS_SESSION_TTL)

            pipe.expire(f"user_sessions:{user_id}", settings.USER_REDIS_SESSION_TTL)
            
            await pipe.execute()

    return UserSessionContext(
        session_uuid=session_uuid,
        **user_data
    )

CURRENT_USER = Annotated[UserSessionContext, Depends(get_current_user)]
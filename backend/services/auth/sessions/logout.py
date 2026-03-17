from fastapi import HTTPException, Request, Response, status
from redis.asyncio import Redis


async def logout_user(request: Request, response: Response, redis_client: Redis):
    session_uuid = request.cookies.get("session_uuid")
    if not session_uuid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired")

    session_key = f"session:{session_uuid}"
    user_id = await redis_client.hget(session_key, "user_id")

    await redis_client.delete(session_key)
    
    if user_id:
        user_sessions_set = f"user_sessions:{user_id}"
        await redis_client.srem(user_sessions_set, session_uuid)

        active_count = await redis_client.scard(user_sessions_set)
        if active_count == 0:
            await redis_client.delete(f"user_profile:{user_id}")

    response.delete_cookie(key="session_uuid", httponly=True, samesite="lax")
    return session_uuid
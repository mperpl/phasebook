from typing import Annotated
from fastapi import HTTPException, Request, status
from fastapi import Depends
from redis.asyncio import Redis
from database.redis import get_redis


async def guest_endpoint(request: Request, redis_client: Redis = Depends(get_redis)):
    """
    Lock logged in users from accessing the route.
    """
    session_uuid = request.cookies.get("session_uuid")
    
    if session_uuid:
        session_exists = await redis_client.exists(f"session:{session_uuid}")
        
        if session_exists:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are already logged in."
            )
    
GUEST_ENDPOINT = Annotated[None, Depends(guest_endpoint)]
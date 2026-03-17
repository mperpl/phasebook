from typing import Annotated
from fastapi import HTTPException, Request, status
from fastapi.params import Depends
from database.redis import redis_client

async def guest_endpoint(request: Request):
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
from typing import Annotated

from fastapi import Depends, HTTPException, status
from schemas import UserSessionContext
from services.auth.sessions.identity.get_current_user import CURRENT_USER


async def get_active_user(user: CURRENT_USER) -> UserSessionContext:
    if not user.is_verified or not user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Email not verified or username not set."
        )
    return user

VERIFIED_USER = Annotated[UserSessionContext, Depends(get_active_user)]
from fastapi import HTTPException
from database.models.user import User
from services.redis_token.TokenPrefix import TokenPrefix
from services.redis_token.get_user_id_by_key import get_user_id_by_key
from sqlalchemy.ext.asyncio import AsyncSession


# TODO update logic to be update first rathare than select->update
async def password_reset(token: str, db: AsyncSession):
    key = f'{TokenPrefix.PASSWORD_RESET}:{token}'
    
    redis_data: str = await get_user_id_by_key(key)

    if redis_data is None:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token")
    
    user_id, new_hashed_password = redis_data.split(":", 1)
    
    user = await db.get(User, int(user_id))
    
    user.hashed_password = new_hashed_password
    try:
        await db.commit()
        await db.refresh(user)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=409, detail=f"Failed to reset the password: [ERROR]: {e}")

    return True
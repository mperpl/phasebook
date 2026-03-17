from fastapi import HTTPException, status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.user import User


async def delete_user_account(db: AsyncSession, user_id: int, redis_client: Redis):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_sessions_key = f"user_sessions:{user_id}"
    session_uuids = await redis_client.smembers(user_sessions_key)
    
    keys_to_delete = [f"session:{uuid}" for uuid in session_uuids]
    keys_to_delete.append(user_sessions_key)
    keys_to_delete.append(f"user_profile:{user_id}")

    await db.delete(user)
    
    try:
        await db.commit()
        if keys_to_delete:
            await redis_client.delete(*keys_to_delete)
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete user")
    
    return True
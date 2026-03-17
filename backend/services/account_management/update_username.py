from fastapi import HTTPException, status
from redis.asyncio import Redis
from sqlalchemy import or_, update
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.user import User
from schemas.user import UserUpdateUsername

async def update_username(db: AsyncSession, user_id: int, new_data: UserUpdateUsername, redis_client: Redis) -> bool:
    cache_key = f"user_profile:{user_id}"
    
    try:
        stmt = (
            update(User)
            .where(
                User.id == user_id,
                or_(User.username == None, User.username == "")  # noqa: E711
            )
            .values(username=new_data.username)
            .returning(User.id)
        )
        
        result = await db.execute(stmt)
        updated_id = result.scalar_one_or_none()

        if not updated_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Update failed. User not found or username already set.")

        await db.commit()
        await redis_client.delete(cache_key)
        
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Can't set the username")
    
    return True
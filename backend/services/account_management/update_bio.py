from fastapi import HTTPException, status
from redis.asyncio import Redis
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.user import User
from schemas.user import UserUpdateBio


async def update_bio(db: AsyncSession, new_data: UserUpdateBio, id: int, redis_client: Redis) -> bool:
    stmt = (
        update(User)
        .where(User.id == id)
        .values(bio=new_data.bio)
        .returning(User.id)
    )
    
    try:
        user_id = (await db.execute(stmt)).scalar_one_or_none()

        if not user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        await db.commit()
        await redis_client.delete(f'user_profile:{id}')

    except Exception:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update the bio")
    
    return True
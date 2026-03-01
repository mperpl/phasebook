from fastapi import HTTPException, status
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from schemas import UserUpdateBio
from database.redis import redis_client

async def update_bio(db: AsyncSession, new_data: UserUpdateBio, id: int) -> bool:
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
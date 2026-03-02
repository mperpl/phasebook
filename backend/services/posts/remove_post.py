from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from models import Post
async def remove_post(db: AsyncSession, id: int) -> bool:
    try:
        stmt = delete(Post).where(Post.id == id)
        await db.execute(stmt)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to delete post. Maybe it's already gone?")
    return True
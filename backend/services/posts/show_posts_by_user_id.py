from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.post import Post


# TODO implement pagination
async def show_posts_by_user_id(db: AsyncSession, user_id: int):
    print(user_id)
    try:
        stmt = (select(Post).where(Post.author_id == user_id))
        posts = (await db.execute(stmt)).scalars().all()
        return posts
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
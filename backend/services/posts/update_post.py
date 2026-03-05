from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.post import Post
from schemas.post import WritePost


async def update_post(db: AsyncSession, user_id: int, post_id: int, update_data: WritePost):
    stmt = update(Post).where(Post.id == post_id, Post.author_id == user_id).values(update_data.model_dump(exclude_unset=True)).returning(Post)
    
    try:
        updated_post = (await db.execute(stmt)).scalar_one_or_none()

        if not updated_post:
            raise HTTPException(status_code=404, detail="Post not found or unauthorized")
            
        await db.commit()
        return updated_post
        
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(status_code=500,detail="An unexpected error occurred while updating the post")
from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.comment import Comment
from schemas.post import WritePost


async def update_comment(db: AsyncSession, post_id: int, comment_id: int, update_data: WritePost, user_id: int):
    stmt = update(Comment).where(Comment.id == comment_id, Comment.post_id == post_id, Comment.author_id == user_id).values(update_data.model_dump(exclude_unset=True)).returning(Comment)
    
    try:
        updated_comment = (await db.execute(stmt)).scalar_one_or_none()

        if not updated_comment:
            raise HTTPException(status_code=404, detail="Comment not found or unauthorized")
            
        await db.commit()
        return updated_comment
        
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(status_code=500,detail="An unexpected error occurred while updating the comment.")
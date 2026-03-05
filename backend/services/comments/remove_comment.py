from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.comment import Comment


async def remove_comment(db: AsyncSession, post_id: int, comment_id: int, user_id: int) -> bool:
    stmt = delete(Comment).where(Comment.post_id == post_id, Comment.id == comment_id, Comment.author_id == user_id)
    result = await db.execute(stmt)
    if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Comment not found.")
    try:
        await db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error.")
    return True
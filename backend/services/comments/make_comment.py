from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.comment import Comment
from schemas.comment import WriteComment

async def make_comment(db: AsyncSession, post_id: int, comment_data: WriteComment, user_id: int) -> Comment:
    new_comment = Comment(
        **comment_data.model_dump(),
        post_id=post_id,
        author_id=user_id
    )

    db.add(new_comment)
    try:
        await db.commit()
        await db.refresh(new_comment)
        return new_comment
        
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=500, 
            detail="An unexpected error occurred while creating the comment"
        )
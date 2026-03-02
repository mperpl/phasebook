from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from models import Comment
from schemas import WriteComment
from services.auth.sessions.identity.get_active_user import ACTIVATED_USER

async def make_comment(
    db: AsyncSession, 
    post_id: int, 
    comment_data: WriteComment, 
    current_user: ACTIVATED_USER
) -> Comment:
    new_comment = Comment(
        **comment_data.model_dump(),
        post_id=post_id,
        author_id=current_user.id
    )

    try:
        db.add(new_comment)
        await db.commit()
        await db.refresh(new_comment)
        return new_comment
        
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=500, 
            detail="An unexpected error occurred while creating the comment"
        )
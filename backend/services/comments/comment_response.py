from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.comment import Comment
from schemas.comment import WriteComment
from services.auth.sessions.identity.get_active_user import ACTIVATED_USER

async def comment_response(db: AsyncSession, post_id: int, parent_comment_id: int,comment_data: WriteComment, current_user: ACTIVATED_USER) -> Comment:
    response_comment = Comment(
        **comment_data.model_dump(),
        post_id=post_id,
        author_id=current_user.id,
        parent_id=parent_comment_id
    )

    db.add(response_comment)
    try:
        await db.commit()
        await db.refresh(response_comment)
        return response_comment
        
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=500, 
            detail="An unexpected error occurred while creating the comment"
        )
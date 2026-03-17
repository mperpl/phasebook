from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.post import Post
from schemas.post import ReadPost, WritePost


async def make_post(db: AsyncSession, user_id: int, post_data: WritePost) -> ReadPost:
    new_post = Post(
        author_id=user_id, 
        content=post_data.content,
        is_public=post_data.is_public
    )
    try:
        db.add(new_post)
        await db.commit()
        await db.refresh(new_post)
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred while creating the post")

    # 2. Return using Pydantic's validation
    try:
        new_post = ReadPost.model_validate(new_post)
        return new_post
    except ValidationError:
        raise HTTPException(status_code=500, detail="Couldn't validate the post.")
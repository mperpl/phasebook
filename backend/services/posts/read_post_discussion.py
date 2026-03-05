from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from database.models.comment import Comment
from database.models.post import Post


# TODO we first check for cached user data
async def read_post_discussion(db: AsyncSession, post_id: int) -> Post:
    stmt = (
        select(Post)
        .where(Post.id == post_id)
        .options(
            selectinload(Post.author),
            selectinload(Post.comments.and_(Comment.parent_id == None))  # noqa: E711
            .selectinload(Comment.author) 
        )
    )
    
    result = await db.execute(stmt)
    post = result.scalars().first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
        
    return post
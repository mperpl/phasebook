from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from models import Post

async def read_post_discussion(db: AsyncSession, post_id: int) -> Post:
    stmt = (
        select(Post)
        .where(Post.id == post_id)
        .options(selectinload(Post.comments))
    )
    
    result = await db.execute(stmt)
    post = result.scalars().first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
        
    return post
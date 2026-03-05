from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from database.models.comment import Comment


async def read_replies(db: AsyncSession, post_id: int, parent_id: int) -> list[Comment]:
    stmt = select(Comment).where(Comment.parent_id == parent_id, Comment.post_id == post_id).options(selectinload(Comment.author)).order_by(Comment.created_at.asc())
    replies = (await db.execute(stmt)).scalars().all()
    return replies
from fastapi import HTTPException
from sqlalchemy import and_, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.friendship import Friendship

async def delete_relationship(db: AsyncSession, friend_id: int, my_id: int):
    if friend_id == my_id:
        raise HTTPException(status_code=400, detail="Bad request.")
    stmt = (
        delete(Friendship)
        .where(
            or_(
                and_(Friendship.sender_id == my_id, Friendship.receiver_id == friend_id),
                and_(Friendship.sender_id == friend_id, Friendship.receiver_id == my_id)
            )
        )
        .returning(Friendship.id)
    )

    try:
        deleted_id = (await db.execute(stmt)).scalar_one_or_none()
        if not deleted_id:
            raise HTTPException(status_code=404, detail="Relationship not found.")

        await db.commit()
        return {"message": "Operation success."}

    except Exception:
        await db.rollback()
        raise HTTPException(status_code=404, detail="Relationship not found.")
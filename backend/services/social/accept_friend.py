from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.friendship import Friendship, FriendshipStatus


async def accept_friend(db: AsyncSession, my_id: int, sender_id: int):
    if sender_id == my_id:
        raise HTTPException(status_code=400, detail="You cannot accept a friend request from yourself.")

    stmt = select(Friendship).where(Friendship.receiver_id == my_id, Friendship.sender_id == sender_id)

    existing_friendship = (await db.execute(stmt)).scalar_one_or_none()

    if not existing_friendship:
        raise HTTPException(status_code=404, detail="Relationship not found.")
    if existing_friendship:
        if existing_friendship.status == FriendshipStatus.PENDING:
            existing_friendship.status = FriendshipStatus.ACCEPTED
            existing_friendship.action_by_id = my_id
            try:
                await db.commit()
                return {"message": "Friend request accepted."}
            except Exception:
                await db.rollback()
                raise HTTPException(status_code=500, detail="Database error occurred.")
        elif existing_friendship.status == FriendshipStatus.ACCEPTED:
            raise HTTPException(status_code=400, detail="You are already friends.")
        elif existing_friendship.status == FriendshipStatus.BLOCKED:
            raise HTTPException(status_code=400, detail="You are blocked.")
    
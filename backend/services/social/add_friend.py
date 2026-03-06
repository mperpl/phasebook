from fastapi import HTTPException, status
from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.friendship import Friendship, FriendshipStatus


async def add_friend(db: AsyncSession, sender_id: int, receiver_id: int):
    if sender_id == receiver_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot send a friend request to yourself.")

    stmt = select(Friendship).where(
        or_(
            and_(Friendship.sender_id == sender_id, Friendship.receiver_id == receiver_id),
            and_(Friendship.sender_id == receiver_id, Friendship.receiver_id == sender_id)
        )
    )

    existing_friendship = (await db.execute(stmt)).scalar_one_or_none()

    if existing_friendship:
        if existing_friendship.status == FriendshipStatus.ACCEPTED:
            raise HTTPException(status_code=400, detail="You are already friends.")
        if existing_friendship.status == FriendshipStatus.BLOCKED:
            raise HTTPException(status_code=400, detail="Can't add blocked user.")
        if existing_friendship.status == FriendshipStatus.PENDING:
            raise HTTPException(status_code=400, detail="Request already pending.")
            
            

    new_friendship_request = Friendship(
        sender_id=sender_id,
        receiver_id=receiver_id,
        status=FriendshipStatus.PENDING,
        action_by_id=sender_id
    )
    
    db.add(new_friendship_request)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=404, detail="User not found.")
    
    return {"message": "Friend request sent."}
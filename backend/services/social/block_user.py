from fastapi import HTTPException
from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.friendship import Friendship, FriendshipStatus


async def block_user(db: AsyncSession, receiver_id: int, my_id: int):
    if my_id == receiver_id:
        raise HTTPException(status_code=400, detail="You cannot block yourself.")

    stmt = select(Friendship).where(
        or_(
            and_(Friendship.sender_id == my_id, Friendship.receiver_id == receiver_id),
            and_(Friendship.sender_id == receiver_id, Friendship.receiver_id == my_id)
        )
    )

    existing_relationship = (await db.execute(stmt)).scalar_one_or_none()
    if existing_relationship:
        if existing_relationship.status == FriendshipStatus.BLOCKED:
            raise HTTPException(status_code=400, detail="Already blocked.")
        
        existing_relationship.status = FriendshipStatus.BLOCKED
        existing_relationship.action_by_id = my_id
        try:
            await db.commit()
            return {"message": "User blocked successfully."}
        except Exception:
            raise HTTPException(500, 'Database error occured.')
            

    new_relationship = Friendship(
        sender_id=my_id,
        receiver_id=receiver_id,
        status=FriendshipStatus.BLOCKED,
        action_by_id=my_id
    )
    
    db.add(new_relationship)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred.")
    
    return {"message": "User blocked successfully."}
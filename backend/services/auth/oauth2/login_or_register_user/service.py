from typing import Any, Dict
from fastapi import HTTPException, Response, status
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from database.models.user import OAuthAccount, User
from services.auth.oauth2.login_or_register_user._get_cached_provider_id import _get_cached_provider_id
from services.auth.sessions.create_user_session import create_user_session

async def login_or_register_user(db: AsyncSession, response: Response, normalized_user: Dict[str, Any]) -> User:
    provider_id = await _get_cached_provider_id(db, normalized_user["provider"])

    stmt = (
        select(User)
        .outerjoin(User.oauth_accounts)
        .where(
            or_(
                User.email == normalized_user["email"],
                (OAuthAccount.provider_id == provider_id) & 
                (OAuthAccount.provider_user_id == str(normalized_user["uid"]))
            )
        )
        .options(selectinload(User.oauth_accounts))
    )
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user:
        is_linked = any(oauth_account.provider_id == provider_id for oauth_account in user.oauth_accounts)
        
        if is_linked:
            # PATH A: Known OAuth User
            await create_user_session(response, user)
            await db.commit()
            return user
        
        # PATH B: Existing user, but NOT linked to this provider yet
        if user.hashed_password:
            # Traditional / Mixed User
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered. Please log in with your password to link this account."
            )
        else:
            # OAuth-only User
            new_oauth = OAuthAccount(
                user_id=user.id,
                provider_id=provider_id,
                provider_user_id=str(normalized_user["uid"])
            )
            db.add(new_oauth)
            
            try:
                await create_user_session(response, user)
                await db.commit()
                await db.refresh(user)
                return user
            except IntegrityError:
                await db.rollback()
                raise HTTPException(status_code=409, detail="Account linking conflict")

    # PATH C: Brand New User Registration 
    user = User(email=normalized_user["email"], is_verified=True)
    db.add(user)
    await db.flush()

    new_oauth = OAuthAccount(
        user_id=user.id,
        provider_id=provider_id,
        provider_user_id=str(normalized_user["uid"])
    )
    db.add(new_oauth)

    try:
        await create_user_session(response, user)
        await db.commit()
        await db.refresh(user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Account registration conflict")
    
    return user
from fastapi.concurrency import run_in_threadpool
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Response
from models import User
from core.security import verify_password
from services.auth.sessions.create_user_session import create_user_session
from schemas import UserLogin

async def login_user(db: AsyncSession, user_data: UserLogin, response: Response) -> User:
    """ Login logic. returns User instance on success, raises HTTPException on failure.
    Args:
        db: DB_SESSSION (db instance for database operations)
        user_data: UserLogin (data from the request)
        response: Response (needed to set cookies)
    Raises:
        HTTPException: If the user is not found or the password is incorrect.
    Returns:
        User
    """
    login_id = user_data.identifier.strip().lower()

    stmt = select(User).where(
        or_(
            User.email == login_id,
            User.username == login_id
        )
    )

    user = (await db.execute(stmt)).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid identifier or password"
        )
    
    if not user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="An accout associated with the email already exists. Please use your previous login method and link the accounts in the settings"
        )

    is_password_valid = await run_in_threadpool(
        verify_password, 
        user_data.password.get_secret_value(), 
        user.hashed_password
    )
    
    if not is_password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid identifier or password"
        )
    
    await create_user_session(response, user)
    
    return user
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import BackgroundTasks, HTTPException, status, Response
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import load_only
from core.security import get_password_hash
from database.models.user import User
from schemas.user import UserRegister
from services.auth.sessions.create_user_session import create_user_session
from services.email.service import send_registration_email
from services.redis_token.TokenPrefix import TokenPrefix
from services.redis_token.generate_redis_token import generate_redis_token

async def register_new_user(db: AsyncSession, user_data: UserRegister, response: Response,  background_tasks: BackgroundTasks):
    """
    Returns a User instance on successful registration and sets a session cookie.
    Args:
        db: DB_SESSION (db instance for database operations)
        user_data: UserRegister (data from the request)
        response: Response (needed to set cookies)
    Raises:
        HTTPException: If email is already taken.
    Returns:
        User
    """

    if user_data.password == user_data.password_repeat:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Passwords must be the same")

    hashed_password = await run_in_threadpool(get_password_hash, user_data.password.get_secret_value())

    stmt = select(User).where(or_(User.email == user_data.email, User.username == user_data.username)).options(load_only(User.username, User.email))
    user = (await db.execute(stmt)).scalar_one_or_none()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed during background processing [ERROR]: {e}")
    
    await create_user_session(response, new_user)

    try:
        key = await generate_redis_token(new_user.id, TokenPrefix.VERIFY_EMAIL, 300)
        background_tasks.add_task(send_registration_email, new_user.email, key)
    except Exception:
        print("Failed to send verification email")

    return new_user
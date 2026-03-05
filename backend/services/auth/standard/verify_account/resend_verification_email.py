from fastapi import BackgroundTasks, HTTPException
from schemas.user import UserSessionContext
from services.email.service import send_registration_email
from services.redis_token.TokenPrefix import TokenPrefix
from services.redis_token.generate_redis_token import generate_redis_token


async def resend_verification_email(background_tasks: BackgroundTasks, user: UserSessionContext):
    if not user.email:
        raise HTTPException(status_code=400, detail="User does not have an email address")
    try:
        key = await generate_redis_token(user.id, TokenPrefix.VERIFY_EMAIL, expire_seconds=300)
        background_tasks.add_task(send_registration_email, user.email, key)
    except Exception as e:
        print("Failed to send verification email:", str(e))
        raise HTTPException(status_code=500, detail="Failed to resend verification email")
    return True
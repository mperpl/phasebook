from fastapi import APIRouter, BackgroundTasks, Request, HTTPException, Response
from pydantic import EmailStr
from database.redis import REDIS_SESSION
from core.limiter import limiter
from schemas.user import UserForgotPassword, UserLogin, UserPasswordReset, UserRead, UserRegister
from services.account_management.delete_user_account import delete_user_account
from services.auth.oauth2.oauth2_service import oauth, oauth2_service
from services.auth.oauth2.SUPPORTED_PROVIDERS import SUPPORTED_PROVIDERS
from database.database import DB_SESSION
from services.auth.sessions.logout import logout_user
from services.auth.sessions.identity.get_current_user import CURRENT_USER
from services.auth.sessions.identity.guest_endpoint import GUEST_ENDPOINT
from services.auth.sessions.logout_all import logout_all
from services.auth.standard.forgot_password.forgot_password_email import forgot_password_email
from services.auth.standard.forgot_password.forgot_password_reset import forgot_password_reset
from services.auth.standard.register_new_user import register_new_user
from services.auth.standard.login_user import login_user
from services.auth.standard.reset_password.password_reset import password_reset
from services.auth.standard.reset_password.password_reset_cache import password_reset_cache
from services.auth.standard.verify_account.verify_account import verify_account
from services.auth.standard.verify_account.resend_verification_email import resend_verification_email


router = APIRouter()


@router.delete("/delete")
@limiter.limit("1/minute")
async def delete_user(request: Request, user: CURRENT_USER, db: DB_SESSION, redis: REDIS_SESSION):
    success = await delete_user_account(db, int(user.id), redis)
    return {"detail": success}


@router.put("/refresh-session")
@limiter.limit("1/minute")
async def ping(request: Request, _: CURRENT_USER):
    return {"detail": "session refreshed"}


@router.post("/register")
@limiter.limit("5/minute")
async def register(request: Request, user_data: UserRegister, db: DB_SESSION, _: GUEST_ENDPOINT, response: Response, background_tasks: BackgroundTasks, redis: REDIS_SESSION):
    user = await register_new_user(db, user_data, response, background_tasks, redis)
    return {"message": "Registration successful", "user": user}


@router.get("/verify/{token}")
@limiter.limit("2/minute")
async def verify(request: Request, db: DB_SESSION, token: str, redis: REDIS_SESSION):
    user = await verify_account(db, token, redis)
    return {"message": "Verification successful", "user": user}


@router.post("/verify/resend", response_model=None)
@limiter.limit("1/minute")
async def resend_verification(request: Request, background_tasks: BackgroundTasks, user: CURRENT_USER):
    if user.is_verified:
        raise HTTPException(status_code=400, detail="Account is already verified")
    
    success = await resend_verification_email(background_tasks, user)
    return {"message": "Verification email resent"} if success else {"message": "Failed to resend verification email"}


@router.post("/login", response_model=UserRead)
@limiter.limit("5/minute")
async def login(request: Request, user_data: UserLogin, db: DB_SESSION, _: GUEST_ENDPOINT, response: Response, redis: REDIS_SESSION):
    user = await login_user(db, user_data, response, redis)
    return user


@router.post("/forgot-password")
@limiter.limit("2/minute")
async def forgot_password(request: Request, email: EmailStr, background_tasks: BackgroundTasks, _: GUEST_ENDPOINT, db: DB_SESSION):
    success = await forgot_password_email(email, background_tasks, db)
    return {'message': 'Mail sent successfully'} if success else {'message': 'Failed to proceed with password reset'}


# test using postman - browser send a get request when you click on a link
@router.patch("/forgot-password/{token}")
@limiter.limit("3/day")
async def forgot_password_verified(request: Request, db: DB_SESSION, token: str, password_data: UserForgotPassword):
    success = await forgot_password_reset(password_data, token, db)
    return {"message": "Password reset successful"} if success else {"message": "Failed to reset password"}


@router.post("/password-reset")
@limiter.limit("2/minute")
async def reset_user_password(request: Request, background_tasks: BackgroundTasks, db: DB_SESSION, user: CURRENT_USER, password_data: UserPasswordReset):
    success = await password_reset_cache(user, password_data, db, background_tasks)
    return {'message': 'Mail sent successfully'} if success else {'message': 'Failed to proceed with password reset'}


@router.patch("/password-reset/{token}")
@limiter.limit("1/day")
async def reset_user_password_verified(request: Request, db: DB_SESSION, token: str):
    success = await password_reset(token, db)
    return {"message": "Password reset successfully"} if success else {"message": "Failed to reset password"}


@router.post("/logout")
@limiter.limit("2/minute")
async def logout(request: Request, response: Response, redis: REDIS_SESSION):
    session_id = await logout_user(request, response, redis)
    message = {"message": "Logout successful", "session_id": session_id} if session_id else {"message": "No active session found"}
    return message


@router.delete("/logout-all")
@limiter.limit("2/minute")
async def logout_global(request: Request, response: Response, user: CURRENT_USER, redis: REDIS_SESSION):
    session_id = await logout_all(int(user.id), redis)
    message = {"message": "Logout successful", "session_id": session_id} if session_id else {"message": "No active session found"}
    return message


@router.get("/oauth2/login/{provider}")
@limiter.limit("2/minute")
async def login_via_provider(request: Request, provider: str, _: GUEST_ENDPOINT):
    if provider.lower() not in SUPPORTED_PROVIDERS:
        raise HTTPException(status_code=400, detail="Unsupported provider")
    
    client = oauth.create_client(provider)
    redirect_uri = request.url_for('auth_by_provider', provider=provider)
    
    return await client.authorize_redirect(request, redirect_uri)


@router.get("/oauth2/callback/{provider}")
@limiter.limit("2/minute")
async def auth_by_provider(request: Request, provider: str, response: Response, db: DB_SESSION,_: GUEST_ENDPOINT, redis: REDIS_SESSION):
    client = oauth.create_client(provider)
    user = await oauth2_service(db, response, client, provider, request, redis)

    return {"status": "ok", "username": user.username}
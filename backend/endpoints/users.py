from fastapi import APIRouter, Request
from core.limiter import limiter
from database.database import DB_SESSION
from schemas import UserRead, UserUpdateBio, UserUpdateUsername
from services.account_management.update_username import update_username
from services.account_management.generate_user_cache import generate_user_cache
from services.account_management.update_bio import update_bio
from services.auth.sessions.identity.get_current_user import CURRENT_USER
from services.social.find_user_by_id import find_user_by_id


router = APIRouter()


@router.get("/me", response_model=UserRead)
@limiter.limit("2/minute")
async def get_current_user_profile(request: Request, current_user: CURRENT_USER):
    return current_user


@router.post("/refresh")
@limiter.limit("2/minute")
async def refresh_current_user_profile(request: Request, db: DB_SESSION, current_user: CURRENT_USER):
    success = await generate_user_cache(db, int(current_user.id))
    return success


@router.get("/{id}")
@limiter.limit("2/minute")
async def get_user_profile_by_id(request: Request, id: int, db: DB_SESSION):
    profile = await find_user_by_id(db, id)
    return profile

# TODO insecure to let users generate caches on profiles other than theirs
# @router.post("/{id}/refresh")
# @limiter.limit("2/day")
# async def refresh_user_profile_by_id(request: Request, id: int, db: DB_SESSION):
#     success = await generate_user_cache(db, id)
#     return success


@router.post("/me/bio")
@limiter.limit("2/minute")
async def update_current_bio(request: Request, db: DB_SESSION, current_user: CURRENT_USER, new_data: UserUpdateBio):
    success = await update_bio(db, new_data, int(current_user.id))
    return success


@router.post("/me/username")
@limiter.limit("2/minute")
async def update_current_profile(request: Request, db: DB_SESSION, current_user: CURRENT_USER, new_data: UserUpdateUsername):
    success = await update_username(db, int(current_user.id), new_data)
    return success


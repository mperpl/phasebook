from fastapi import APIRouter, Request
from database.redis import REDIS_SESSION
from core.limiter import limiter
from database.database import DB_SESSION
from schemas.user import UserRead, UserUpdateBio, UserUpdateUsername
from services.account_management.update_username import update_username
from services.account_management.generate_user_cache import generate_user_cache
from services.account_management.update_bio import update_bio
from services.auth.sessions.identity.get_active_user import ACTIVATED_USER
from services.auth.sessions.identity.get_current_user import CURRENT_USER
from services.posts.show_posts_by_user_id import show_posts_by_user_id
from services.social.accept_friend import accept_friend
from services.social.block_user import block_user
from services.social.delete_relationship import delete_relationship
from services.social.find_user_by_id import find_user_by_id
from services.social.add_friend import add_friend


router = APIRouter()


@router.get("/posts")
@limiter.limit("2/minute")
async def display_my_posts(request: Request, db: DB_SESSION, current_user: CURRENT_USER):
    posts = await show_posts_by_user_id(db, int(current_user.id))
    return posts


@router.get("/{id}/posts")
@limiter.limit("2/minute")
async def display_posts_by_user_id(request: Request, db: DB_SESSION, id: int):
    posts = await show_posts_by_user_id(db, id)
    return posts


@router.put("/add/{receiver_id}")
@limiter.limit("2/minute")
async def friend(request: Request, db: DB_SESSION, receiver_id: int, user: ACTIVATED_USER):
    return await add_friend(db, int(user.id), receiver_id)


@router.patch("/accept/{sender_id}")
@limiter.limit("2/minute")
async def accept_friend_request(request: Request, db: DB_SESSION, sender_id: int, user: ACTIVATED_USER):
    return await accept_friend(db, int(user.id), sender_id)


@router.delete("/unfriend/{friend_id}")
@limiter.limit("2/minute")
async def unfriend(request: Request, db: DB_SESSION, friend_id: int, user: ACTIVATED_USER):
    return await delete_relationship(db, friend_id, int(user.id))


@router.put("/block/{receiver_id}")
@limiter.limit("2/minute")
async def block(request: Request, db: DB_SESSION, receiver_id: int, user: ACTIVATED_USER):
    return await block_user(db, receiver_id, int(user.id))


@router.delete("/unblock/{receiver_id}")
@limiter.limit("2/minute")
async def unblock(request: Request, db: DB_SESSION, reciver_id: int, user: ACTIVATED_USER):
    return await delete_relationship(db, reciver_id, int(user.id))


@router.get("/me", response_model=UserRead)
@limiter.limit("2/minute")
async def get_current_user_profile(request: Request, current_user: CURRENT_USER):
    return current_user


@router.put("/refresh")
@limiter.limit("1/minute")
async def refresh_current_user_profile(request: Request, db: DB_SESSION, current_user: CURRENT_USER, redis: REDIS_SESSION):
    success = await generate_user_cache(db, int(current_user.id), redis)
    return success


@router.get("/{id}")
@limiter.limit("2/minute")
async def get_user_profile_by_id(request: Request, id: int, db: DB_SESSION, redis: REDIS_SESSION):
    profile = await find_user_by_id(db, id, redis)
    return profile

# TODO insecure to let users generate caches on profiles other than theirs
# @router.post("/{id}/refresh")
# @limiter.limit("2/day")
# async def refresh_user_profile_by_id(request: Request, id: int, db: DB_SESSION):
#     success = await generate_user_cache(db, id)
#     return success


@router.patch("/edit/bio")
@limiter.limit("2/minute")
async def update_current_bio(request: Request, db: DB_SESSION, current_user: CURRENT_USER, new_data: UserUpdateBio, redis: REDIS_SESSION):
    success = await update_bio(db, new_data, int(current_user.id), redis)
    return success


@router.patch("/edit/username")
@limiter.limit("2/minute")
async def update_current_profile(request: Request, db: DB_SESSION, current_user: CURRENT_USER, new_data: UserUpdateUsername, redis: REDIS_SESSION):
    success = await update_username(db, int(current_user.id), new_data, redis)
    return success


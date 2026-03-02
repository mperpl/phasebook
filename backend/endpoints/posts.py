from fastapi import APIRouter, Request
from core.limiter import limiter
from database.database import DB_SESSION
from schemas import ReadPost, WriteComment, WritePost
from services.auth.sessions.identity.get_active_user import ACTIVATED_USER
from services.posts.make_comment import make_comment
from services.posts.make_post import make_post
from services.posts.read_post_discussion import read_post_discussion
from services.posts.remove_post import remove_post


router = APIRouter()

@router.post("/create", response_model=ReadPost)
@limiter.limit("2/minute")
async def post(request: Request, post_data: WritePost, db: DB_SESSION, current_user: ACTIVATED_USER):
    res = await make_post(db, int(current_user.id), post_data)
    return res


@router.post("/{post_id}/comment")
@limiter.limit("2/minute")
async def comment(
    request: Request, 
    db: DB_SESSION, 
    post_id: int, 
    comment_data: WriteComment, 
    current_user: ACTIVATED_USER
):
    success = await make_comment(db, post_id, comment_data, current_user)
    return success


@router.post("/{post_id}/discuss")
@limiter.limit("2/minute")
async def read_post_discussion_by_id(request: Request,db: DB_SESSION, post_id: int):
    success = await read_post_discussion(db, post_id)
    return success


@router.delete("/delete/{id}")
@limiter.limit("2/minute")
async def delete_post(request: Request, db: DB_SESSION, id: int, _: ACTIVATED_USER):
    success = await remove_post(db, id,)
    return success

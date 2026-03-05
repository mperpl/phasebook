from fastapi import APIRouter, Request
from core.limiter import limiter
from database.database import DB_SESSION
from schemas.comment import WriteComment
from services.auth.sessions.identity.get_active_user import ACTIVATED_USER
from services.comments.comment_response import comment_response
from services.comments.make_comment import make_comment
from services.comments.read_replies import read_replies
from services.comments.remove_comment import remove_comment
from services.comments.update_comment import update_comment


router = APIRouter()


@router.post("/post/{post_id}/create")
@limiter.limit("2/minute")
async def comment(request: Request, db: DB_SESSION, post_id: int, comment_data: WriteComment, current_user: ACTIVATED_USER):
    success = await make_comment(db, post_id, comment_data, int(current_user.id))
    return success


@router.patch("/post/{post_id}/comment/{comment_id}/update")
@limiter.limit("2/minute")
async def update(request: Request, db: DB_SESSION, post_id: int, comment_id: int, update_data: WriteComment, current_user: ACTIVATED_USER):
    success = await update_comment(db, post_id, comment_id, update_data, int(current_user.id))
    return success



@router.get("/post/{post_id}/comment/{comment_id}/replies")
@limiter.limit("2/minute")
async def replies(request: Request, db: DB_SESSION, post_id: int, parent_id: int, _: ACTIVATED_USER):
    success = await read_replies(db, post_id, parent_id)
    return success


@router.post("/post/{post_id}/comment/{comment_id}/respond")
@limiter.limit("2/minute")
async def respond(request: Request, db: DB_SESSION, post_id: int, parrent_comment_id: int, comment_data: WriteComment, current_user: ACTIVATED_USER):
    success = await comment_response(db, post_id, parrent_comment_id, comment_data, current_user)
    return success


@router.delete("/post/{post_id}/remove")
@limiter.limit("2/minute")
async def remove(request: Request, db: DB_SESSION, post_id: int, comment_id: int, current_user: ACTIVATED_USER):
    success = await remove_comment(db, post_id, comment_id, int(current_user.id))
    return success
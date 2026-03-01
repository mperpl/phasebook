from fastapi import APIRouter, Request
from core.limiter import limiter
from database.database import DB_SESSION
from services.auth.sessions.identity.get_current_user import CURRENT_USER


router = APIRouter()

@router.get("/post")
@limiter.limit("2/minute")
async def get_user_data(request: Request, db: DB_SESSION, current_user: CURRENT_USER):
    return current_user
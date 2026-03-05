from fastapi import APIRouter, Request
from core.limiter import limiter


router = APIRouter()


@router.post("/chatbot")
@limiter.limit("5/minute")
async def ask_question(request: Request):
    return True


@router.post("/post/create/moderate")
@limiter.limit("5/minute")
async def moderator(request: Request):
    return True


@router.post("/post/{id}/sumarize")
@limiter.limit("5/minute")
async def post_sumarizator(request: Request):
    return True


@router.post("/post/{id}/discussion/sumarize")
@limiter.limit("5/minute")
async def discussion_sumarizator(request: Request):
    return True
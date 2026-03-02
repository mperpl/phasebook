from fastapi import APIRouter, Request
from core.limiter import limiter


router = APIRouter()


@router.post("/chatbot")
@limiter.limit("5/minute")
async def ask_question(request: Request):
    return True
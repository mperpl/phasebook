from typing import Annotated
from fastapi import Depends
import redis.asyncio as redis
from core.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

async def get_redis():
    async with redis_client as conn:
        yield conn

REDIS_SESSION = Annotated[redis.Redis, Depends(get_redis)]
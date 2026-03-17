import secrets
from redis.asyncio import Redis
from core.config import settings
from services.redis_token.TokenPrefix import TokenPrefix

async def generate_redis_token(user_id: int, prefix: TokenPrefix, redis_client: Redis, expire_seconds: int = settings.USER_REDIS_SESSION_TTL) -> str:
    """
    Stores a token in Redis with a TTL (default 15m).
    Key format: 'TokenPrefix:{token}' -> Value: user_id
    Raises:
        ValueError: If user_id or prefix is not provided.
    """
    if user_id is None or prefix is None:
        raise ValueError("user_id and prefix must be provided")
    
    token = secrets.token_urlsafe(32)
    key = f"{prefix}:{token}"
    await redis_client.set(key, user_id, ex=expire_seconds)

    return token
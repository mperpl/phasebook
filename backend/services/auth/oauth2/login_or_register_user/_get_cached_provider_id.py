from typing import Optional
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.provider import OAuthProvider


async def _get_cached_provider_id(db: AsyncSession, provider_name: str, redis_client: Redis) -> Optional[int]:
    """Retrieves provider ID from Redis, or DB if not cached."""
    key = f"provider:{provider_name}"
    
    povider_id = await redis_client.get(key)
    if povider_id:
        return int(povider_id)

    stmt = select(OAuthProvider).where(OAuthProvider.provider == provider_name)
    provider_row = (await db.execute(stmt)).scalar_one_or_none()
    
    if provider_row:
        await redis_client.set(key, provider_row.id)
        return provider_row.id
    
    return None
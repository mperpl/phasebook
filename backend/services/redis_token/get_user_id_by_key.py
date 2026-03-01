from database.redis import redis_client

async def get_user_id_by_key(key: str) -> int | None:
    """ Retrieves user_id as str and immediately deletes the token (single use). """
    user_id = await redis_client.get(key)
    if user_id:
        await redis_client.delete(key)
    return user_id if user_id else None
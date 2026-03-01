from database.redis import redis_client

async def logout_all(user_id: int) -> bool:
    index_key = f"user_sessions:{user_id}"
    profile_key = f"user_profile:{user_id}"
    
    session_ids = await redis_client.smembers(index_key)
    
    keys_to_del = [f"session:{sid}" for sid in session_ids]
    keys_to_del.append(index_key)
    keys_to_del.append(profile_key)
   
    if session_ids:
        await redis_client.delete(*keys_to_del)
        return True
    return False
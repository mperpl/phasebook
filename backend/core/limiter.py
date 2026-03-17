from slowapi import Limiter
from slowapi.util import get_remote_address
from core.config import settings

limiter = Limiter(key_func=get_remote_address, enabled=False, default_limits=["5/minute"], storage_uri=settings.REDIS_URL)
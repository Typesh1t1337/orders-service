import redis.asyncio as redis
from core.config import settings

redis_client = redis.from_url(
    url=settings.redis_connection,
    decode_responses=True
)


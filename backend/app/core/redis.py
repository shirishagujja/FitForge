from redis.asyncio import Redis

from app.config import get_settings

_redis_client: Redis | None = None


def get_redis_client() -> Redis:
    """Return a shared async Redis client (URL resolved at first use)."""
    global _redis_client
    if _redis_client is None:
        settings = get_settings()
        _redis_client = Redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )
    return _redis_client


async def close_redis_client() -> None:
    """Close the shared Redis client on application shutdown."""
    global _redis_client
    if _redis_client is not None:
        await _redis_client.aclose()
        _redis_client = None

from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.core.database import async_session_factory
from app.core.redis import get_redis_client

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, Any]:
    """Liveness probe — confirms the API process is running."""
    return {"data": {"status": "ok"}}


@router.get("/ready")
async def ready() -> JSONResponse:
    """Readiness probe — verifies downstream dependencies.

    Returns HTTP 503 when any dependency is down so load balancers
    and orchestrators can remove this instance from rotation.
    """
    checks: dict[str, str] = {"database": "down", "redis": "down"}

    try:
        async with async_session_factory() as session:
            await session.execute(text("SELECT 1"))
        checks["database"] = "up"
    except Exception:
        checks["database"] = "down"

    try:
        redis = get_redis_client()
        if await redis.ping():
            checks["redis"] = "up"
    except Exception:
        checks["redis"] = "down"

    all_up = all(status == "up" for status in checks.values())
    body = {
        "data": {
            "status": "ok" if all_up else "degraded",
            "checks": checks,
        }
    }
    return JSONResponse(status_code=200 if all_up else 503, content=body)

from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session_factory
from app.modules.auth.models import User
from app.modules.auth.service import get_current_user_from_token

bearer_scheme = HTTPBearer(auto_error=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provide a database session for request scope."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Resolve the authenticated user from the Bearer access token."""
    from app.core.exceptions import AppException

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise AppException(
            code="UNAUTHORIZED",
            message="Not authenticated",
            status_code=401,
        )

    return await get_current_user_from_token(db, credentials.credentials)

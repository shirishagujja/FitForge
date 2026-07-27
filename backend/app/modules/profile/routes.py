"""Profile HTTP routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppException
from app.dependencies import get_current_user, get_db
from app.modules.auth.models import User
from app.modules.profile import service as profile_service
from app.modules.profile.schemas import ProfileUpsert

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("")
async def get_profile(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    profile = await profile_service.get_profile(db, user)
    if profile is None:
        raise AppException(code="NOT_FOUND", message="Profile not found", status_code=404)
    return {"data": profile_service.to_profile_response(profile)}


@router.put("")
async def upsert_profile(
    payload: ProfileUpsert,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    profile = await profile_service.upsert_profile(db, user, payload)
    return {"data": profile_service.to_profile_response(profile)}

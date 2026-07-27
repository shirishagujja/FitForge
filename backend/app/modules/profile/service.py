"""Profile business logic: single-row-per-user upsert."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import User
from app.modules.profile.models import Profile
from app.modules.profile.schemas import ProfileResponse, ProfileUpsert


async def get_profile(db: AsyncSession, user: User) -> Profile | None:
    return await db.scalar(select(Profile).where(Profile.user_id == user.id))


async def has_profile(db: AsyncSession, user: User) -> bool:
    return await get_profile(db, user) is not None


def _apply_fields(profile: Profile, payload: ProfileUpsert) -> None:
    profile.display_name = payload.display_name
    profile.date_of_birth = payload.date_of_birth
    profile.sex = payload.sex
    profile.height_cm = payload.height_cm
    profile.fitness_goal = payload.fitness_goal
    profile.activity_level = payload.activity_level


async def upsert_profile(db: AsyncSession, user: User, payload: ProfileUpsert) -> Profile:
    profile = await get_profile(db, user)
    if profile is None:
        profile = Profile(user_id=user.id)
        db.add(profile)
    _apply_fields(profile, payload)
    await db.flush()
    await db.refresh(profile)
    return profile


def to_profile_response(profile: Profile) -> ProfileResponse:
    return ProfileResponse.model_validate(profile)

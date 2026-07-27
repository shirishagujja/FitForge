"""Profile request/response Pydantic schemas."""

from __future__ import annotations

import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.modules.profile.models import ActivityLevel, Sex


class ProfileUpsert(BaseModel):
    display_name: str | None = Field(default=None, max_length=100)
    date_of_birth: date | None = None
    sex: Sex | None = None
    height_cm: float | None = Field(default=None, gt=0, le=300)
    fitness_goal: str | None = Field(default=None, max_length=255)
    activity_level: ActivityLevel | None = None


class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    display_name: str | None = None
    date_of_birth: date | None = None
    sex: Sex | None = None
    height_cm: float | None = None
    fitness_goal: str | None = None
    activity_level: ActivityLevel | None = None
    created_at: datetime
    updated_at: datetime

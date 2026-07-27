"""Progress request/response Pydantic schemas."""

from __future__ import annotations

import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.modules.progress.models import GoalStatus


class MeasurementCreate(BaseModel):
    recorded_at: date
    weight_kg: float | None = Field(default=None, gt=0, le=500)
    body_fat_pct: float | None = Field(default=None, ge=0, le=100)
    waist_cm: float | None = Field(default=None, gt=0, le=300)
    chest_cm: float | None = Field(default=None, gt=0, le=300)
    hips_cm: float | None = Field(default=None, gt=0, le=300)
    arm_cm: float | None = Field(default=None, gt=0, le=100)
    notes: str | None = Field(default=None, max_length=500)


class MeasurementUpdate(MeasurementCreate):
    """Full replace semantics — same shape as create."""


class MeasurementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    recorded_at: date
    weight_kg: float | None = None
    body_fat_pct: float | None = None
    waist_cm: float | None = None
    chest_cm: float | None = None
    hips_cm: float | None = None
    arm_cm: float | None = None
    notes: str | None = None
    created_at: datetime


class GoalCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    target_weight_kg: float | None = Field(default=None, gt=0, le=500)
    target_date: date | None = None


class GoalUpdate(GoalCreate):
    status: GoalStatus = GoalStatus.ACTIVE


class GoalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    target_weight_kg: float | None = None
    target_date: date | None = None
    status: GoalStatus
    created_at: datetime

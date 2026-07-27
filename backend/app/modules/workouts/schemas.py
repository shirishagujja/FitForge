"""Workout request/response Pydantic schemas."""

from __future__ import annotations

import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.modules.workouts.models import ExerciseCategory


class ExerciseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    category: ExerciseCategory
    muscle_group: str | None = None
    equipment: str | None = None


class WorkoutExerciseCreate(BaseModel):
    exercise_id: uuid.UUID
    sets: int = Field(gt=0, le=50)
    reps: int = Field(gt=0, le=1000)
    weight_kg: float | None = Field(default=None, ge=0)
    notes: str | None = Field(default=None, max_length=500)


class WorkoutExerciseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    exercise: ExerciseResponse
    order_index: int
    sets: int
    reps: int
    weight_kg: float | None = None
    notes: str | None = None


class WorkoutCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    performed_at: date
    notes: str | None = Field(default=None, max_length=2000)
    exercises: list[WorkoutExerciseCreate] = Field(default_factory=list)


class WorkoutUpdate(WorkoutCreate):
    """Full replace semantics — same shape as create."""


class WorkoutResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    performed_at: date
    notes: str | None = None
    created_at: datetime
    updated_at: datetime
    exercises: list[WorkoutExerciseResponse]


class WorkoutSummary(BaseModel):
    id: uuid.UUID
    name: str
    performed_at: date
    exercise_count: int

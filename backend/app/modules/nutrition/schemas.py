"""Nutrition request/response Pydantic schemas."""

from __future__ import annotations

import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class MealCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    logged_at: date
    calories: int = Field(ge=0, le=20000)
    protein_g: float | None = Field(default=None, ge=0)
    carbs_g: float | None = Field(default=None, ge=0)
    fat_g: float | None = Field(default=None, ge=0)
    notes: str | None = Field(default=None, max_length=500)


class MealUpdate(MealCreate):
    """Full replace semantics — same shape as create."""


class MealResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    logged_at: date
    calories: int
    protein_g: float | None = None
    carbs_g: float | None = None
    fat_g: float | None = None
    notes: str | None = None
    created_at: datetime


class WaterEntryCreate(BaseModel):
    logged_at: date
    amount_ml: int = Field(gt=0, le=5000)


class WaterEntryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    logged_at: date
    amount_ml: int
    created_at: datetime


class DailyNutritionSummary(BaseModel):
    date: date
    total_calories: int
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float
    total_water_ml: int

"""AI request/response Pydantic schemas."""

from __future__ import annotations

import uuid
from typing import Literal

from pydantic import BaseModel, Field


class GenerateWorkoutRequest(BaseModel):
    goal: str = Field(min_length=1, max_length=200)
    equipment: str | None = Field(default=None, max_length=200)
    duration_minutes: int = Field(default=45, ge=10, le=180)
    difficulty: Literal["beginner", "intermediate", "advanced"] = "intermediate"


class GeneratedExercise(BaseModel):
    exercise_name: str
    exercise_id: uuid.UUID | None = None
    sets: int
    reps: int
    notes: str | None = None


class GeneratedWorkoutResponse(BaseModel):
    name: str
    exercises: list[GeneratedExercise]


class LlmExercise(BaseModel):
    """LLM-facing shape: the model only knows exercise names, not our UUIDs."""

    exercise_name: str
    sets: int
    reps: int
    notes: str | None = None


class LlmWorkout(BaseModel):
    name: str
    exercises: list[LlmExercise]


class GenerateMealRequest(BaseModel):
    meal_type: str = Field(min_length=1, max_length=50)
    dietary_restrictions: str | None = Field(default=None, max_length=200)
    target_calories: int | None = Field(default=None, ge=0, le=3000)


class GeneratedMeal(BaseModel):
    name: str
    estimated_calories: int
    protein_g: float
    carbs_g: float
    fat_g: float


class GenerateMealResponse(BaseModel):
    suggestions: list[GeneratedMeal]


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=4000)


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_length=1, max_length=20)


class ChatResponse(BaseModel):
    message: str


class RecommendationsResponse(BaseModel):
    recommendations: list[str]

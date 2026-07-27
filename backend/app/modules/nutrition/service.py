"""Nutrition business logic: meals, water entries, daily summary."""

from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppException
from app.modules.auth.models import User
from app.modules.nutrition.models import Meal, WaterEntry
from app.modules.nutrition.schemas import (
    DailyNutritionSummary,
    MealCreate,
    MealResponse,
    MealUpdate,
    WaterEntryCreate,
    WaterEntryResponse,
)


async def create_meal(db: AsyncSession, user: User, payload: MealCreate) -> Meal:
    meal = Meal(
        user_id=user.id,
        name=payload.name,
        logged_at=payload.logged_at,
        calories=payload.calories,
        protein_g=payload.protein_g,
        carbs_g=payload.carbs_g,
        fat_g=payload.fat_g,
        notes=payload.notes,
    )
    db.add(meal)
    await db.flush()
    return meal


async def list_meals(
    db: AsyncSession,
    user: User,
    *,
    date_from: date | None = None,
    date_to: date | None = None,
) -> list[Meal]:
    stmt = (
        select(Meal)
        .where(Meal.user_id == user.id)
        .order_by(Meal.logged_at.desc(), Meal.created_at.desc())
    )
    if date_from is not None:
        stmt = stmt.where(Meal.logged_at >= date_from)
    if date_to is not None:
        stmt = stmt.where(Meal.logged_at <= date_to)
    result = await db.scalars(stmt)
    return list(result.all())


async def get_meal(db: AsyncSession, user: User, meal_id: uuid.UUID) -> Meal:
    meal = await db.get(Meal, meal_id)
    if meal is None or meal.user_id != user.id:
        raise AppException(code="NOT_FOUND", message="Meal not found", status_code=404)
    return meal


async def update_meal(
    db: AsyncSession, user: User, meal_id: uuid.UUID, payload: MealUpdate
) -> Meal:
    meal = await get_meal(db, user, meal_id)
    meal.name = payload.name
    meal.logged_at = payload.logged_at
    meal.calories = payload.calories
    meal.protein_g = payload.protein_g
    meal.carbs_g = payload.carbs_g
    meal.fat_g = payload.fat_g
    meal.notes = payload.notes
    await db.flush()
    return meal


async def delete_meal(db: AsyncSession, user: User, meal_id: uuid.UUID) -> None:
    meal = await get_meal(db, user, meal_id)
    await db.delete(meal)
    await db.flush()


async def create_water_entry(
    db: AsyncSession, user: User, payload: WaterEntryCreate
) -> WaterEntry:
    entry = WaterEntry(user_id=user.id, logged_at=payload.logged_at, amount_ml=payload.amount_ml)
    db.add(entry)
    await db.flush()
    return entry


async def list_water_entries(
    db: AsyncSession, user: User, *, logged_date: date | None = None
) -> list[WaterEntry]:
    stmt = (
        select(WaterEntry)
        .where(WaterEntry.user_id == user.id)
        .order_by(WaterEntry.created_at.desc())
    )
    if logged_date is not None:
        stmt = stmt.where(WaterEntry.logged_at == logged_date)
    result = await db.scalars(stmt)
    return list(result.all())


async def get_water_entry(db: AsyncSession, user: User, entry_id: uuid.UUID) -> WaterEntry:
    entry = await db.get(WaterEntry, entry_id)
    if entry is None or entry.user_id != user.id:
        raise AppException(code="NOT_FOUND", message="Water entry not found", status_code=404)
    return entry


async def delete_water_entry(db: AsyncSession, user: User, entry_id: uuid.UUID) -> None:
    entry = await get_water_entry(db, user, entry_id)
    await db.delete(entry)
    await db.flush()


async def get_daily_summary(
    db: AsyncSession, user: User, summary_date: date
) -> DailyNutritionSummary:
    meal_totals = (
        await db.execute(
            select(
                func.coalesce(func.sum(Meal.calories), 0),
                func.coalesce(func.sum(Meal.protein_g), 0.0),
                func.coalesce(func.sum(Meal.carbs_g), 0.0),
                func.coalesce(func.sum(Meal.fat_g), 0.0),
            ).where(Meal.user_id == user.id, Meal.logged_at == summary_date)
        )
    ).one()

    water_total = (
        await db.execute(
            select(func.coalesce(func.sum(WaterEntry.amount_ml), 0)).where(
                WaterEntry.user_id == user.id, WaterEntry.logged_at == summary_date
            )
        )
    ).scalar_one()

    return DailyNutritionSummary(
        date=summary_date,
        total_calories=int(meal_totals[0]),
        total_protein_g=float(meal_totals[1]),
        total_carbs_g=float(meal_totals[2]),
        total_fat_g=float(meal_totals[3]),
        total_water_ml=int(water_total),
    )


def to_meal_response(meal: Meal) -> MealResponse:
    return MealResponse.model_validate(meal)


def to_water_entry_response(entry: WaterEntry) -> WaterEntryResponse:
    return WaterEntryResponse.model_validate(entry)

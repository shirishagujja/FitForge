"""Nutrition & water HTTP routes."""

from __future__ import annotations

import uuid
from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db
from app.modules.auth.models import User
from app.modules.nutrition import service as nutrition_service
from app.modules.nutrition.schemas import MealCreate, MealUpdate, WaterEntryCreate

meals_router = APIRouter(prefix="/meals", tags=["nutrition"])
water_router = APIRouter(prefix="/water-entries", tags=["nutrition"])
nutrition_router = APIRouter(prefix="/nutrition", tags=["nutrition"])


@meals_router.post("", status_code=201)
async def create_meal(
    payload: MealCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    meal = await nutrition_service.create_meal(db, user, payload)
    return {"data": nutrition_service.to_meal_response(meal)}


@meals_router.get("")
async def list_meals(
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    meals = await nutrition_service.list_meals(db, user, date_from=date_from, date_to=date_to)
    return {"data": [nutrition_service.to_meal_response(m) for m in meals]}


@meals_router.get("/{meal_id}")
async def get_meal(
    meal_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    meal = await nutrition_service.get_meal(db, user, meal_id)
    return {"data": nutrition_service.to_meal_response(meal)}


@meals_router.put("/{meal_id}")
async def update_meal(
    meal_id: uuid.UUID,
    payload: MealUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    meal = await nutrition_service.update_meal(db, user, meal_id, payload)
    return {"data": nutrition_service.to_meal_response(meal)}


@meals_router.delete("/{meal_id}", status_code=204, response_model=None)
async def delete_meal(
    meal_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    await nutrition_service.delete_meal(db, user, meal_id)


@water_router.post("", status_code=201)
async def create_water_entry(
    payload: WaterEntryCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    entry = await nutrition_service.create_water_entry(db, user, payload)
    return {"data": nutrition_service.to_water_entry_response(entry)}


@water_router.get("")
async def list_water_entries(
    logged_date: date | None = Query(default=None, alias="date"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    entries = await nutrition_service.list_water_entries(db, user, logged_date=logged_date)
    return {"data": [nutrition_service.to_water_entry_response(e) for e in entries]}


@water_router.delete("/{entry_id}", status_code=204, response_model=None)
async def delete_water_entry(
    entry_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    await nutrition_service.delete_water_entry(db, user, entry_id)


@nutrition_router.get("/summary")
async def get_daily_summary(
    summary_date: date = Query(alias="date"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    summary = await nutrition_service.get_daily_summary(db, user, summary_date)
    return {"data": summary}

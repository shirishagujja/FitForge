"""Body measurement & goal HTTP routes."""

from __future__ import annotations

import uuid
from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db
from app.modules.auth.models import User
from app.modules.progress import service as progress_service
from app.modules.progress.schemas import (
    GoalCreate,
    GoalUpdate,
    MeasurementCreate,
    MeasurementUpdate,
)

measurements_router = APIRouter(prefix="/measurements", tags=["progress"])
goals_router = APIRouter(prefix="/goals", tags=["progress"])


@measurements_router.post("", status_code=201)
async def create_measurement(
    payload: MeasurementCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    measurement = await progress_service.create_measurement(db, user, payload)
    return {"data": progress_service.to_measurement_response(measurement)}


@measurements_router.get("")
async def list_measurements(
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    measurements = await progress_service.list_measurements(
        db, user, date_from=date_from, date_to=date_to
    )
    return {"data": [progress_service.to_measurement_response(m) for m in measurements]}


@measurements_router.get("/{measurement_id}")
async def get_measurement(
    measurement_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    measurement = await progress_service.get_measurement(db, user, measurement_id)
    return {"data": progress_service.to_measurement_response(measurement)}


@measurements_router.put("/{measurement_id}")
async def update_measurement(
    measurement_id: uuid.UUID,
    payload: MeasurementUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    measurement = await progress_service.update_measurement(db, user, measurement_id, payload)
    return {"data": progress_service.to_measurement_response(measurement)}


@measurements_router.delete("/{measurement_id}", status_code=204, response_model=None)
async def delete_measurement(
    measurement_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    await progress_service.delete_measurement(db, user, measurement_id)


@goals_router.post("", status_code=201)
async def create_goal(
    payload: GoalCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    goal = await progress_service.create_goal(db, user, payload)
    return {"data": progress_service.to_goal_response(goal)}


@goals_router.get("")
async def list_goals(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    goals = await progress_service.list_goals(db, user)
    return {"data": [progress_service.to_goal_response(g) for g in goals]}


@goals_router.put("/{goal_id}")
async def update_goal(
    goal_id: uuid.UUID,
    payload: GoalUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    goal = await progress_service.update_goal(db, user, goal_id, payload)
    return {"data": progress_service.to_goal_response(goal)}


@goals_router.delete("/{goal_id}", status_code=204, response_model=None)
async def delete_goal(
    goal_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    await progress_service.delete_goal(db, user, goal_id)

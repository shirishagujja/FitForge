"""Progress business logic: body measurements and goals."""

from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppException
from app.modules.auth.models import User
from app.modules.progress.models import BodyMeasurement, Goal
from app.modules.progress.schemas import (
    GoalCreate,
    GoalResponse,
    GoalUpdate,
    MeasurementCreate,
    MeasurementResponse,
    MeasurementUpdate,
)


def _apply_measurement_fields(measurement: BodyMeasurement, payload: MeasurementCreate) -> None:
    measurement.weight_kg = payload.weight_kg
    measurement.body_fat_pct = payload.body_fat_pct
    measurement.waist_cm = payload.waist_cm
    measurement.chest_cm = payload.chest_cm
    measurement.hips_cm = payload.hips_cm
    measurement.arm_cm = payload.arm_cm
    measurement.notes = payload.notes


async def create_measurement(
    db: AsyncSession, user: User, payload: MeasurementCreate
) -> BodyMeasurement:
    """Upsert: creating a measurement for a day that already has one updates it in place."""
    existing = await db.scalar(
        select(BodyMeasurement).where(
            BodyMeasurement.user_id == user.id,
            BodyMeasurement.recorded_at == payload.recorded_at,
        )
    )
    if existing is not None:
        _apply_measurement_fields(existing, payload)
        await db.flush()
        return existing

    measurement = BodyMeasurement(user_id=user.id, recorded_at=payload.recorded_at)
    _apply_measurement_fields(measurement, payload)
    db.add(measurement)
    await db.flush()
    return measurement


async def list_measurements(
    db: AsyncSession,
    user: User,
    *,
    date_from: date | None = None,
    date_to: date | None = None,
) -> list[BodyMeasurement]:
    stmt = (
        select(BodyMeasurement)
        .where(BodyMeasurement.user_id == user.id)
        .order_by(BodyMeasurement.recorded_at.desc())
    )
    if date_from is not None:
        stmt = stmt.where(BodyMeasurement.recorded_at >= date_from)
    if date_to is not None:
        stmt = stmt.where(BodyMeasurement.recorded_at <= date_to)
    result = await db.scalars(stmt)
    return list(result.all())


async def get_measurement(
    db: AsyncSession, user: User, measurement_id: uuid.UUID
) -> BodyMeasurement:
    measurement = await db.get(BodyMeasurement, measurement_id)
    if measurement is None or measurement.user_id != user.id:
        raise AppException(code="NOT_FOUND", message="Measurement not found", status_code=404)
    return measurement


async def update_measurement(
    db: AsyncSession,
    user: User,
    measurement_id: uuid.UUID,
    payload: MeasurementUpdate,
) -> BodyMeasurement:
    measurement = await get_measurement(db, user, measurement_id)
    measurement.recorded_at = payload.recorded_at
    _apply_measurement_fields(measurement, payload)
    await db.flush()
    return measurement


async def delete_measurement(db: AsyncSession, user: User, measurement_id: uuid.UUID) -> None:
    measurement = await get_measurement(db, user, measurement_id)
    await db.delete(measurement)
    await db.flush()


async def create_goal(db: AsyncSession, user: User, payload: GoalCreate) -> Goal:
    goal = Goal(
        user_id=user.id,
        title=payload.title,
        target_weight_kg=payload.target_weight_kg,
        target_date=payload.target_date,
    )
    db.add(goal)
    await db.flush()
    return goal


async def list_goals(db: AsyncSession, user: User) -> list[Goal]:
    stmt = select(Goal).where(Goal.user_id == user.id).order_by(Goal.created_at.desc())
    result = await db.scalars(stmt)
    return list(result.all())


async def get_goal(db: AsyncSession, user: User, goal_id: uuid.UUID) -> Goal:
    goal = await db.get(Goal, goal_id)
    if goal is None or goal.user_id != user.id:
        raise AppException(code="NOT_FOUND", message="Goal not found", status_code=404)
    return goal


async def update_goal(
    db: AsyncSession, user: User, goal_id: uuid.UUID, payload: GoalUpdate
) -> Goal:
    goal = await get_goal(db, user, goal_id)
    goal.title = payload.title
    goal.target_weight_kg = payload.target_weight_kg
    goal.target_date = payload.target_date
    goal.status = payload.status
    await db.flush()
    return goal


async def delete_goal(db: AsyncSession, user: User, goal_id: uuid.UUID) -> None:
    goal = await get_goal(db, user, goal_id)
    await db.delete(goal)
    await db.flush()


def to_measurement_response(measurement: BodyMeasurement) -> MeasurementResponse:
    return MeasurementResponse.model_validate(measurement)


def to_goal_response(goal: Goal) -> GoalResponse:
    return GoalResponse.model_validate(goal)

"""User profile ORM model."""

from __future__ import annotations

import enum
import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, Float, ForeignKey, String, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Sex(enum.StrEnum):
    MALE = "male"
    FEMALE = "female"
    UNSPECIFIED = "unspecified"


class ActivityLevel(enum.StrEnum):
    SEDENTARY = "sedentary"
    LIGHT = "light"
    MODERATE = "moderate"
    ACTIVE = "active"
    VERY_ACTIVE = "very_active"


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    display_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)
    sex: Mapped[Sex | None] = mapped_column(
        Enum(Sex, name="profile_sex", values_callable=lambda x: [e.value for e in x]),
        nullable=True,
    )
    height_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    fitness_goal: Mapped[str | None] = mapped_column(String(255), nullable=True)
    activity_level: Mapped[ActivityLevel | None] = mapped_column(
        Enum(
            ActivityLevel,
            name="profile_activity_level",
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

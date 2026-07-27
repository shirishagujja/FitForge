"""Create workout tables: exercises, workouts, workout_exercises. Seeds a starter exercise library.

Revision ID: 003_workouts
Revises: 002_email_password_tokens
Create Date: 2026-07-23
"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "003_workouts"
down_revision: str | None = "002_email_password_tokens"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

exercise_category = postgresql.ENUM(
    "strength", "cardio", "mobility", "other", name="exercise_category", create_type=False
)

SEED_EXERCISES = [
    ("Squat", "strength", "legs", "barbell"),
    ("Bench Press", "strength", "chest", "barbell"),
    ("Deadlift", "strength", "back", "barbell"),
    ("Overhead Press", "strength", "shoulders", "barbell"),
    ("Barbell Row", "strength", "back", "barbell"),
    ("Pull-up", "strength", "back", "bodyweight"),
    ("Push-up", "strength", "chest", "bodyweight"),
    ("Running", "cardio", "full_body", None),
    ("Cycling", "cardio", "legs", "bike"),
    ("Plank", "mobility", "core", "bodyweight"),
]


def upgrade() -> None:
    exercise_category.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "exercises",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("category", exercise_category, nullable=False),
        sa.Column("muscle_group", sa.String(length=100), nullable=True),
        sa.Column("equipment", sa.String(length=100), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index("ix_exercises_name", "exercises", ["name"], unique=False)

    op.create_table(
        "workouts",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("performed_at", sa.Date(), nullable=False),
        sa.Column("notes", sa.String(length=2000), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_workouts_user_id", "workouts", ["user_id"], unique=False)
    op.create_index("ix_workouts_performed_at", "workouts", ["performed_at"], unique=False)

    op.create_table(
        "workout_exercises",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("workout_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("exercise_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("sets", sa.Integer(), nullable=False),
        sa.Column("reps", sa.Integer(), nullable=False),
        sa.Column("weight_kg", sa.Float(), nullable=True),
        sa.Column("notes", sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(["workout_id"], ["workouts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["exercise_id"], ["exercises.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_workout_exercises_workout_id", "workout_exercises", ["workout_id"], unique=False
    )

    exercises_table = sa.table(
        "exercises",
        sa.column("name", sa.String),
        sa.column("category", exercise_category),
        sa.column("muscle_group", sa.String),
        sa.column("equipment", sa.String),
    )
    op.bulk_insert(
        exercises_table,
        [
            {
                "name": name,
                "category": category,
                "muscle_group": muscle_group,
                "equipment": equipment,
            }
            for name, category, muscle_group, equipment in SEED_EXERCISES
        ],
    )


def downgrade() -> None:
    op.drop_index("ix_workout_exercises_workout_id", table_name="workout_exercises")
    op.drop_table("workout_exercises")
    op.drop_index("ix_workouts_performed_at", table_name="workouts")
    op.drop_index("ix_workouts_user_id", table_name="workouts")
    op.drop_table("workouts")
    op.drop_index("ix_exercises_name", table_name="exercises")
    op.drop_table("exercises")
    exercise_category.drop(op.get_bind(), checkfirst=True)

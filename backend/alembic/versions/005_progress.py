"""Create progress tables: body_measurements, goals.

Revision ID: 005_progress
Revises: 004_nutrition
Create Date: 2026-07-23
"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "005_progress"
down_revision: str | None = "004_nutrition"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

goal_status = postgresql.ENUM(
    "active", "achieved", "abandoned", name="goal_status", create_type=False
)


def upgrade() -> None:
    goal_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "body_measurements",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("recorded_at", sa.Date(), nullable=False),
        sa.Column("weight_kg", sa.Float(), nullable=True),
        sa.Column("body_fat_pct", sa.Float(), nullable=True),
        sa.Column("waist_cm", sa.Float(), nullable=True),
        sa.Column("chest_cm", sa.Float(), nullable=True),
        sa.Column("hips_cm", sa.Float(), nullable=True),
        sa.Column("arm_cm", sa.Float(), nullable=True),
        sa.Column("notes", sa.String(length=500), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "recorded_at"),
    )
    op.create_index(
        "ix_body_measurements_user_id", "body_measurements", ["user_id"], unique=False
    )
    op.create_index(
        "ix_body_measurements_recorded_at", "body_measurements", ["recorded_at"], unique=False
    )

    op.create_table(
        "goals",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("target_weight_kg", sa.Float(), nullable=True),
        sa.Column("target_date", sa.Date(), nullable=True),
        sa.Column("status", goal_status, server_default="active", nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_goals_user_id", "goals", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_goals_user_id", table_name="goals")
    op.drop_table("goals")
    op.drop_index("ix_body_measurements_recorded_at", table_name="body_measurements")
    op.drop_index("ix_body_measurements_user_id", table_name="body_measurements")
    op.drop_table("body_measurements")
    goal_status.drop(op.get_bind(), checkfirst=True)

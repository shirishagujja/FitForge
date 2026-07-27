"""Create nutrition tables: meals, water_entries.

Revision ID: 004_nutrition
Revises: 003_workouts
Create Date: 2026-07-23
"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "004_nutrition"
down_revision: str | None = "003_workouts"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "meals",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("logged_at", sa.Date(), nullable=False),
        sa.Column("calories", sa.Integer(), nullable=False),
        sa.Column("protein_g", sa.Float(), nullable=True),
        sa.Column("carbs_g", sa.Float(), nullable=True),
        sa.Column("fat_g", sa.Float(), nullable=True),
        sa.Column("notes", sa.String(length=500), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_meals_user_id", "meals", ["user_id"], unique=False)
    op.create_index("ix_meals_logged_at", "meals", ["logged_at"], unique=False)

    op.create_table(
        "water_entries",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("logged_at", sa.Date(), nullable=False),
        sa.Column("amount_ml", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_water_entries_user_id", "water_entries", ["user_id"], unique=False)
    op.create_index("ix_water_entries_logged_at", "water_entries", ["logged_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_water_entries_logged_at", table_name="water_entries")
    op.drop_index("ix_water_entries_user_id", table_name="water_entries")
    op.drop_table("water_entries")
    op.drop_index("ix_meals_logged_at", table_name="meals")
    op.drop_index("ix_meals_user_id", table_name="meals")
    op.drop_table("meals")

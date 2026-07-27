"""Create profiles table.

Revision ID: 006_profile
Revises: 005_progress
Create Date: 2026-07-24
"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "006_profile"
down_revision: str | None = "005_progress"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

profile_sex = postgresql.ENUM(
    "male", "female", "unspecified", name="profile_sex", create_type=False
)
profile_activity_level = postgresql.ENUM(
    "sedentary",
    "light",
    "moderate",
    "active",
    "very_active",
    name="profile_activity_level",
    create_type=False,
)


def upgrade() -> None:
    profile_sex.create(op.get_bind(), checkfirst=True)
    profile_activity_level.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "profiles",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("display_name", sa.String(length=100), nullable=True),
        sa.Column("date_of_birth", sa.Date(), nullable=True),
        sa.Column("sex", profile_sex, nullable=True),
        sa.Column("height_cm", sa.Float(), nullable=True),
        sa.Column("fitness_goal", sa.String(length=255), nullable=True),
        sa.Column("activity_level", profile_activity_level, nullable=True),
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
        sa.UniqueConstraint("user_id"),
    )


def downgrade() -> None:
    op.drop_table("profiles")
    profile_activity_level.drop(op.get_bind(), checkfirst=True)
    profile_sex.drop(op.get_bind(), checkfirst=True)

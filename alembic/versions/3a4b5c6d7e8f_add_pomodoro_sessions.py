"""add_pomodoro_sessions

Revision ID: 3a4b5c6d7e8f
Revises: 2f351a9243f5
Create Date: 2026-01-16 10:00:00.000000

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = "3a4b5c6d7e8f"
down_revision: Union[str, None] = "2f351a9243f5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "pomodoro_sessions",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False,
            index=True,
        ),
        sa.Column("focus_count", sa.Integer(), default=0),
        sa.Column("focus_time", sa.Integer(), default=0),
        sa.Column("break_time", sa.Integer(), default=0),
        sa.Column("long_break_time", sa.Integer(), default=0),
        sa.Column("status", sa.String(50), default="completed"),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("pomodoro_sessions")

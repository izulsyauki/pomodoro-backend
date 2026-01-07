"""initial user table

Revision ID: 001_initial
Revises:
Create Date: 2026-01-07

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), unique=True, nullable=False, index=True),
        sa.Column("username", sa.String(100), unique=True, nullable=False, index=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=True),
        sa.Column("avatar_url", sa.String(500), nullable=True),
        sa.Column("role", sa.String(20), nullable=False, server_default="user"),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("is_verified", sa.Boolean(), default=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("users")

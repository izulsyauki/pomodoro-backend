"""adding_table_quotes

Revision ID: 2f351a9243f5
Revises: 001_initial
Create Date: 2026-01-15 15:59:18.408523

"""

from typing import Sequence, Union
from sqlalchemy.dialects.postgresql import UUID
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2f351a9243f5"
down_revision: Union[str, None] = "001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "quotes",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("content", sa.String(255), unique=True, nullable=False, index=True),
        sa.Column("author", sa.String(255), nullable=True),
        sa.Column(
            "created_by", UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True
        ),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("quotes")

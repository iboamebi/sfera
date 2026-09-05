"""fix site timestamp defaults

Revision ID: 0c9e8a7b6d5f
Revises: f1a2b3c4d5e6
Create Date: 2026-09-05

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op


revision: str = "0c9e8a7b6d5f"
down_revision: str | None = "f1a2b3c4d5e6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add database defaults for Site timestamps."""
    op.alter_column(
        "sites",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        server_default=sa.text("now()"),
        existing_nullable=False,
    )
    op.alter_column(
        "sites",
        "updated_at",
        existing_type=sa.DateTime(timezone=True),
        server_default=sa.text("now()"),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Remove database defaults from Site timestamps."""
    op.alter_column(
        "sites",
        "updated_at",
        existing_type=sa.DateTime(timezone=True),
        server_default=None,
        existing_nullable=False,
    )
    op.alter_column(
        "sites",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        server_default=None,
        existing_nullable=False,
    )

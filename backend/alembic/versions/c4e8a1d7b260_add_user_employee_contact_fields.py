"""Add employee contact fields to users.

Revision ID: c4e8a1d7b260
Revises: 9f2a6c4d8e14
Create Date: 2026-11-15
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "c4e8a1d7b260"
down_revision: str | Sequence[str] | None = "9f2a6c4d8e14"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add optional phone and job position to employee accounts."""
    op.add_column("users", sa.Column("phone", sa.String(length=50), nullable=True))
    op.add_column(
        "users",
        sa.Column("position", sa.String(length=255), nullable=True),
    )


def downgrade() -> None:
    """Remove employee contact fields."""
    op.drop_column("users", "position")
    op.drop_column("users", "phone")

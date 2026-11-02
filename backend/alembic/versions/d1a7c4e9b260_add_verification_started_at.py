"""add verification start timestamp

Revision ID: d1a7c4e9b260
Revises: a7c9e2f4b610
Create Date: 2026-11-02

"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "d1a7c4e9b260"
down_revision: str | None = "a7c9e2f4b610"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add the timestamp of the actual start of verification."""
    op.add_column(
        "verifications",
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    """Remove the verification start timestamp."""
    op.drop_column("verifications", "started_at")

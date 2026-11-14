"""Add cancelled verification state and cancellation reason.

Revision ID: f7c2a9e4b610
Revises: d4e8a1c6f230
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "f7c2a9e4b610"
down_revision: str | None = "d4e8a1c6f230"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add the cancellation status and its optional reason."""
    op.execute("ALTER TYPE verification_status ADD VALUE IF NOT EXISTS 'CANCELLED'")
    op.add_column(
        "verifications",
        sa.Column("cancellation_reason", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    """Remove the cancellation reason column.

    PostgreSQL enum values cannot be removed without recreating the enum type.
    """
    op.drop_column("verifications", "cancellation_reason")

"""Make Customer and new Order Organization optional.

Revision ID: 9f2a6c4d8e11
Revises: 9f2a6c4d8e10
Create Date: 2026-11-05

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "9f2a6c4d8e11"
down_revision: str | None = "9f2a6c4d8e10"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Allow Customer and new Orders to exist without an Organization."""
    op.alter_column(
        "customers",
        "organization_id",
        existing_type=sa.UUID(),
        nullable=True,
    )
    op.alter_column(
        "orders",
        "organization_id",
        existing_type=sa.UUID(),
        nullable=True,
    )


def downgrade() -> None:
    """Restore the previous non-null Organization requirement."""
    op.alter_column(
        "orders",
        "organization_id",
        existing_type=sa.UUID(),
        nullable=False,
    )
    op.alter_column(
        "customers",
        "organization_id",
        existing_type=sa.UUID(),
        nullable=False,
    )

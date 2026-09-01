"""allow null audit entity id

Revision ID: 7c1d4e8f2a90
Revises: 5b7c9e2a1f40
Create Date: 2026-09-01

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "7c1d4e8f2a90"
down_revision: str = "5b7c9e2a1f40"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Allow audit records without an entity identifier."""
    op.alter_column(
        "audit_records",
        "entity_id",
        existing_type=sa.UUID(),
        nullable=True,
    )


def downgrade() -> None:
    """Restore the required audit entity identifier."""
    op.alter_column(
        "audit_records",
        "entity_id",
        existing_type=sa.UUID(),
        nullable=False,
    )

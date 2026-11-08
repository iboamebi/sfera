"""remove duplicate factory number from instruments

Revision ID: 9b1c7d4e2f30
Revises: 8a4d2f6b1c90
Create Date: 2026-08-31

"""
from collections.abc import Sequence

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "9b1c7d4e2f30"
down_revision: str | Sequence[str] | None = "8a4d2f6b1c90"
branch_labels: str | Sequence[str] | None = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Remove the duplicate factory number column."""
    op.drop_column("instruments", "factory_number")


def downgrade() -> None:
    """Restore the legacy duplicate factory number column."""
    import sqlalchemy as sa

    op.add_column(
        "instruments",
        sa.Column("factory_number", sa.String(length=100), nullable=True),
    )

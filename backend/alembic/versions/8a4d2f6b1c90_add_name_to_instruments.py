"""add name to instruments

Revision ID: 8a4d2f6b1c90
Revises: 7c2f1a9e4b60
Create Date: 2026-08-31

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8a4d2f6b1c90"
down_revision: Union[str, Sequence[str], None] = "7c2f1a9e4b60"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add the individual instrument name to instrument cards."""
    op.add_column(
        "instruments",
        sa.Column("name", sa.String(length=255), nullable=True),
    )


def downgrade() -> None:
    """Remove the individual instrument name from instrument cards."""
    op.drop_column("instruments", "name")

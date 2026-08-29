"""add instrument type to order items

Revision ID: 7c2f1a9e4b60
Revises: 4d7a9c2e1f30
Create Date: 2026-08-30

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7c2f1a9e4b60"
down_revision: Union[str, Sequence[str], None] = "4d7a9c2e1f30"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add an optional instrument type reference to order items."""
    op.add_column(
        "order_items",
        sa.Column("instrument_type_id", sa.UUID(), nullable=True),
    )
    op.create_foreign_key(
        "order_items_instrument_type_id_fkey",
        "order_items",
        "instrument_types",
        ["instrument_type_id"],
        ["id"],
    )


def downgrade() -> None:
    """Remove the instrument type reference from order items."""
    op.drop_constraint(
        "order_items_instrument_type_id_fkey",
        "order_items",
        type_="foreignkey",
    )
    op.drop_column("order_items", "instrument_type_id")

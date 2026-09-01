"""add quantity to order items

Revision ID: 9f4c2b7a1d60
Revises: 8e2f6a1b3c40
Create Date: 2026-09-02

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "9f4c2b7a1d60"
down_revision: str = "8e2f6a1b3c40"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add quantity to order items with a default of one."""
    op.add_column(
        "order_items",
        sa.Column(
            "quantity",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("1"),
        ),
    )
    op.alter_column(
        "order_items",
        "quantity",
        server_default=None,
    )


def downgrade() -> None:
    """Remove quantity from order items."""
    op.drop_column("order_items", "quantity")

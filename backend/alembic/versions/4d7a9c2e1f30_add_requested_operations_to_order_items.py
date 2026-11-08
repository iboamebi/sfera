"""add requested operations to order items

Revision ID: 4d7a9c2e1f30
Revises: 071a88b4b6da
Create Date: 2026-08-29

"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "4d7a9c2e1f30"
down_revision: str | tuple[str, ...] | None = "071a88b4b6da"
branch_labels: str | tuple[str, ...] | None = None
depends_on: str | tuple[str, ...] | None = None


def upgrade() -> None:
    """Add the requested operations collection to order items."""
    op.add_column(
        "order_items",
        sa.Column(
            "requested_operations",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'[]'"),
        ),
    )


def downgrade() -> None:
    """Remove the requested operations collection from order items."""
    op.drop_column("order_items", "requested_operations")

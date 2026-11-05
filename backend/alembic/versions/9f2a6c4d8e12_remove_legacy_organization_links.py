"""Remove legacy Customer and Order Organization links.

Revision ID: 9f2a6c4d8e12
Revises: 9f2a6c4d8e11
Create Date: 2026-11-05

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "9f2a6c4d8e12"
down_revision: str | None = "9f2a6c4d8e11"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Remove legacy Organization links from Customer and Order."""
    op.drop_constraint(
        "customers_organization_id_fkey",
        "customers",
        type_="foreignkey",
    )
    op.drop_column("customers", "organization_id")

    op.drop_constraint(
        "orders_organization_id_fkey",
        "orders",
        type_="foreignkey",
    )
    op.drop_column("orders", "organization_id")


def downgrade() -> None:
    """Restore legacy Organization links as nullable columns."""
    op.add_column(
        "orders",
        sa.Column("organization_id", sa.UUID(), nullable=True),
    )
    op.create_foreign_key(
        "orders_organization_id_fkey",
        "orders",
        "organizations",
        ["organization_id"],
        ["id"],
    )

    op.add_column(
        "customers",
        sa.Column("organization_id", sa.UUID(), nullable=True),
    )
    op.create_foreign_key(
        "customers_organization_id_fkey",
        "customers",
        "organizations",
        ["organization_id"],
        ["id"],
    )

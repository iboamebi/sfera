"""Remove legacy Order Site link.

Revision ID: c2e5f7a9b310
Revises: b1d4e7f9a260
Create Date: 2026-11-07
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "c2e5f7a9b310"
down_revision: str | None = "b1d4e7f9a260"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _ensure_order_site_link_is_unused() -> None:
    """Reject removal while legacy Order Site data still exists."""
    count = (
        op.get_bind()
        .execute(
            sa.text("SELECT count(*) FROM orders WHERE site_id IS NOT NULL"),
        )
        .scalar_one()
    )

    if count:
        raise RuntimeError(
            "Cannot remove legacy Order Site link automatically: "
            f"{count} Order row(s) still have site_id. Clear the obsolete "
            "Order Site assignments before applying this migration.",
        )


def upgrade() -> None:
    """Remove the obsolete persistent Order Site link."""
    _ensure_order_site_link_is_unused()
    op.drop_column("orders", "site_id")


def downgrade() -> None:
    """Restore the legacy nullable Order Site link."""
    op.add_column(
        "orders",
        sa.Column("site_id", sa.UUID(), nullable=True),
    )
    op.create_foreign_key(
        "orders_site_id_fkey",
        "orders",
        "sites",
        ["site_id"],
        ["id"],
    )

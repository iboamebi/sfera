"""Move Site ownership from Organization to Customer.

Revision ID: 9f2a6c4d8e13
Revises: 9f2a6c4d8e12
Create Date: 2026-11-05

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "9f2a6c4d8e13"
down_revision: str | None = "9f2a6c4d8e12"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _ensure_sites_empty() -> None:
    """Reject an unsafe ownership migration when Site rows already exist."""
    site_count = (
        op.get_bind()
        .execute(
            sa.text("SELECT count(*) FROM sites"),
        )
        .scalar_one()
    )

    if site_count:
        raise RuntimeError(
            "Cannot change Site ownership automatically: "
            f"{site_count} Site row(s) exist. Assign each Site to a Customer "
            "before applying this migration.",
        )


def upgrade() -> None:
    """Replace Site Organization ownership with Customer ownership."""
    _ensure_sites_empty()

    op.drop_constraint(
        "sites_organization_id_fkey",
        "sites",
        type_="foreignkey",
    )
    op.drop_column("sites", "organization_id")

    op.add_column(
        "sites",
        sa.Column("customer_id", sa.UUID(), nullable=False),
    )
    op.create_foreign_key(
        "sites_customer_id_fkey",
        "sites",
        "customers",
        ["customer_id"],
        ["id"],
    )


def downgrade() -> None:
    """Restore the previous Site Organization ownership structure."""
    _ensure_sites_empty()

    op.drop_constraint(
        "sites_customer_id_fkey",
        "sites",
        type_="foreignkey",
    )
    op.drop_column("sites", "customer_id")

    op.add_column(
        "sites",
        sa.Column("organization_id", sa.UUID(), nullable=False),
    )
    op.create_foreign_key(
        "sites_organization_id_fkey",
        "sites",
        "organizations",
        ["organization_id"],
        ["id"],
    )

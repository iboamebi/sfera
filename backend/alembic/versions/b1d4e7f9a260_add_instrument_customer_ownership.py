"""Add Customer ownership to instruments.

Revision ID: b1d4e7f9a260
Revises: a6c8e1f3b520
Create Date: 2026-11-07
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "b1d4e7f9a260"
down_revision: str | None = "a6c8e1f3b520"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _ensure_instruments_empty() -> None:
    """Reject ownership migration when Instrument rows already exist."""
    instrument_count = (
        op.get_bind()
        .execute(
            sa.text("SELECT count(*) FROM instruments"),
        )
        .scalar_one()
    )

    if instrument_count:
        raise RuntimeError(
            "Cannot add mandatory Instrument Customer ownership automatically: "
            f"{instrument_count} Instrument row(s) exist. Assign each Instrument "
            "to a Customer before applying this migration.",
        )


def upgrade() -> None:
    """Add mandatory Customer ownership and enforce Site ownership consistency."""
    _ensure_instruments_empty()

    op.create_unique_constraint(
        "uq_sites_id_customer_id",
        "sites",
        ["id", "customer_id"],
    )

    op.add_column(
        "instruments",
        sa.Column("customer_id", sa.UUID(), nullable=False),
    )

    op.create_foreign_key(
        "instruments_customer_id_fkey",
        "instruments",
        "customers",
        ["customer_id"],
        ["id"],
    )

    op.drop_constraint(
        "fk_instruments_site_id_sites",
        "instruments",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "instruments_site_customer_fkey",
        "instruments",
        "sites",
        ["site_id", "customer_id"],
        ["id", "customer_id"],
    )


def downgrade() -> None:
    """Restore the previous Instrument Site-only ownership structure."""
    _ensure_instruments_empty()

    op.drop_constraint(
        "instruments_site_customer_fkey",
        "instruments",
        type_="foreignkey",
    )

    op.drop_constraint(
        "instruments_customer_id_fkey",
        "instruments",
        type_="foreignkey",
    )

    op.drop_column("instruments", "customer_id")

    op.create_foreign_key(
        "fk_instruments_site_id_sites",
        "instruments",
        "sites",
        ["site_id"],
        ["id"],
    )

    op.drop_constraint(
        "uq_sites_id_customer_id",
        "sites",
        type_="unique",
    )

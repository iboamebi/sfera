"""refactor: migrate price list item to ddd model

Revision ID: 22ae78ebd152
Revises: c5ce4959d90d
Create Date: 2026-08-01 17:57:02.651281

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "22ae78ebd152"
down_revision: str | Sequence[str] | None = "c5ce4959d90d"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "price_list_items",
        sa.Column(
            "service_code",
            sa.String(length=100),
            nullable=True,
        ),
    )

    op.add_column(
        "price_list_items",
        sa.Column(
            "price",
            sa.Numeric(precision=12, scale=2),
            nullable=True,
        ),
    )

    op.add_column(
        "price_list_items",
        sa.Column(
            "unit",
            sa.String(length=50),
            nullable=True,
        ),
    )

    op.add_column(
        "price_list_items",
        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
        ),
    )

    op.execute(
        """
        UPDATE price_list_items
        SET
            price = unit_price,
            service_code = COALESCE(service_type, 'UNKNOWN'),
            unit = 'pcs'
        """
    )

    op.alter_column(
        "price_list_items",
        "service_code",
        nullable=False,
    )

    op.alter_column(
        "price_list_items",
        "price",
        nullable=False,
    )

    op.alter_column(
        "price_list_items",
        "unit",
        nullable=False,
    )

    op.drop_column(
        "price_list_items",
        "unit_price",
    )

    op.drop_column(
        "price_list_items",
        "service_type",
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.add_column(
        "price_list_items",
        sa.Column(
            "service_type",
            sa.String(length=100),
            nullable=True,
        ),
    )

    op.add_column(
        "price_list_items",
        sa.Column(
            "unit_price",
            sa.Numeric(precision=12, scale=2),
            nullable=True,
        ),
    )

    op.execute(
        """
        UPDATE price_list_items
        SET
            unit_price = price,
            service_type = service_code
        """
    )

    op.alter_column(
        "price_list_items",
        "unit_price",
        nullable=False,
    )

    op.drop_column(
        "price_list_items",
        "description",
    )

    op.drop_column(
        "price_list_items",
        "unit",
    )

    op.drop_column(
        "price_list_items",
        "price",
    )

    op.drop_column(
        "price_list_items",
        "service_code",
    )

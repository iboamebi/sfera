"""add customer organization and site links

Revision ID: 1d3e5f7a9b20
Revises: 0c9e8a7b6d5f
Create Date: 2026-09-05

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "1d3e5f7a9b20"
down_revision: str | None = "0c9e8a7b6d5f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add organization and site links for customers, orders, and instruments."""
    op.create_table(
        "customer_organizations",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("customer_id", sa.UUID(), nullable=False),
        sa.Column("organization_id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "archived",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"]),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "customer_id",
            "organization_id",
            name="uq_customer_organizations_customer_organization",
        ),
    )

    op.execute(
        sa.text(
            """
            INSERT INTO customer_organizations (
                id,
                customer_id,
                organization_id
            )
            SELECT
                gen_random_uuid(),
                c.id,
                c.organization_id
            FROM customers AS c
            """
        )
    )

    op.add_column(
        "orders",
        sa.Column("organization_id", sa.UUID(), nullable=True),
    )
    op.execute(
        sa.text(
            """
            UPDATE orders AS o
            SET organization_id = c.organization_id
            FROM customers AS c
            WHERE c.id = o.customer_id
            """
        )
    )
    op.alter_column(
        "orders",
        "organization_id",
        existing_type=sa.UUID(),
        nullable=False,
    )
    op.create_foreign_key(
        "fk_orders_organization_id_organizations",
        "orders",
        "organizations",
        ["organization_id"],
        ["id"],
    )

    op.add_column(
        "orders",
        sa.Column("site_id", sa.UUID(), nullable=True),
    )
    op.create_foreign_key(
        "fk_orders_site_id_sites",
        "orders",
        "sites",
        ["site_id"],
        ["id"],
    )

    op.add_column(
        "instruments",
        sa.Column("site_id", sa.UUID(), nullable=True),
    )
    op.create_foreign_key(
        "fk_instruments_site_id_sites",
        "instruments",
        "sites",
        ["site_id"],
        ["id"],
    )


def downgrade() -> None:
    """Remove organization and site links."""
    op.drop_constraint(
        "fk_instruments_site_id_sites",
        "instruments",
        type_="foreignkey",
    )
    op.drop_column("instruments", "site_id")

    op.drop_constraint(
        "fk_orders_site_id_sites",
        "orders",
        type_="foreignkey",
    )
    op.drop_column("orders", "site_id")

    op.drop_constraint(
        "fk_orders_organization_id_organizations",
        "orders",
        type_="foreignkey",
    )
    op.drop_column("orders", "organization_id")

    op.drop_table("customer_organizations")

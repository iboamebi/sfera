"""Remove the obsolete Customer–Organization association.

Revision ID: 9f2a6c4d8e14
Revises: 9f2a6c4d8e13
Create Date: 2026-11-05
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "9f2a6c4d8e14"
down_revision: str | None = "9f2a6c4d8e13"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Drop untrusted Customer–Organization links; preserve Organization rows."""
    op.drop_table("customer_organizations")


def downgrade() -> None:
    """Recreate an empty association table; deleted links are not recoverable."""
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

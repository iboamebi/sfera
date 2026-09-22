"""add verification type to verifications

Revision ID: 8d4f6a1b2c30
Revises: f3a8c1d9e720
Create Date: 2026-09-22

"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "8d4f6a1b2c30"
down_revision: str | None = "f3a8c1d9e720"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


verification_type_enum = postgresql.ENUM(
    "PRIMARY",
    "PERIODIC",
    "AFTER_REPAIR",
    name="verification_type",
)


def upgrade() -> None:
    """Persist the required verification type."""
    verification_type_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "verifications",
        sa.Column(
            "verification_type",
            verification_type_enum,
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Remove the persisted verification type."""
    op.drop_column("verifications", "verification_type")
    verification_type_enum.drop(op.get_bind(), checkfirst=True)

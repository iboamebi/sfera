"""prepare verification lifecycle persistence

Revision ID: f3a8c1d9e720
Revises: e2d7f4a9c130
Create Date: 2026-09-13

"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "f3a8c1d9e720"
down_revision: str | None = "e2d7f4a9c130"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


verification_status_enum = postgresql.ENUM(
    "CREATED",
    "IN_PROGRESS",
    "DECIDED",
    name="verification_status",
)


def upgrade() -> None:
    """Prepare persistence for the verification lifecycle model."""
    verification_status_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "verifications",
        sa.Column("status", verification_status_enum, nullable=True),
    )
    op.add_column(
        "verifications",
        sa.Column("decision_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.execute(
        sa.text(
            """
            UPDATE verifications
            SET status = 'DECIDED',
                decision_at = verification_date::timestamp with time zone
            """
        )
    )

    op.alter_column(
        "verifications",
        "status",
        existing_type=verification_status_enum,
        nullable=False,
    )
    op.alter_column(
        "verifications",
        "result",
        existing_nullable=False,
        nullable=True,
    )


def downgrade() -> None:
    """Restore the previous verification result persistence contract."""
    op.alter_column(
        "verifications",
        "result",
        existing_nullable=True,
        nullable=False,
    )
    op.drop_column("verifications", "decision_at")
    op.drop_column("verifications", "status")
    verification_status_enum.drop(op.get_bind(), checkfirst=True)

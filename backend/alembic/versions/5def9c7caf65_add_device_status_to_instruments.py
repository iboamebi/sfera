"""
add device status to instruments

Revision ID: 5def9c7caf65
Revises: 22ae78ebd152
Create Date: 2026-08-02
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5def9c7caf65"
down_revision: str | Sequence[str] | None = "22ae78ebd152"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add device status column."""

    op.add_column(
        "instruments",
        sa.Column(
            "device_status",
            sa.String(length=50),
            nullable=False,
            server_default="AVAILABLE",
        ),
    )

    op.alter_column(
        "instruments",
        "device_status",
        server_default=None,
    )


def downgrade() -> None:
    """Remove device status column."""

    op.drop_column(
        "instruments",
        "device_status",
    )

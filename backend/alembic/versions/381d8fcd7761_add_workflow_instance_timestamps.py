"""add workflow instance timestamps

Revision ID: 381d8fcd7761
Revises: 9a1ddec34200
Create Date: 2026-08-23
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "381d8fcd7761"
down_revision: str | Sequence[str] | None = "9a1ddec34200"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "workflow_instances",
        sa.Column(
            "started_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )
    op.add_column(
        "workflow_instances",
        sa.Column(
            "completed_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("workflow_instances", "completed_at")
    op.drop_column("workflow_instances", "started_at")

"""remove obsolete arshin export flags

Revision ID: c5ce4959d90d
Revises: 9a1ddec34200
Create Date: 2026-07-24

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c5ce4959d90d"
down_revision: str | Sequence[str] | None = "9a1ddec34200"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Remove obsolete Arshin export flags."""
    op.drop_column(
        "verifications",
        "export_to_arshin",
    )
    op.drop_column(
        "verifications",
        "exported_to_arshin",
    )


def downgrade() -> None:
    """Restore obsolete Arshin export flags."""
    op.add_column(
        "verifications",
        sa.Column(
            "export_to_arshin",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )
    op.add_column(
        "verifications",
        sa.Column(
            "exported_to_arshin",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

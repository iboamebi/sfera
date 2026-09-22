"""merge alembic heads

Revision ID: a7c9e2f4b610
Revises: 1d3e5f7a9b20, 8d4f6a1b2c30
Create Date: 2026-09-22

"""

from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "a7c9e2f4b610"
down_revision: tuple[str, str] = (
    "1d3e5f7a9b20",
    "8d4f6a1b2c30",
)
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Merge the active Alembic heads."""
    pass


def downgrade() -> None:
    """Restore the two migration branches."""
    pass

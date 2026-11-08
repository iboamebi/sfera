"""merge workflow and auth migration heads

Revision ID: 071a88b4b6da
Revises: 381d8fcd7761, d1f7a8c9e2b4
Create Date: 2026-08-23 20:46:48.796760

"""

from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "071a88b4b6da"
down_revision: tuple[str, str] = ("381d8fcd7761", "d1f7a8c9e2b4")
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

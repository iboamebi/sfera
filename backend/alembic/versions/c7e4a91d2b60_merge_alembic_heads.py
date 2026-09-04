"""merge alembic heads

Revision ID: c7e4a91d2b60
Revises: 9b1c7d4e2f30, c5ce4959d90d, b6c1e8f3a420
Create Date: 2026-09-04

"""
from collections.abc import Sequence


revision: str = "c7e4a91d2b60"
down_revision: tuple[str, str, str] = (
    "9b1c7d4e2f30",
    "c5ce4959d90d",
    "b6c1e8f3a420",
)
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Merge existing Alembic heads."""
    pass


def downgrade() -> None:
    """Restore the three migration branches."""
    pass

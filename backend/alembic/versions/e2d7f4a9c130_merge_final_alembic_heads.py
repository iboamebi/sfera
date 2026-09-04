"""merge final alembic heads

Revision ID: e2d7f4a9c130
Revises: 9f4c2b7a1d60, c7e4a91d2b60
Create Date: 2026-09-04

"""
from collections.abc import Sequence


revision: str = "e2d7f4a9c130"
down_revision: tuple[str, str] = (
    "9f4c2b7a1d60",
    "c7e4a91d2b60",
)
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Merge final Alembic heads."""
    pass


def downgrade() -> None:
    """Restore the two migration branches."""
    pass

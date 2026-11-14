"""merge alembic heads

Revision ID: c7e4a91d2b60
Revises: 9b1c7d4e2f30, b6c1e8f3a420
Create Date: 2026-09-04

"""

revision: str = "c7e4a91d2b60"
down_revision: tuple[str, str] = (
    "9b1c7d4e2f30",
    "b6c1e8f3a420",
)
branch_labels: str | tuple[str, ...] | None = None
depends_on: str | tuple[str, ...] | None = None


def upgrade() -> None:
    """Merge existing Alembic heads."""
    pass


def downgrade() -> None:
    """Restore the two migration branches."""
    pass

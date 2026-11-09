"""merge user password and verification lifecycle migrations

Revision ID: 4c9e2a7b1d60
Revises: 3b8e1a6d4f20, d1a7c4e9b260
Create Date: 2026-11-02

"""

revision: str = "4c9e2a7b1d60"
down_revision: tuple[str, str] = (
    "3b8e1a6d4f20",
    "d1a7c4e9b260",
)
branch_labels: str | tuple[str, ...] | None = None
depends_on: str | tuple[str, ...] | None = None


def upgrade() -> None:
    """Merge user and verification migration branches."""
    pass


def downgrade() -> None:
    """Restore the two migration branches."""
    pass

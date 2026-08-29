"""Retire the legacy audit log table.

Revision ID: 6f4b8e1c2d90
Revises: 071a88b4b6da
Create Date: 2026-08-29

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6f4b8e1c2d90"
down_revision: str | Sequence[str] | None = "071a88b4b6da"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Rename the obsolete audit table while preserving historical rows."""
    op.rename_table("audit_logs", "legacy_audit_logs")


def downgrade() -> None:
    """Restore the legacy audit table name."""
    op.rename_table("legacy_audit_logs", "audit_logs")

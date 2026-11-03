"""allow audit records without a direct entity identifier

Revision ID: c4d8a2f19b70
Revises: a7c9e2f4b610
Create Date: 2026-11-03

"""

from collections.abc import Sequence

from alembic import op

revision: str = "c4d8a2f19b70"
down_revision: str | Sequence[str] | None = "a7c9e2f4b610"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Align the database constraint with the nullable AuditRecord contract."""
    op.alter_column(
        "audit_records",
        "entity_id",
        existing_type=None,
        nullable=True,
    )


def downgrade() -> None:
    """Restore the previous non-null constraint."""
    op.alter_column(
        "audit_records",
        "entity_id",
        existing_type=None,
        nullable=False,
    )

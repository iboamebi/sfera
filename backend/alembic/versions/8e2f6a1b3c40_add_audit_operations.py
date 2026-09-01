"""add audit operations

Revision ID: 8e2f6a1b3c40
Revises: 7c1d4e8f2a90
Create Date: 2026-09-01

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "8e2f6a1b3c40"
down_revision: str = "7c1d4e8f2a90"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create audit operations and link audit records to them."""
    op.create_table(
        "audit_operations",
        sa.Column("operation_id", sa.UUID(), nullable=False),
        sa.Column("initiated_by", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("operation_id"),
    )
    op.create_index(
        "ix_audit_operations_initiated_by",
        "audit_operations",
        ["initiated_by"],
    )
    op.create_foreign_key(
        "fk_audit_records_operation_id_audit_operations",
        "audit_records",
        "audit_operations",
        ["operation_id"],
        ["operation_id"],
    )


def downgrade() -> None:
    """Remove the audit operation relationship and table."""
    op.drop_constraint(
        "fk_audit_records_operation_id_audit_operations",
        "audit_records",
        type_="foreignkey",
    )
    op.drop_index(
        "ix_audit_operations_initiated_by",
        table_name="audit_operations",
    )
    op.drop_table("audit_operations")

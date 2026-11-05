"""Reset untrusted business data while preserving Organizations and alex admin.

Revision ID: a6c8e1f3b520
Revises: 9f2a6c4d8e14
Create Date: 2026-11-05

This is a one-time initialization cleanup. It is intentionally irreversible.
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "a6c8e1f3b520"
down_revision: str | None = "9f2a6c4d8e14"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Remove all existing business/master data except legal entities and RBAC."""
    bind = op.get_bind()
    alex_count = bind.execute(
        sa.text(
            "SELECT count(*) FROM users "
            "WHERE username = 'alex' AND role = 'admin'"
        )
    ).scalar_one()

    if alex_count != 1:
        raise RuntimeError(
            "Refusing destructive reset: expected exactly one users row "
            "with username='alex' and role='admin'."
        )

    # Invalidate every existing browser session, including alex's.
    op.execute("DELETE FROM auth_sessions")

    # This is a one-time pre-operational reset. No valid verification/audit
    # history exists yet; preserve the append-only trigger after clearing it.
    op.execute(
        "ALTER TABLE audit_records "
        "DISABLE TRIGGER trg_audit_records_immutable"
    )
    op.execute("DELETE FROM audit_records")
    op.execute(
        "ALTER TABLE audit_records "
        "ENABLE TRIGGER trg_audit_records_immutable"
    )
    op.execute("DELETE FROM audit_operations")
    op.execute("DELETE FROM audit_logs")

    # Production and document records.
    op.execute("DELETE FROM arshin_exports")
    op.execute("DELETE FROM verifications")
    op.execute("DELETE FROM diagnostics")
    op.execute("DELETE FROM repairs")
    op.execute("DELETE FROM workflow_instances")
    op.execute("DELETE FROM documents")
    op.execute("DELETE FROM instrument_labels")
    op.execute("DELETE FROM warehouse_movements")
    op.execute("DELETE FROM warehouse_stocks")
    op.execute("DELETE FROM production_movements")

    # Customer, order, instrument and site records.
    op.execute("DELETE FROM order_items")
    op.execute("DELETE FROM orders")
    op.execute("DELETE FROM instruments")
    op.execute("DELETE FROM sites")
    op.execute("DELETE FROM customers")

    # Business reference/master data is also reset. It can be repopulated
    # deliberately after the clean baseline is established.
    op.execute("DELETE FROM price_list_items")
    op.execute("DELETE FROM workflow_stages")
    op.execute("DELETE FROM workflows")
    op.execute("DELETE FROM materials")
    op.execute("DELETE FROM warehouses")
    op.execute("DELETE FROM price_lists")
    op.execute("DELETE FROM document_templates")
    op.execute("DELETE FROM instrument_types")
    op.execute("DELETE FROM methodologies")
    op.execute("DELETE FROM verification_methods")

    # Keep the existing alex account and its RBAC assignments unchanged.
    op.execute(
        "DELETE FROM user_roles "
        "WHERE user_id <> (SELECT id FROM users WHERE username = 'alex')"
    )
    op.execute("DELETE FROM users WHERE username <> 'alex'")


def downgrade() -> None:
    """The deleted business data cannot be reconstructed by a schema downgrade."""
    raise RuntimeError(
        "This data reset is irreversible. Restore the database from a backup "
        "instead of downgrading this revision."
    )

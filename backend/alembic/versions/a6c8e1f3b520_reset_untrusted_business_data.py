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


def _delete_if_table_exists(table_name: str) -> None:
    """Delete rows only when an optional legacy table exists in this database."""
    bind = op.get_bind()
    if sa.inspect(bind).has_table(table_name):
        op.execute(sa.text(f'DELETE FROM "{table_name}"'))


def _truncate_if_table_exists(table_name: str) -> None:
    """Truncate rows only when an optional table exists in this database."""
    bind = op.get_bind()
    if sa.inspect(bind).has_table(table_name):
        op.execute(sa.text(f'TRUNCATE TABLE "{table_name}"'))


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
    _delete_if_table_exists("auth_sessions")

    # This is a one-time pre-operational reset. TRUNCATE removes the untrusted
    # rows without invoking row-level UPDATE/DELETE triggers; the append-only
    # trigger remains installed and enabled throughout.
    _truncate_if_table_exists("audit_records")
    _delete_if_table_exists("audit_operations")

    # Production and document records.
    for table_name in (
        "arshin_exports",
        "verifications",
        "diagnostics",
        "repairs",
        "workflow_instances",
        "documents",
        "instrument_labels",
        "warehouse_movements",
        "warehouse_stocks",
        "production_movements",
    ):
        _delete_if_table_exists(table_name)

    # Customer, order, instrument and site records.
    for table_name in (
        "order_items",
        "orders",
        "instruments",
        "sites",
        "customers",
    ):
        _delete_if_table_exists(table_name)

    # Business reference/master data is also reset. It can be repopulated
    # deliberately after the clean baseline is established.
    for table_name in (
        "price_list_items",
        "workflow_stages",
        "workflows",
        "materials",
        "warehouses",
        "price_lists",
        "document_templates",
        "instrument_types",
        "methodologies",
        "verification_methods",
    ):
        _delete_if_table_exists(table_name)

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

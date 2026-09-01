"""add audit records

Revision ID: 5b7c9e2a1f40
Revises: 071a88b4b6da
Create Date: 2026-09-01

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "5b7c9e2a1f40"
down_revision: str | Sequence[str] | None = "071a88b4b6da"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "audit_records",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("operation_id", sa.UUID(), nullable=False),
        sa.Column("actor_id", sa.UUID(), nullable=False),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("entity_type", sa.String(length=100), nullable=False),
        sa.Column("entity_id", sa.UUID(), nullable=False),
        sa.Column("changes", sa.dialects.postgresql.JSONB(), nullable=False),
        sa.Column("reason", sa.String(length=1000), nullable=True),
        sa.Column("related_record_id", sa.UUID(), nullable=True),
        sa.Column(
            "occurred_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["related_record_id"], ["audit_records.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_audit_records_operation_id"),
        "audit_records",
        ["operation_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_audit_records_actor_id"),
        "audit_records",
        ["actor_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_audit_records_entity_id"),
        "audit_records",
        ["entity_id"],
        unique=False,
    )
    op.create_index(
        "ix_audit_records_entity_type_entity_id",
        "audit_records",
        ["entity_type", "entity_id"],
        unique=False,
    )
    op.create_index(
        "ix_audit_records_occurred_at",
        "audit_records",
        ["occurred_at"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_audit_records_occurred_at", table_name="audit_records")
    op.drop_index(
        "ix_audit_records_entity_type_entity_id",
        table_name="audit_records",
    )
    op.drop_index(op.f("ix_audit_records_entity_id"), table_name="audit_records")
    op.drop_index(op.f("ix_audit_records_actor_id"), table_name="audit_records")
    op.drop_index(op.f("ix_audit_records_operation_id"), table_name="audit_records")
    op.drop_table("audit_records")

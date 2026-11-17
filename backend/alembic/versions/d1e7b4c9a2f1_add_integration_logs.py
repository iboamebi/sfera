"""Add integration exchange logs.

Revision ID: d1e7b4c9a2f1
Revises: c4e8a1d7b260
Create Date: 2026-11-17
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "d1e7b4c9a2f1"
down_revision: str | Sequence[str] | None = "c4e8a1d7b260"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create integration exchange log persistence."""
    integration_log_status = postgresql.ENUM(
        "STARTED",
        "SUCCESS",
        "WARNING",
        "ERROR",
        "CANCELLED",
        name="integration_log_status",
    )
    integration_log_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "integration_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("integration_type", sa.String(length=100), nullable=False),
        sa.Column("operation", sa.String(length=100), nullable=False),
        sa.Column(
            "status",
            postgresql.ENUM(
                "STARTED",
                "SUCCESS",
                "WARNING",
                "ERROR",
                "CANCELLED",
                name="integration_log_status",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("request_data", postgresql.JSONB(), nullable=True),
        sa.Column("response_data", postgresql.JSONB(), nullable=True),
        sa.Column(
            "created_by",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Remove integration exchange log persistence."""
    op.drop_table("integration_logs")
    postgresql.ENUM(
        "STARTED",
        "SUCCESS",
        "WARNING",
        "ERROR",
        "CANCELLED",
        name="integration_log_status",
    ).drop(op.get_bind(), checkfirst=True)

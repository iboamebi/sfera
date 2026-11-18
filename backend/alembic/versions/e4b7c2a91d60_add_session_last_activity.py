"""Add last activity timestamp to authenticated sessions.

Revision ID: e4b7c2a91d60
Revises: d1e7b4c9a2f1
Create Date: 2026-11-18
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "e4b7c2a91d60"
down_revision: str | Sequence[str] | None = "d1e7b4c9a2f1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add and backfill the last observed activity timestamp."""

    op.add_column(
        "auth_sessions",
        sa.Column("last_activity_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.execute(
        "UPDATE auth_sessions SET last_activity_at = created_at "
        "WHERE last_activity_at IS NULL"
    )
    op.alter_column("auth_sessions", "last_activity_at", nullable=False)
    op.create_index(
        op.f("ix_auth_sessions_last_activity_at"),
        "auth_sessions",
        ["last_activity_at"],
        unique=False,
    )


def downgrade() -> None:
    """Remove the last observed activity timestamp."""

    op.drop_index(
        op.f("ix_auth_sessions_last_activity_at"),
        table_name="auth_sessions",
    )
    op.drop_column("auth_sessions", "last_activity_at")

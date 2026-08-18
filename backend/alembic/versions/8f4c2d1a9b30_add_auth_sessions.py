"""add auth sessions

Revision ID: 8f4c2d1a9b30
Revises: 9a1ddec34200
Create Date: 2026-08-18 20:25:00

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "8f4c2d1a9b30"
down_revision: str | Sequence[str] | None = "9a1ddec34200"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "auth_sessions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("session_id", sa.String(length=128), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("session_id"),
    )
    op.create_index(
        op.f("ix_auth_sessions_session_id"),
        "auth_sessions",
        ["session_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_auth_sessions_user_id"),
        "auth_sessions",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_auth_sessions_expires_at"),
        "auth_sessions",
        ["expires_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_auth_sessions_expires_at"), table_name="auth_sessions")
    op.drop_index(op.f("ix_auth_sessions_user_id"), table_name="auth_sessions")
    op.drop_index(op.f("ix_auth_sessions_session_id"), table_name="auth_sessions")
    op.drop_table("auth_sessions")

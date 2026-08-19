"""add user role

Revision ID: d1f7a8c9e2b4
Revises: 8f4c2d1a9b30
Create Date: 2026-08-19 15:00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "d1f7a8c9e2b4"
down_revision: str | Sequence[str] | None = "8f4c2d1a9b30"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.String(length=32),
            server_default=sa.text("'operator'"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "role")

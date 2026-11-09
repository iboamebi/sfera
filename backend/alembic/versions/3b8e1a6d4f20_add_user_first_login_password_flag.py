"""add user first-login password flag

Revision ID: 3b8e1a6d4f20
Revises: a7c9e2f4b610
Create Date: 2026-11-02

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "3b8e1a6d4f20"
down_revision: str | Sequence[str] | None = "a7c9e2f4b610"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "must_change_password",
            sa.Boolean(),
            server_default=sa.false(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "must_change_password")

"""add instrument association to verifications

Revision ID: b6c1e8f3a420
Revises: 071a88b4b6da
Create Date: 2026-09-04

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b6c1e8f3a420"
down_revision: Union[str, Sequence[str], None] = "071a88b4b6da"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add instrument association and backfill it from order items."""
    op.add_column(
        "verifications",
        sa.Column("instrument_id", sa.Uuid(), nullable=True),
    )
    op.create_foreign_key(
        "fk_verifications_instrument_id_instruments",
        "verifications",
        "instruments",
        ["instrument_id"],
        ["id"],
    )
    op.execute(
        sa.text(
            """
            UPDATE verifications AS v
            SET instrument_id = oi.instrument_id
            FROM order_items AS oi
            WHERE v.order_item_id = oi.id
              AND oi.instrument_id IS NOT NULL
            """
        )
    )


def downgrade() -> None:
    """Remove instrument association from verifications."""
    op.drop_constraint(
        "fk_verifications_instrument_id_instruments",
        "verifications",
        type_="foreignkey",
    )
    op.drop_column("verifications", "instrument_id")

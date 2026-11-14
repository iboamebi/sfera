"""Enforce instrument serial uniqueness per customer and type.

Revision ID: d4e8a1c6f230
Revises: 7a9d2e4c6b10
Create Date: 2026-11-14
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "d4e8a1c6f230"
down_revision: str | Sequence[str] | None = "7a9d2e4c6b10"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Enforce normalized serial uniqueness within Customer and Instrument Type."""
    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM instruments
                GROUP BY customer_id, instrument_type_id,
                         lower(btrim(serial_number))
                HAVING COUNT(*) > 1
            ) THEN
                RAISE EXCEPTION
                    'Cannot enforce instrument serial uniqueness: duplicate serials exist for the same customer and instrument type';
            END IF;
        END
        $$;
        """
    )
    op.execute(

        """
        DROP INDEX uq_instruments_customer_type_serial;
        CREATE UNIQUE INDEX uq_instruments_customer_type_serial
        ON instruments (
            customer_id,
            instrument_type_id,
            lower(btrim(serial_number))
        );
        """
    )


def downgrade() -> None:
    """Remove Customer and Instrument Type serial uniqueness."""
    op.drop_index(
        "uq_instruments_customer_type_serial",
        table_name="instruments",
    )

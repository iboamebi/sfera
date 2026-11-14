"""Enforce one active verification per order item.

Revision ID: 7a9d2e4c6b10
Revises: c2e5f7a9b310
Create Date: 2026-11-14
"""

from alembic import op

revision = "7a9d2e4c6b10"
down_revision = "c2e5f7a9b310"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM verifications
                WHERE archived = false
                  AND status IN ('CREATED', 'IN_PROGRESS')
                GROUP BY order_item_id
                HAVING COUNT(*) > 1
            ) THEN
                RAISE EXCEPTION
                    'Cannot enforce one active verification per order item: duplicates exist';
            END IF;
        END
        $$;
        """
    )
    op.create_index(
        "uq_verifications_one_active_per_order_item",
        "verifications",
        ["order_item_id"],
        unique=True,
        postgresql_where=op.text(
            "archived = false AND status IN ('CREATED', 'IN_PROGRESS')"
        ),
    )


def downgrade() -> None:
    op.drop_index(
        "uq_verifications_one_active_per_order_item",
        table_name="verifications",
    )

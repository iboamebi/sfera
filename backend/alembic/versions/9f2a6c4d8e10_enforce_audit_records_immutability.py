"""enforce audit record immutability

Revision ID: 9f2a6c4d8e10
Revises: 4c9e2a7b1d60
Create Date: 2026-11-03

"""

from collections.abc import Sequence

from alembic import op

revision: str = "9f2a6c4d8e10"
down_revision: str | None = "4c9e2a7b1d60"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Prevent updates and deletes of historical audit records."""
    op.execute(
        """
        CREATE FUNCTION prevent_audit_records_mutation()
        RETURNS trigger
        LANGUAGE plpgsql
        AS $$
        BEGIN
            RAISE EXCEPTION
                'audit_records is append-only: % is not allowed', TG_OP
                USING ERRCODE = '55000';
        END;
        $$
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_audit_records_immutable
        BEFORE UPDATE OR DELETE ON audit_records
        FOR EACH ROW
        EXECUTE FUNCTION prevent_audit_records_mutation()
        """
    )


def downgrade() -> None:
    """Remove audit record immutability enforcement."""
    op.execute(
        "DROP TRIGGER IF EXISTS trg_audit_records_immutable ON audit_records"
    )
    op.execute("DROP FUNCTION IF EXISTS prevent_audit_records_mutation()")

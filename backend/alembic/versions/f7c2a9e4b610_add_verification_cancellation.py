"""Add cancelled verification state and cancellation reason."""
import sqlalchemy as sa
from alembic import op
revision = "f7c2a9e4b610"
down_revision = ("d4e8a1c6f230", "e2d7f4a9c130")
branch_labels = None
depends_on = None
def upgrade() -> None:
    op.execute("ALTER TYPE verification_status ADD VALUE IF NOT EXISTS 'CANCELLED'")
    op.add_column("verifications", sa.Column("cancellation_reason", sa.Text(), nullable=True))
def downgrade() -> None:
    op.drop_column("verifications", "cancellation_reason")

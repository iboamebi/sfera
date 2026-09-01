"""SQLAlchemy model for audit operations."""

from uuid import UUID

from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AuditOperationModel(Base):
    """Store the initiator of one logical application operation."""

    __tablename__ = "audit_operations"

    operation_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
    )
    initiated_by: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        nullable=False,
        index=True,
    )

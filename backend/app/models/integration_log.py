import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.dialects.postgresql import JSONB, UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class IntegrationLogStatus(StrEnum):
    STARTED = "STARTED"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CANCELLED = "CANCELLED"


class IntegrationLogModel(Base):
    """Store one integration exchange attempt."""

    __tablename__ = "integration_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
    )
    integration_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    operation: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    status: Mapped[IntegrationLogStatus] = mapped_column(
        SqlEnum(IntegrationLogStatus, name="integration_log_status"),
        nullable=False,
    )
    request_data: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )
    response_data: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

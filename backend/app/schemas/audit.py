"""Audit journal API schemas."""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AuditRecordListRead(BaseModel):
    """One immutable audit journal entry."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    operation_id: UUID
    actor_id: UUID
    actor_username: str | None
    actor_full_name: str | None
    initiated_by: UUID | None
    initiator_username: str | None
    initiator_full_name: str | None
    action: str
    entity_type: str
    entity_id: UUID | None
    changes: dict[str, Any]
    reason: str | None
    related_record_id: UUID | None
    occurred_at: datetime


class AuditRecordPageRead(BaseModel):
    """Paginated audit journal response."""

    items: list[AuditRecordListRead]
    total: int
    limit: int = Field(ge=1, le=200)
    offset: int = Field(ge=0)

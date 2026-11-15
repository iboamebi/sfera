"""Audit read models."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID


@dataclass(frozen=True)
class AuditRecordReadData:
    """Read data for one immutable audit record."""

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
    entity_display_name: str | None
    changes: dict[str, Any]
    reason: str | None
    related_record_id: UUID | None
    occurred_at: datetime

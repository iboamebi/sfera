"""
Application contracts for audit persistence.
"""

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(frozen=True, kw_only=True)
class AuditOperation:
    """Describe one logical application operation."""

    operation_id: UUID = field(default_factory=uuid4)
    initiated_by: UUID


@dataclass(frozen=True, kw_only=True)
class AuditRecord:
    """Describe one immutable audit record before persistence."""

    operation_id: UUID
    actor_id: UUID
    action: str
    entity_type: str
    entity_id: UUID | None
    changes: dict[str, object]
    reason: str | None = None
    related_record_id: UUID | None = None
    id: UUID = field(default_factory=uuid4)

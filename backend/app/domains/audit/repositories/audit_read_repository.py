"""Audit read repository contract."""

from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from app.domains.audit.read_models.audit_read_models import AuditRecordReadData


class AuditReadRepository(ABC):
    """Read-only access to persistent audit records."""

    @abstractmethod
    def list(
        self,
        *,
        occurred_from: datetime | None,
        occurred_to: datetime | None,
        actor_id: UUID | None,
        actor_query: str | None,
        action: str | None,
        entity_type: str | None,
        operation_id: UUID | None,
        limit: int,
        offset: int,
    ) -> tuple[list[AuditRecordReadData], int]:
        """Return a page of audit records and the total matching count."""
        raise NotImplementedError

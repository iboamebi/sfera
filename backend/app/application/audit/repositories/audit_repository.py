from abc import ABC, abstractmethod

from app.shared.audit.models import AuditRecord


class AuditRepository(ABC):
    """Persist audit records."""

    @abstractmethod
    def save(self, record: AuditRecord) -> None: ...

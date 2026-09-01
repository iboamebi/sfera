from abc import ABC, abstractmethod

from app.shared.audit.models import AuditOperation


class AuditOperationRepository(ABC):
    """Persistence contract for audit operations."""

    @abstractmethod
    def save(self, operation: AuditOperation) -> None:
        """Persist an audit operation."""
        raise NotImplementedError

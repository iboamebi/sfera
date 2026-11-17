"""Persistence contract for integration exchange logs."""

from abc import ABC, abstractmethod
from uuid import UUID

from app.shared.integration.models import IntegrationLog


class IntegrationLogRepository(ABC):
    """Persist integration exchange logs."""

    @abstractmethod
    def get(self, integration_log_id: UUID) -> IntegrationLog | None:
        """Get an integration log by identifier."""

        raise NotImplementedError

    @abstractmethod
    def save(self, integration_log: IntegrationLog) -> None:
        """Persist an integration log."""

        raise NotImplementedError

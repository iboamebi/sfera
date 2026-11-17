"""Shared contracts for integration exchange logs."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4


class IntegrationLogStatus(StrEnum):
    """Lifecycle status of one integration attempt."""

    STARTED = "STARTED"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CANCELLED = "CANCELLED"


@dataclass(eq=False, kw_only=True)
class IntegrationLog:
    """Record one externally visible integration operation."""

    id: UUID = field(default_factory=uuid4)
    integration_type: str
    operation: str
    status: IntegrationLogStatus = IntegrationLogStatus.STARTED
    request_data: dict[str, object] | None = None
    response_data: dict[str, object] | None = None
    created_by: UUID | None = None
    created_at: datetime

    def mark_success(
        self,
        response_data: dict[str, object] | None = None,
    ) -> None:
        """Mark a started operation as successful."""

        self._ensure_started()
        self.status = IntegrationLogStatus.SUCCESS
        self.response_data = response_data

    def mark_warning(
        self,
        response_data: dict[str, object] | None = None,
    ) -> None:
        """Mark a started operation as completed with a warning."""

        self._ensure_started()
        self.status = IntegrationLogStatus.WARNING
        self.response_data = response_data

    def mark_error(
        self,
        response_data: dict[str, object] | None = None,
    ) -> None:
        """Mark a started operation as failed."""

        self._ensure_started()
        self.status = IntegrationLogStatus.ERROR
        self.response_data = response_data

    def cancel(
        self,
        response_data: dict[str, object] | None = None,
    ) -> None:
        """Mark a started operation as cancelled."""

        self._ensure_started()
        self.status = IntegrationLogStatus.CANCELLED
        self.response_data = response_data

    def _ensure_started(self) -> None:
        if self.status != IntegrationLogStatus.STARTED:
            raise ValueError("Integration log is already finalized")

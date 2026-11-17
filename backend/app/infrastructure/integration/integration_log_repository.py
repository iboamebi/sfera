"""SQLAlchemy integration log repository."""

from uuid import UUID

from sqlalchemy.orm import Session

from app.infrastructure.mappers.integration_log_mapper import IntegrationLogMapper
from app.models.integration_log import IntegrationLogModel
from app.shared.integration.models import IntegrationLog
from app.shared.integration.repositories.integration_log_repository import (
    IntegrationLogRepository,
)


class IntegrationLogRepositorySQLAlchemy(IntegrationLogRepository):
    """SQLAlchemy implementation of IntegrationLogRepository."""

    def __init__(self, session: Session) -> None:
        self._session = session
        self._mapper = IntegrationLogMapper()

    def get(self, integration_log_id: UUID) -> IntegrationLog | None:
        """Get an integration log by identifier."""

        model = self._session.get(
            IntegrationLogModel,
            integration_log_id,
        )

        if model is None:
            return None

        return self._mapper.to_domain(model)

    def save(self, integration_log: IntegrationLog) -> None:
        """Persist an integration log."""

        model = self._session.get(
            IntegrationLogModel,
            integration_log.id,
        )

        if model is None:
            model = IntegrationLogModel(id=integration_log.id)
            self._session.add(model)

        self._mapper.to_model(integration_log, model)
        self._session.flush()

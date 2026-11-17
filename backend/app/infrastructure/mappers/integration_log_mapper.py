"""Integration log mapper."""

from app.infrastructure.mappers.base_mapper import BaseMapper
from app.models.integration_log import IntegrationLogModel, IntegrationLogStatus
from app.shared.integration.models import IntegrationLog
from app.shared.integration.models import IntegrationLogStatus as DomainStatus


class IntegrationLogMapper(
    BaseMapper[IntegrationLog, IntegrationLogModel],
):
    """Maps integration logs between domain and persistence."""

    def to_domain(self, model: IntegrationLogModel) -> IntegrationLog:
        """Convert ORM model to domain entity."""

        return IntegrationLog(
            id=model.id,
            integration_type=model.integration_type,
            operation=model.operation,
            status=DomainStatus(model.status.value),
            request_data=model.request_data,
            response_data=model.response_data,
            created_by=model.created_by,
            created_at=model.created_at,
        )

    def to_model(
        self,
        entity: IntegrationLog,
        model: IntegrationLogModel,
    ) -> IntegrationLogModel:
        """Convert domain entity to ORM model."""

        model.integration_type = entity.integration_type
        model.operation = entity.operation
        model.status = IntegrationLogStatus(entity.status.value)
        model.request_data = entity.request_data
        model.response_data = entity.response_data
        model.created_by = entity.created_by
        model.created_at = entity.created_at
        return model

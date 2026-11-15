"""Application query service for the administrative audit journal."""

from datetime import datetime
from uuid import UUID

from app.application.audit.queries.audit_read_mapper import AuditReadMapper
from app.application.authorization.authorization import require_role
from app.domains.audit.repositories.audit_read_repository import AuditReadRepository
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.schemas.audit import AuditRecordPageRead


class AuditReadService:
    """Provides administrator-only read access to persistent audit records."""

    def __init__(self, repository: AuditReadRepository) -> None:
        self._repository = repository
        self._mapper = AuditReadMapper()

    def list(
        self,
        actor: User,
        *,
        occurred_from: datetime | None = None,
        occurred_to: datetime | None = None,
        actor_id: UUID | None = None,
        actor_query: str | None = None,
        action: str | None = None,
        entity_type: str | None = None,
        operation_id: UUID | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> AuditRecordPageRead:
        """List audit records after enforcing administrator authorization."""
        require_role(actor, UserRole.ADMIN)
        records, total = self._repository.list(
            occurred_from=occurred_from,
            occurred_to=occurred_to,
            actor_id=actor_id,
            action=action,
            entity_type=entity_type,
            operation_id=operation_id,
            limit=limit,
            offset=offset,
        )
        return AuditRecordPageRead(
            items=[self._mapper.to_schema(record) for record in records],
            total=total,
            limit=limit,
            offset=offset,
        )

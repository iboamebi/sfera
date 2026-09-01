"""SQLAlchemy implementation of AuditRepository."""

from sqlalchemy.orm import Session

from app.application.audit.repositories.audit_repository import AuditRepository
from app.models.audit_record import AuditRecordModel
from app.shared.audit.models import AuditRecord


class AuditRepositorySQLAlchemy(AuditRepository):
    """SQLAlchemy audit repository."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, record: AuditRecord) -> None:
        """Persist an audit record."""

        self.session.add(
            AuditRecordModel(
                id=record.id,
                operation_id=record.operation_id,
                actor_id=record.actor_id,
                action=record.action,
                entity_type=record.entity_type,
                entity_id=record.entity_id,
                changes=record.changes,
                reason=record.reason,
                related_record_id=record.related_record_id,
            )
        )
        self.session.flush()

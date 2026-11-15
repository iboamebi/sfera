"""SQLAlchemy implementation of the audit read repository."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session, aliased

from app.domains.audit.read_models.audit_read_models import AuditRecordReadData
from app.domains.audit.repositories.audit_read_repository import AuditReadRepository
from app.models.audit_operation import AuditOperationModel
from app.models.audit_record import AuditRecordModel
from app.models.user import User


class AuditReadRepositorySQLAlchemy(AuditReadRepository):
    """Read-only SQLAlchemy audit repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def list(
        self,
        *,
        occurred_from: datetime | None,
        occurred_to: datetime | None,
        actor_id: UUID | None,
        action: str | None,
        entity_type: str | None,
        operation_id: UUID | None,
        limit: int,
        offset: int,
    ) -> tuple[list[AuditRecordReadData], int]:
        actor = aliased(User)
        initiator = aliased(User)
        query = (
            self._session.query(AuditRecordModel, actor, AuditOperationModel, initiator)
            .outerjoin(actor, actor.id == AuditRecordModel.actor_id)
            .outerjoin(
                AuditOperationModel,
                AuditOperationModel.operation_id == AuditRecordModel.operation_id,
            )
            .outerjoin(
                initiator,
                initiator.id == AuditOperationModel.initiated_by,
            )
        )

        if occurred_from is not None:
            query = query.filter(AuditRecordModel.occurred_at >= occurred_from)
        if occurred_to is not None:
            query = query.filter(AuditRecordModel.occurred_at <= occurred_to)
        if actor_id is not None:
            query = query.filter(AuditRecordModel.actor_id == actor_id)
        if action is not None:
            query = query.filter(AuditRecordModel.action == action)
        if entity_type is not None:
            query = query.filter(AuditRecordModel.entity_type == entity_type)
        if operation_id is not None:
            query = query.filter(AuditRecordModel.operation_id == operation_id)

        total = query.with_entities(func.count(AuditRecordModel.id)).scalar() or 0
        rows = (
            query.order_by(
                AuditRecordModel.occurred_at.desc(),
                AuditRecordModel.id.desc(),
            )
            .offset(offset)
            .limit(limit)
            .all()
        )

        records = [
            AuditRecordReadData(
                id=record.id,
                operation_id=record.operation_id,
                actor_id=record.actor_id,
                actor_username=actor.username if actor else None,
                actor_full_name=actor.full_name if actor else None,
                initiated_by=operation.initiated_by if operation else None,
                initiator_username=initiator.username if initiator else None,
                initiator_full_name=initiator.full_name if initiator else None,
                action=record.action,
                entity_type=record.entity_type,
                entity_id=record.entity_id,
                changes=record.changes,
                reason=record.reason,
                related_record_id=record.related_record_id,
                occurred_at=record.occurred_at,
            )
            for record, actor, operation, initiator in rows
        ]
        return records, total

"""Audit read model mapper."""

from app.domains.audit.read_models.audit_read_models import AuditRecordReadData
from app.schemas.audit import AuditRecordListRead


class AuditReadMapper:
    """Map audit read data to API schemas."""

    def to_schema(self, record: AuditRecordReadData) -> AuditRecordListRead:
        return AuditRecordListRead(
            id=record.id,
            operation_id=record.operation_id,
            actor_id=record.actor_id,
            actor_username=record.actor_username,
            actor_full_name=record.actor_full_name,
            initiated_by=record.initiated_by,
            initiator_username=record.initiator_username,
            initiator_full_name=record.initiator_full_name,
            action=record.action,
            entity_type=record.entity_type,
            entity_id=record.entity_id,
            entity_display_name=record.entity_display_name,
            changes=record.changes,
            reason=record.reason,
            related_record_id=record.related_record_id,
            occurred_at=record.occurred_at,
        )

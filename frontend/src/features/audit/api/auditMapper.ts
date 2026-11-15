import type { AuditRecord } from "../model/types";
import type { AuditRecordApiDto } from "./types";

export function mapAuditRecord(dto: AuditRecordApiDto): AuditRecord {
  return {
    id: dto.id,
    operationId: dto.operation_id,
    actorId: dto.actor_id,
    actorUsername: dto.actor_username,
    actorFullName: dto.actor_full_name,
    initiatedBy: dto.initiated_by,
    initiatorUsername: dto.initiator_username,
    initiatorFullName: dto.initiator_full_name,
    action: dto.action,
    entityType: dto.entity_type,
    entityId: dto.entity_id,
    changes: dto.changes,
    reason: dto.reason,
    relatedRecordId: dto.related_record_id,
    occurredAt: dto.occurred_at,
  };
}

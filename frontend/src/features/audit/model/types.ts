export interface AuditRecord {
  id: string;
  operationId: string;
  actorId: string;
  actorUsername: string | null;
  actorFullName: string | null;
  initiatedBy: string | null;
  initiatorUsername: string | null;
  initiatorFullName: string | null;
  action: string;
  entityType: string;
  entityId: string | null;
  entityDisplayName: string | null;
  changes: Record<string, unknown>;
  reason: string | null;
  relatedRecordId: string | null;
  occurredAt: string;
}

export interface AuditRecordPage {
  items: AuditRecord[];
  total: number;
  limit: number;
  offset: number;
}

export interface AuditFilters {
  occurredFrom: string;
  occurredTo: string;
  actorQuery: string;
  action: string;
  entityType: string;
  operationId: string;
  limit: number;
  offset: number;
}

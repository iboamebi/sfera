export interface AuditRecordApiDto {
  id: string;
  operation_id: string;
  actor_id: string;
  actor_username: string | null;
  actor_full_name: string | null;
  initiated_by: string | null;
  initiator_username: string | null;
  initiator_full_name: string | null;
  action: string;
  entity_type: string;
  entity_id: string | null;
  entity_display_name: string | null;
  changes: Record<string, unknown>;
  reason: string | null;
  related_record_id: string | null;
  occurred_at: string;
}

export interface AuditRecordPageApiDto {
  items: AuditRecordApiDto[];
  total: number;
  limit: number;
  offset: number;
}

export interface AuditQueryParams {
  occurred_from?: string;
  occurred_to?: string;
  actor_query?: string;
  action?: string;
  entity_type?: string;
  operation_id?: string;
  limit: number;
  offset: number;
}

import { useQuery } from "@tanstack/react-query";

import { getAuditRecords } from "../api/getAuditRecords";
import type { AuditFilters } from "./types";

export function useAuditRecords(filters: AuditFilters) {
  const params = {
    ...(filters.occurredFrom && { occurred_from: new Date(filters.occurredFrom).toISOString() }),
    ...(filters.occurredTo && { occurred_to: new Date(filters.occurredTo).toISOString() }),
    ...(filters.actorQuery.trim() && { actor_query: filters.actorQuery.trim() }),
    ...(filters.action && { action: filters.action.trim() }),
    ...(filters.entityType && { entity_type: filters.entityType.trim() }),
    ...(filters.operationId && { operation_id: filters.operationId.trim() }),
    limit: filters.limit,
    offset: filters.offset,
  };

  return useQuery({
    queryKey: ["audit-records", params],
    queryFn: () => getAuditRecords(params),
    placeholderData: (previousData) => previousData,
  });
}

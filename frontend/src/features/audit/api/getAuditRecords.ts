import { http } from "../../../shared/api/http";
import type { AuditRecordPage } from "../model/types";
import { mapAuditRecord } from "./auditMapper";
import type { AuditQueryParams, AuditRecordPageApiDto } from "./types";

export async function getAuditRecords(
  params: AuditQueryParams,
): Promise<AuditRecordPage> {
  const response = await http.get<AuditRecordPageApiDto>("/audit/", { params });

  return {
    ...response.data,
    items: response.data.items.map(mapAuditRecord),
  };
}

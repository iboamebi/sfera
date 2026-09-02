import type { OrderRead } from "../model/types";
import type { OrderApiDto } from "./types";

export function mapOrder(dto: OrderApiDto): OrderRead {
  return {
    id: dto.id,
    number: dto.number,
    customerId: dto.customer_id,
    customerName: dto.customer_name,
    status: dto.status,
    receivedAt: dto.received_at,
    createdAt: dto.created_at,
    updatedAt: dto.updated_at,
    plannedIssueAt: dto.planned_issue_at,
    issuedAt: dto.issued_at,
    comment: dto.comment,
    archived: dto.archived,
    items: dto.items.map((item) => ({
      id: item.id,
      instrumentId: item.instrument_id,
      instrumentTypeId: item.instrument_type_id,
      instrumentName: item.instrument_name,
      instrumentTypeName: item.instrument_type_name,
      serialNumber: item.serial_number,
      modification: item.modification,
      comment: item.comment,
      requestedOperations: item.requested_operations,
    })),
  };
}

import type { OrderRead } from "../model/types";
import type { OrderApiDto } from "./types";

export function mapOrder(dto: OrderApiDto): OrderRead {
  return {
    id: dto.id,
    number: dto.number,
    customerId: dto.customer_id,
    status: dto.status,
    receivedAt: dto.received_at,
    plannedIssueAt: dto.planned_issue_at,
    issuedAt: dto.issued_at,
    comment: dto.comment,
    archived: dto.archived,
    items: dto.items.map((item) => ({
      id: item.id,
      instrumentId: item.instrument_id,
      comment: item.comment,
    })),
  };
}

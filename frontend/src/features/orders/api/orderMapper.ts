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
      instrumentTypeId: item.instrument_type_id,
      instrumentTypeName: item.instrument_type_name,
      instrumentTypeModel: item.instrument_type_model,
      instrumentTypeMeasurementType: item.instrument_type_measurement_type,
      serialNumber: item.serial_number,
      modification: item.modification,
      comment: item.comment,
      requestedOperations: item.requested_operations,
    })),
  };
}

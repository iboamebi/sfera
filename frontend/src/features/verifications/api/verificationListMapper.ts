import type { VerificationListRead } from "../model/types";
import type { VerificationListApiDto } from "./types";

export function mapVerificationList(
  dto: VerificationListApiDto,
): VerificationListRead {
  return {
    id: dto.id,
    orderItemId: dto.order_item_id,
    orderId: dto.order_id,
    orderNumber: dto.order_number,
    customerId: dto.customer_id,
    customerName: dto.customer_name,
    instrumentId: dto.instrument_id,
    instrumentName: dto.instrument_name,
    instrumentTypeId: dto.instrument_type_id,
    instrumentTypeName: dto.instrument_type_name,
    serialNumber: dto.serial_number,
    verificationDate: dto.verification_date,
    verificationType: dto.verification_type,
    status: dto.status,
    result: dto.result,
    validUntil: dto.valid_until,
    createdAt: dto.created_at,
    startedAt: dto.started_at,
    decisionAt: dto.decision_at,
    archived: dto.archived,
  };
}

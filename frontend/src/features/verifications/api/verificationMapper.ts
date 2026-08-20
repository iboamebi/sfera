import type { VerificationRead } from "../model/types";
import type { VerificationApiDto } from "./types";

export function mapVerification(dto: VerificationApiDto): VerificationRead {
  return {
    id: dto.id,
    orderItemId: dto.order_item_id,
    verificationDate: dto.verification_date,
    validUntil: dto.valid_until,
    result: dto.result,
    unsuitableReason: dto.unsuitable_reason,
    methodology: dto.methodology,
    archived: dto.archived,
  };
}

import { http } from "../../../../shared/api/http";

import { mapVerification } from "../../api/verificationMapper";
import type { VerificationApiDto } from "../../api/types";
import type { VerificationRead, VerificationType } from "../../model/types";

export interface CreateVerificationData {
  orderItemId: string;
  verificationDate: string;
  verificationType: VerificationType;
  methodology: string;
}

export async function createVerification(
  data: CreateVerificationData,
): Promise<VerificationRead> {
  const response = await http.post<VerificationApiDto>("/verifications", {
    order_item_id: data.orderItemId,
    verification_date: data.verificationDate,
    verification_type: data.verificationType,
    methodology: data.methodology.trim() || null,
  });

  return mapVerification(response.data);
}

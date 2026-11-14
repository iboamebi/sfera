import { http } from "../../../../shared/api/http";

import { mapVerification } from "../../api/verificationMapper";
import type { VerificationApiDto } from "../../api/types";
import type { VerificationRead } from "../../model/types";

export async function correctVerificationValidUntil(
  verificationId: string,
  validUntil: string,
  reason: string,
): Promise<VerificationRead> {
  const response = await http.post<VerificationApiDto>(
    `/verifications/${verificationId}/correct-valid-until`,
    null,
    { params: { valid_until: validUntil, reason } },
  );
  return mapVerification(response.data);
}

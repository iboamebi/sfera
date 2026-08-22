import { http } from "../../../../shared/api/http";

import { mapVerification } from "../../api/verificationMapper";
import type { VerificationApiDto } from "../../api/types";
import type { VerificationRead } from "../../model/types";

export async function approveVerification(
  verificationId: string,
  validUntil: string,
): Promise<VerificationRead> {
  const response = await http.post<VerificationApiDto>(
    `/verifications/${verificationId}/approve`,
    null,
    {
      params: {
        valid_until: validUntil,
      },
    },
  );

  return mapVerification(response.data);
}

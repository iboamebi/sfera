import { http } from "../../../../shared/api/http";

import { mapVerification } from "../../api/verificationMapper";
import type { VerificationApiDto } from "../../api/types";
import type { VerificationRead } from "../../model/types";

export async function rejectVerification(
  verificationId: string,
  reason: string,
): Promise<VerificationRead> {
  const response = await http.post<VerificationApiDto>(
    `/verifications/${verificationId}/reject`,
    null,
    {
      params: {
        reason,
      },
    },
  );

  return mapVerification(response.data);
}

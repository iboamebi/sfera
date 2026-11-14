import { http } from "../../../../shared/api/http";

import { mapVerification } from "../../api/verificationMapper";
import type { VerificationApiDto } from "../../api/types";
import type { VerificationRead } from "../../model/types";

interface ApproveVerificationInput {
  verificationId: string;
  durationYears: number;
  timeZone: string;
  validUntil?: string;
}

export async function approveVerification(
  input: ApproveVerificationInput,
): Promise<VerificationRead> {
  const response = await http.post<VerificationApiDto>(
    `/verifications/${input.verificationId}/approve`,
    null,
    {
      params: {
        duration_years: input.durationYears,
        time_zone: input.timeZone,
        ...(input.validUntil ? { valid_until: input.validUntil } : {}),
      },
    },
  );

  return mapVerification(response.data);
}

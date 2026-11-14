import { http } from "../../../../shared/api/http";

import { mapVerification } from "../../api/verificationMapper";
import type { VerificationApiDto } from "../../api/types";
import type { VerificationRead, VerificationResult } from "../../model/types";

interface CorrectVerificationDecisionInput {
  verificationId: string;
  result: VerificationResult;
  validUntil?: string;
  unsuitableReason?: string;
  reason: string;
}

export async function correctVerificationDecision(
  input: CorrectVerificationDecisionInput,
): Promise<VerificationRead> {
  const response = await http.post<VerificationApiDto>(
    `/verifications/${input.verificationId}/correct-decision`,
    {
      result: input.result,
      valid_until: input.validUntil ?? null,
      unsuitable_reason: input.unsuitableReason ?? null,
      reason: input.reason,
    },
  );

  return mapVerification(response.data);
}

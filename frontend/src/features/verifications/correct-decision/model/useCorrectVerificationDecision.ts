import { useMutation, type UseMutationOptions } from "@tanstack/react-query";

import { correctVerificationDecision } from "../api/correctVerificationDecision";
import type { VerificationRead, VerificationResult } from "../../model/types";

interface CorrectVerificationDecisionInput {
  verificationId: string;
  result: VerificationResult;
  validUntil?: string;
  unsuitableReason?: string;
  reason: string;
}

export function useCorrectVerificationDecision(
  options?: UseMutationOptions<
    VerificationRead,
    Error,
    CorrectVerificationDecisionInput
  >,
) {
  return useMutation({
    mutationFn: correctVerificationDecision,
    ...options,
  });
}

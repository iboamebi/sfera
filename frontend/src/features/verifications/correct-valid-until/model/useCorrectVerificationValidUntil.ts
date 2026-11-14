import { useMutation, type UseMutationOptions } from "@tanstack/react-query";

import { correctVerificationValidUntil } from "../api/correctVerificationValidUntil";
import type { VerificationRead } from "../../model/types";

interface CorrectionInput {
  verificationId: string;
  validUntil: string;
  reason: string;
}

export function useCorrectVerificationValidUntil(
  options?: UseMutationOptions<VerificationRead, Error, CorrectionInput>,
) {
  return useMutation({
    mutationFn: ({ verificationId, validUntil, reason }) =>
      correctVerificationValidUntil(verificationId, validUntil, reason),
    ...options,
  });
}

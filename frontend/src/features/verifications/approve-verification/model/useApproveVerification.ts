import { useMutation, type UseMutationOptions } from "@tanstack/react-query";

import { approveVerification } from "../api/approveVerification";
import type { VerificationRead } from "../../model/types";

interface ApproveVerificationInput {
  verificationId: string;
  durationYears: number;
  timeZone: string;
  validUntil?: string;
}

export function useApproveVerification(
  options?: UseMutationOptions<
    VerificationRead,
    Error,
    ApproveVerificationInput
  >,
) {
  return useMutation({
    mutationFn: approveVerification,
    ...options,
  });
}

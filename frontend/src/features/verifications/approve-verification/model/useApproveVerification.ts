import { useMutation, type UseMutationOptions } from "@tanstack/react-query";

import { approveVerification } from "../api/approveVerification";
import type { VerificationRead } from "../../model/types";

export function useApproveVerification(
  options?: UseMutationOptions<
    VerificationRead,
    Error,
    { verificationId: string; validUntil: string }
  >,
) {
  return useMutation({
    mutationFn: ({ verificationId, validUntil }) =>
      approveVerification(verificationId, validUntil),
    ...options,
  });
}

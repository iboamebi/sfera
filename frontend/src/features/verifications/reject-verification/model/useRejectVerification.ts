import { useMutation, type UseMutationOptions } from "@tanstack/react-query";

import { rejectVerification } from "../api/rejectVerification";
import type { VerificationRead } from "../../model/types";

export function useRejectVerification(
  options?: UseMutationOptions<
    VerificationRead,
    Error,
    { verificationId: string; reason: string }
  >,
) {
  return useMutation({
    mutationFn: ({ verificationId, reason }) =>
      rejectVerification(verificationId, reason),
    ...options,
  });
}

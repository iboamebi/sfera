import { useMutation, type UseMutationOptions } from "@tanstack/react-query";

import { startVerification } from "../api/startVerification";
import type { VerificationRead } from "../../model/types";

export function useStartVerification(
  options?: UseMutationOptions<VerificationRead, Error, string>,
) {
  return useMutation({
    mutationFn: startVerification,
    ...options,
  });
}

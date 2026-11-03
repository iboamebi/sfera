import { useMutation, useQueryClient } from "@tanstack/react-query";

import {
  createVerification,
  type CreateVerificationData,
} from "../api/createVerification";

export function useCreateVerification(orderId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createVerification,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["orders", orderId] });
    },
  });
}

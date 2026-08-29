import { useMutation, useQueryClient } from "@tanstack/react-query";

import { updateDevice } from "../api/updateDevice";

export function useUpdateDevice(orderId?: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateDevice,
    onSuccess: async () => {
      if (orderId) {
        await Promise.all([
          queryClient.invalidateQueries({ queryKey: ["orders", orderId] }),
          queryClient.invalidateQueries({ queryKey: ["orders"] }),
        ]);
      }

      await queryClient.invalidateQueries({ queryKey: ["devices"] });
    },
  });
}

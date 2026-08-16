import { useMutation } from "@tanstack/react-query";

import {
  updateOrder,
  type UpdateOrderData,
} from "../api/updateOrder";

interface UseUpdateOrderOptions {
  onSuccess?: () => void;
}

export function useUpdateOrder(
  options?: UseUpdateOrderOptions,
) {
  return useMutation({
    mutationFn: ({
      orderId,
      data,
    }: {
      orderId: string;
      data: UpdateOrderData;
    }) => updateOrder(orderId, data),
    onSuccess: options?.onSuccess,
  });
}

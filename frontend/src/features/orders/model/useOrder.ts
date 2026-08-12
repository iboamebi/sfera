import { useQuery } from "@tanstack/react-query";

import { getOrder } from "../api/getOrder";

export function useOrder(orderId: string) {
  return useQuery({
    queryKey: ["orders", orderId],
    queryFn: () => getOrder(orderId),
    enabled: Boolean(orderId),
  });
}

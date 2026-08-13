import { useQuery } from "@tanstack/react-query";

import { getOrders } from "../api/getOrders";

export function useOrders() {
  return useQuery({
    queryKey: ["orders"],
    queryFn: getOrders,
  });
}

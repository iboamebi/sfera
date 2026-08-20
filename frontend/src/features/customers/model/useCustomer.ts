import { useQuery } from "@tanstack/react-query";

import { getCustomer } from "../api/getCustomer";

export function useCustomer(customerId: string) {
  return useQuery({
    queryKey: ["customers", customerId],
    queryFn: () => getCustomer(customerId),
    enabled: Boolean(customerId),
  });
}

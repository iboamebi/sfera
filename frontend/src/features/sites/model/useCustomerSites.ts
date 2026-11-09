import { useQuery } from "@tanstack/react-query";

import { getCustomerSites } from "../api/getCustomerSites";

export function useCustomerSites(customerId: string) {
  return useQuery({
    queryKey: ["sites", "customer", customerId],
    queryFn: () => getCustomerSites(customerId),
    enabled: Boolean(customerId),
  });
}

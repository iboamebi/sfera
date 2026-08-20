import { useQuery } from "@tanstack/react-query";

import { getOrganization } from "../api/getOrganization";

export function useOrganization(organizationId: string) {
  return useQuery({
    queryKey: ["organizations", organizationId],
    queryFn: () => getOrganization(organizationId),
    enabled: Boolean(organizationId),
  });
}

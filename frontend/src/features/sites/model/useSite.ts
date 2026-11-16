import { useQuery } from "@tanstack/react-query";

import { getSite } from "../api/getSite";

export function useSite(siteId: string) {
  return useQuery({
    queryKey: ["sites", siteId],
    queryFn: () => getSite(siteId),
    enabled: Boolean(siteId),
  });
}

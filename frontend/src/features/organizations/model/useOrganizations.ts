import { useQuery } from "@tanstack/react-query";

import { getOrganizations } from "../api/getOrganizations";

export function useOrganizations() {
  return useQuery({
    queryKey: ["organizations"],
    queryFn: getOrganizations,
  });
}

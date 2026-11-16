import { useQuery } from "@tanstack/react-query";

import { getSites } from "../api/getSites";

export function useSites() {
  return useQuery({
    queryKey: ["sites"],
    queryFn: getSites,
  });
}

import { useQuery } from "@tanstack/react-query";

import { getVerifications } from "../api/getVerifications";

export function useVerifications() {
  return useQuery({
    queryKey: ["verifications"],
    queryFn: getVerifications,
  });
}

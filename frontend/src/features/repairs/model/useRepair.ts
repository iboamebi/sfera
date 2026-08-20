import { useQuery } from "@tanstack/react-query";

import { getRepair } from "../api/getRepair";

export function useRepair(repairId: string) {
  return useQuery({
    queryKey: ["repairs", repairId],
    queryFn: () => getRepair(repairId),
    enabled: Boolean(repairId),
  });
}

import { useQuery } from "@tanstack/react-query";

import { getMaterial } from "../api/getMaterial";

export function useMaterial(materialId: string) {
  return useQuery({
    queryKey: ["materials", materialId],
    queryFn: () => getMaterial(materialId),
    enabled: Boolean(materialId),
  });
}

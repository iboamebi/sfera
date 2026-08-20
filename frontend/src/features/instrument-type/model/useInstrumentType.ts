import { useQuery } from "@tanstack/react-query";

import { getInstrumentType } from "../api/getInstrumentType";

export function useInstrumentType(instrumentTypeId: string) {
  return useQuery({
    queryKey: ["instrument-types", instrumentTypeId],
    queryFn: () => getInstrumentType(instrumentTypeId),
    enabled: Boolean(instrumentTypeId),
  });
}

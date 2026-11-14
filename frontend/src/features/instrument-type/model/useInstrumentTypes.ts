import { useQuery } from "@tanstack/react-query";

import { getInstrumentTypes } from "../api/getInstrumentTypes";

export function useInstrumentTypes(enabled = true) {
  return useQuery({
    queryKey: ["instrument-types"],
    enabled,
    queryFn: getInstrumentTypes,
  });
}

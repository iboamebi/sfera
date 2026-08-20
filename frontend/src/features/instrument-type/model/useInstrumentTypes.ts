import { useQuery } from "@tanstack/react-query";

import { getInstrumentTypes } from "../api/getInstrumentTypes";

export function useInstrumentTypes() {
  return useQuery({
    queryKey: ["instrument-types"],
    queryFn: getInstrumentTypes,
  });
}

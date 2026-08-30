import { useQuery } from "@tanstack/react-query";

import { getDevice } from "../api/getDevice";

export function useDevice(deviceId: string | null) {
  return useQuery({
    queryKey: ["devices", deviceId],
    queryFn: () => getDevice(deviceId ?? ""),
    enabled: Boolean(deviceId),
  });
}

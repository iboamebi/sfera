import { useMutation, type UseMutationOptions } from "@tanstack/react-query";

import { updateDevice } from "../api/updateDevice";
import type { DeviceRead, UpdateDeviceInput } from "./types";

export function useUpdateDevice(
  deviceId: string,
  options?: UseMutationOptions<DeviceRead, Error, UpdateDeviceInput>,
) {
  return useMutation({
    mutationFn: (data) => updateDevice(deviceId, data),
    ...options,
  });
}

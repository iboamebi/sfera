import { useMutation, type UseMutationOptions } from "@tanstack/react-query";

import { createDevice } from "../api/createDevice";
import type { DeviceRead } from "./types";

type CreateDeviceInput = {
  instrumentTypeId: string;
  serialNumber: string;
};

export function useCreateDevice(
  options?: UseMutationOptions<DeviceRead, Error, CreateDeviceInput>,
) {
  return useMutation({
    mutationFn: (data: CreateDeviceInput) => createDevice(data),
    ...options,
  });
}

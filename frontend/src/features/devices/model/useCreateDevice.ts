import {
  useMutation,
  useQueryClient,
  type UseMutationOptions,
} from "@tanstack/react-query";

import { createDevice, type CreateDeviceInput } from "../api/createDevice";
import type { DeviceRead } from "./types";

export function useCreateDevice(
  options?: UseMutationOptions<DeviceRead, Error, CreateDeviceInput>,
) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateDeviceInput) => createDevice(data),
    onSuccess: async (...args) => {
      await queryClient.invalidateQueries({ queryKey: ["devices"] });
      await options?.onSuccess?.(...args);
    },
    ...options,
  });
}

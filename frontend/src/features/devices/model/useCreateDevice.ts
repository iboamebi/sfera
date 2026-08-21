import {
  useMutation,
  useQueryClient,
  type UseMutationOptions,
} from "@tanstack/react-query";

import { createDevice } from "../api/createDevice";
import type { DeviceRead } from "./types";

type CreateDeviceInput = {
  instrumentTypeId: string;
  serialNumber: string;
};

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

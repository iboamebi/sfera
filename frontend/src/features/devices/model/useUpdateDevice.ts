import {
  useMutation,
  useQueryClient,
  type UseMutationOptions,
} from "@tanstack/react-query";

import { updateDevice } from "../api/updateDevice";
import type { DeviceRead, UpdateDeviceInput } from "./types";

export function useUpdateDevice(
  deviceId: string,
  options?: UseMutationOptions<DeviceRead, Error, UpdateDeviceInput>,
) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data) => updateDevice(deviceId, data),
    ...options,
    onSuccess: async (data, variables, onMutateResult, context) => {
      queryClient.setQueryData(["devices", deviceId], data);
      await queryClient.invalidateQueries({ queryKey: ["devices"] });
      await options?.onSuccess?.(
        data,
        variables,
        onMutateResult,
        context,
      );
    },
  });
}

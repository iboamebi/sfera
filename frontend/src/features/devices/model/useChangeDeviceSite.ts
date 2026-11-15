import {
  useMutation,
  useQueryClient,
  type UseMutationOptions,
} from "@tanstack/react-query";

import { changeDeviceSite } from "../api/changeDeviceSite";
import type { DeviceRead } from "./types";
import type { ChangeDeviceSiteInput } from "../api/changeDeviceSite";

export function useChangeDeviceSite(
  deviceId: string,
  options?: UseMutationOptions<DeviceRead, Error, ChangeDeviceSiteInput>,
) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data) => changeDeviceSite(deviceId, data),
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

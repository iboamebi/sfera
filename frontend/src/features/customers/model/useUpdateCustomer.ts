import {
  useMutation,
  useQueryClient,
  type UseMutationOptions,
} from "@tanstack/react-query";

import { updateCustomer } from "../api/updateCustomer";
import type { CreateCustomerForm, CustomerRead } from "./types";

export function useUpdateCustomer(
  customerId: string,
  options?: UseMutationOptions<
    CustomerRead,
    Error,
    CreateCustomerForm
  >,
) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data) => updateCustomer(customerId, data),
    ...options,
    onSuccess: async (data, variables, onMutateResult, context) => {
      queryClient.setQueryData(["customers", customerId], data);
      await queryClient.invalidateQueries({ queryKey: ["customers"] });
      await options?.onSuccess?.(
        data,
        variables,
        onMutateResult,
        context,
      );
    },
  });
}

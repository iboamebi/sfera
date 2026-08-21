import { useMutation, type UseMutationOptions } from "@tanstack/react-query";

import { createCustomer } from "../api/createCustomer";
import type { CustomerRead } from "./types";
import type { CreateCustomerForm } from "./types";

export function useCreateCustomer(
  options?: UseMutationOptions<CustomerRead, Error, CreateCustomerForm>,
) {
  return useMutation({
    mutationFn: (data: CreateCustomerForm) => createCustomer(data),
    ...options,
  });
}

import { useMutation, type UseMutationOptions } from "@tanstack/react-query";

import { createOrganization } from "../api/createOrganization";
import type { CreateOrganizationForm, OrganizationRead } from "./types";

export function useCreateOrganization(
  options?: UseMutationOptions<
    OrganizationRead,
    Error,
    CreateOrganizationForm
  >,
) {
  return useMutation({
    mutationFn: (data: CreateOrganizationForm) => createOrganization(data),
    ...options,
  });
}

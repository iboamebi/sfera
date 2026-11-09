import {
  useMutation,
  useQueryClient,
  type UseMutationOptions,
} from "@tanstack/react-query";

import { updateOrganization } from "../api/updateOrganization";
import type { CreateOrganizationForm, OrganizationRead } from "./types";

export function useUpdateOrganization(
  organizationId: string,
  options?: UseMutationOptions<
    OrganizationRead,
    Error,
    CreateOrganizationForm
  >,
) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data) => updateOrganization(organizationId, data),
    ...options,
    onSuccess: async (data, variables, onMutateResult, context) => {
      queryClient.setQueryData(["organizations", organizationId], data);
      await queryClient.invalidateQueries({ queryKey: ["organizations"] });
      await options?.onSuccess?.(
        data,
        variables,
        onMutateResult,
        context,
      );
    },
  });
}

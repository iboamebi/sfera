import { useMutation, type UseMutationOptions } from "@tanstack/react-query";

import { createSite, type CreateSiteInput } from "../api/createSite";
import type { SiteRead } from "./types";

export function useCreateSite(
  options?: UseMutationOptions<SiteRead, Error, CreateSiteInput>,
) {
  return useMutation({
    mutationFn: (data: CreateSiteInput) => createSite(data),
    ...options,
  });
}

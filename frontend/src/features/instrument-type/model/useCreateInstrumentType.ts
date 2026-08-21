import {
  useMutation,
  useQueryClient,
  type UseMutationOptions,
} from "@tanstack/react-query";

import { createInstrumentType } from "../api/createInstrumentType";
import type { InstrumentTypeRead } from "./types";

type CreateInstrumentTypeInput = {
  name: string;
  manufacturer?: string | null;
  model?: string | null;
  measurementType?: string | null;
  accuracyClass?: string | null;
  verificationIntervalMonths?: number | null;
  description?: string | null;
};

export function useCreateInstrumentType(
  options?: UseMutationOptions<
    InstrumentTypeRead,
    Error,
    CreateInstrumentTypeInput
  >,
) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateInstrumentTypeInput) =>
      createInstrumentType(data),
    onSuccess: async (...args) => {
      await queryClient.invalidateQueries({ queryKey: ["instrument-types"] });
      await options?.onSuccess?.(...args);
    },
    ...options,
  });
}

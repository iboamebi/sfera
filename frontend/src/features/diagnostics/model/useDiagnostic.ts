import { useQuery } from "@tanstack/react-query";

import { getDiagnostic } from "../api/getDiagnostic";

export function useDiagnostic(diagnosticId: string) {
  return useQuery({
    queryKey: ["diagnostics", diagnosticId],
    queryFn: () => getDiagnostic(diagnosticId),
    enabled: Boolean(diagnosticId),
  });
}

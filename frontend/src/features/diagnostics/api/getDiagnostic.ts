import { http } from "../../../shared/api/http";
import type { DiagnosticRead } from "../model/types";
import { mapDiagnostic } from "./diagnosticMapper";
import type { DiagnosticApiDto } from "./types";

export async function getDiagnostic(
  diagnosticId: string,
): Promise<DiagnosticRead> {
  const response = await http.get<DiagnosticApiDto>(
    `/diagnostics/${diagnosticId}`,
  );

  return mapDiagnostic(response.data);
}

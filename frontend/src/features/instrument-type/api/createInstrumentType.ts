import { http } from "../../../shared/api/http";
import { mapInstrumentType } from "./instrumentTypeMapper";
import type { InstrumentTypeRead } from "../model/types";
import type { InstrumentTypeApiDto } from "./types";

export interface CreateInstrumentTypeInput {
  name: string;
  manufacturer?: string | null;
  model?: string | null;
  measurement_type?: string | null;
  accuracy_class?: string | null;
  verification_interval_months?: number | null;
  description?: string | null;
}

export async function createInstrumentType(
  data: CreateInstrumentTypeInput,
): Promise<InstrumentTypeRead> {
  const response = await http.post<InstrumentTypeApiDto>(
    "/instrument-types/",
    data,
  );

  return mapInstrumentType(response.data);
}

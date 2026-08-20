import { http } from "../../../shared/api/http";
import { mapInstrumentType } from "./instrumentTypeMapper";
import type { InstrumentTypeRead } from "../model/types";
import type { InstrumentTypeApiDto } from "./types";

export async function getInstrumentTypes(): Promise<InstrumentTypeRead[]> {
  const response = await http.get<InstrumentTypeApiDto[]>(
    "/instrument-types/",
  );

  return response.data.map(mapInstrumentType);
}

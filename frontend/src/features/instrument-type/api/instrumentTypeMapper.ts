import type { InstrumentTypeRead } from "../model/types";
import type { InstrumentTypeApiDto } from "./types";

export function mapInstrumentType(
  dto: InstrumentTypeApiDto,
): InstrumentTypeRead {
  return {
    id: dto.id,
    name: dto.name,
    manufacturer: dto.manufacturer,
    model: dto.model,
    measurementType: dto.measurement_type,
    accuracyClass: dto.accuracy_class,
    verificationIntervalMonths: dto.verification_interval_months,
    description: dto.description,
    archived: dto.archived,
  };
}

export interface InstrumentTypeApiDto {
  id: string;
  name: string;
  manufacturer: string | null;
  model: string | null;
  measurement_type: string | null;
  accuracy_class: string | null;
  verification_interval_months: number | null;
  description: string | null;
  archived: boolean;
}

export interface InstrumentTypeRead {
  id: string;
  name: string;
  manufacturer: string | null;
  model: string | null;
  measurementType: string | null;
  accuracyClass: string | null;
  verificationIntervalMonths: number | null;
  description: string | null;
  archived: boolean;
}

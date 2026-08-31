export interface DeviceApiDto {
  id: string;
  instrument_type_id: string;
  serial_number: string;
  registry_number: string | null;
  modification: string | null;
  factory_number: string | null;
  manufacture_year: number | null;
  inventory_number: string | null;
  comment: string | null;
  status: "AVAILABLE" | "IN_WORK" | "WAITING" | "COMPLETED" | "BLOCKED";
}

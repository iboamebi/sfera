export interface DeviceApiDto {
  id: string;
  instrument_type_id: string;
  customer_id: string;
  site_id: string | null;
  name: string | null;
  serial_number: string;
  registry_number: string | null;
  modification: string | null;
  manufacture_year: number | null;
  inventory_number: string | null;
  comment: string | null;
  status: "AVAILABLE" | "IN_WORK" | "WAITING" | "COMPLETED" | "BLOCKED";
}

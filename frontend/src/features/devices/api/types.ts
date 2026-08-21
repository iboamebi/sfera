export interface DeviceApiDto {
  id: string;
  instrument_type_id: string;
  serial_number: string;
  status: "AVAILABLE" | "IN_WORK" | "WAITING" | "COMPLETED" | "BLOCKED";
}

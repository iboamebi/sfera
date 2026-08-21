export type DeviceStatus =
  | "AVAILABLE"
  | "IN_WORK"
  | "WAITING"
  | "COMPLETED"
  | "BLOCKED";

export interface DeviceRead {
  id: string;
  instrumentTypeId: string;
  serialNumber: string;
  status: DeviceStatus;
}

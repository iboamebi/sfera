export type DeviceStatus =
  | "AVAILABLE"
  | "IN_WORK"
  | "WAITING"
  | "COMPLETED"
  | "BLOCKED";

export interface DeviceRead {
  id: string;
  instrumentTypeId: string;
  name: string | null;
  serialNumber: string;
  registryNumber: string | null;
  modification: string | null;
  manufactureYear: number | null;
  inventoryNumber: string | null;
  comment: string | null;
  status: DeviceStatus;
}

export interface UpdateDeviceInput {
  name: string;
  serialNumber: string;
  registryNumber: string | null;
  modification: string | null;
  manufactureYear: number | null;
  inventoryNumber: string | null;
  comment: string | null;
}

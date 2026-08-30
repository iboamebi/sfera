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
  registryNumber: string | null;
  modification: string | null;
  factoryNumber: string | null;
  manufactureYear: number | null;
  inventoryNumber: string | null;
  comment: string | null;
}

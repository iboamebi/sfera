export type OrderItemOperation =
  | "verification"
  | "diagnostic"
  | "repair"
  | "sale";

export interface OrderItem {
  id: string;
  instrumentId: string | null;
  instrumentTypeId: string | null;
  instrumentTypeName: string | null;
  instrumentTypeModel: string | null;
  instrumentTypeMeasurementType: string | null;
  serialNumber: string | null;
  registryNumber: string | null;
  modification: string | null;
  factoryNumber: string | null;
  manufactureYear: number | null;
  inventoryNumber: string | null;
  comment: string | null;
  requestedOperations: OrderItemOperation[];
}

export interface OrderRead {
  id: string;
  number: string;
  customerId: string;
  status: string;
  receivedAt: string;
  plannedIssueAt: string | null;
  issuedAt: string | null;
  comment: string | null;
  archived: boolean;
  items: OrderItem[];
}

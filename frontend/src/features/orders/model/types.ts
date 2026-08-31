export type OrderItemOperation =
  | "verification"
  | "diagnostic"
  | "repair"
  | "sale";

export interface OrderItem {
  id: string;
  instrumentId: string | null;
  instrumentTypeId: string | null;
  instrumentName: string | null;
  instrumentTypeName: string | null;
  serialNumber: string | null;
  modification: string | null;
  comment: string | null;
  requestedOperations: OrderItemOperation[];
}

export interface OrderRead {
  id: string;
  number: string;
  customerId: string;
  status: string;
  receivedAt: string;
  createdAt: string;
  updatedAt: string;
  plannedIssueAt: string | null;
  issuedAt: string | null;
  comment: string | null;
  archived: boolean;
  items: OrderItem[];
}

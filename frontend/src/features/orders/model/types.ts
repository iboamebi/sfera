export type OrderItemOperation =
  | "verification"
  | "diagnostic"
  | "repair"
  | "sale";

export interface OrderItemVerification {
  id: string;
  createdAt: string;
  verificationDate: string;
  verificationType: "PRIMARY" | "PERIODIC" | "AFTER_REPAIR";
  status: "CREATED" | "IN_PROGRESS" | "DECIDED" | "CANCELLED";
  result: "SUITABLE" | "UNSUITABLE" | null;
  validUntil: string | null;
  archived: boolean;
}

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
  verificationIds: string[];
  verifications: OrderItemVerification[];
}

export interface OrderRead {
  id: string;
  number: string;
  customerId: string;
  customerName: string;
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

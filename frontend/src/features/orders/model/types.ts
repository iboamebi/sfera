export interface OrderItem {
  id: string;
  instrumentId: string | null;
  instrumentTypeName: string | null;
  serialNumber: string | null;
  comment: string | null;
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

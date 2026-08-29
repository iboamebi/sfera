export interface CreateOrderForm {
  number: string;
  customerId: string;
  plannedIssueAt?: string;
  comment?: string;
  instrumentIds: string[];
}

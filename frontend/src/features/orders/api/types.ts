export interface OrderItemApiDto {
  id: string;
  instrument_id: string | null;
  comment: string | null;
}

export interface OrderApiDto {
  id: string;
  number: string;
  customer_id: string;
  status: string;
  received_at: string;
  planned_issue_at: string | null;
  issued_at: string | null;
  comment: string | null;
  archived: boolean;
  items: OrderItemApiDto[];
}

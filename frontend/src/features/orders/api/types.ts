import type { OrderItemOperation } from "../model/types";

export interface OrderItemApiDto {
  id: string;
  instrument_id: string | null;
  instrument_type_name: string | null;
  serial_number: string | null;
  comment: string | null;
  requested_operations: OrderItemOperation[];
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

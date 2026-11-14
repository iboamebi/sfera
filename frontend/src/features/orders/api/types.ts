import type { OrderItemOperation } from "../model/types";

export interface OrderItemVerificationApiDto {
  id: string;
  created_at: string;
  verification_date: string;
  verification_type: "PRIMARY" | "PERIODIC" | "AFTER_REPAIR";
  status: "CREATED" | "IN_PROGRESS" | "DECIDED";
  result: "SUITABLE" | "UNSUITABLE" | null;
  valid_until: string | null;
  archived: boolean;
}

export interface OrderItemApiDto {
  id: string;
  instrument_id: string | null;
  instrument_type_id: string | null;
  instrument_name: string | null;
  instrument_type_name: string | null;
  serial_number: string | null;
  modification: string | null;
  comment: string | null;
  requested_operations: OrderItemOperation[];
  verification_ids: string[];
  verifications: OrderItemVerificationApiDto[];
}

export interface OrderApiDto {
  id: string;
  number: string;
  customer_id: string;
  customer_name: string;
  status: string;
  received_at: string;
  created_at: string;
  updated_at: string;
  planned_issue_at: string | null;
  issued_at: string | null;
  comment: string | null;
  archived: boolean;
  items: OrderItemApiDto[];
}

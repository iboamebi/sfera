export interface VerificationApiDto {
  id: string;
  order_item_id: string;
  instrument_id: string | null;
  verification_date: string;
  valid_until: string | null;
  result: "SUITABLE" | "UNSUITABLE" | null;
  unsuitable_reason: string | null;
  cancellation_reason: string | null;
  methodology: string | null;
  created_at: string;
  started_at: string | null;
  decision_at: string | null;
  status: "CREATED" | "IN_PROGRESS" | "DECIDED" | "CANCELLED";
  verification_type: "PRIMARY" | "PERIODIC" | "AFTER_REPAIR";
  archived: boolean;
}

export interface VerificationListApiDto {
  id: string;
  order_item_id: string;
  order_id: string;
  order_number: string;
  customer_id: string;
  customer_name: string;
  instrument_id: string | null;
  instrument_name: string | null;
  instrument_type_id: string | null;
  instrument_type_name: string | null;
  serial_number: string | null;
  verification_date: string;
  verification_type: "PRIMARY" | "PERIODIC" | "AFTER_REPAIR";
  status: "CREATED" | "IN_PROGRESS" | "DECIDED" | "CANCELLED";
  result: "SUITABLE" | "UNSUITABLE" | null;
  valid_until: string | null;
  created_at: string;
  started_at: string | null;
  decision_at: string | null;
  archived: boolean;
}

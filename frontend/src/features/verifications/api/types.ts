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

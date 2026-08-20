export interface VerificationApiDto {
  id: string;
  order_item_id: string;
  verification_date: string;
  valid_until: string | null;
  result: string;
  unsuitable_reason: string | null;
  methodology: string | null;
  archived: boolean;
}

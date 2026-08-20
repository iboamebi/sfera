export interface DiagnosticApiDto {
  id: string;
  order_item_id: string;
  conclusion: string | null;
  recommendation: string | null;
}

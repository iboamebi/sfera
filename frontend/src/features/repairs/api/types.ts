export interface RepairApiDto {
  id: string;
  order_item_id: string;
  status: string;
  description: string | null;
  result: string | null;
}

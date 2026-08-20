export interface RepairRead {
  id: string;
  orderItemId: string;
  status: string;
  description: string | null;
  result: string | null;
}

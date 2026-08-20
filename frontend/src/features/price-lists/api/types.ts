export interface PriceListApiDto {
  id: string;
  name: string;
  price_list_type: string;
  currency: string;
  description: string | null;
  valid_from: string | null;
  valid_to: string | null;
  is_active: boolean;
  archived: boolean;
}

export interface PriceListRead {
  id: string;
  name: string;
  priceListType: string;
  currency: string;
  description: string | null;
  validFrom: string | null;
  validTo: string | null;
  isActive: boolean;
  archived: boolean;
}

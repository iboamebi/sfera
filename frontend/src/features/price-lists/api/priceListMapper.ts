import type { PriceListRead } from "../model/types";
import type { PriceListApiDto } from "./types";

export function mapPriceList(dto: PriceListApiDto): PriceListRead {
  return {
    id: dto.id,
    name: dto.name,
    priceListType: dto.price_list_type,
    currency: dto.currency,
    description: dto.description,
    validFrom: dto.valid_from,
    validTo: dto.valid_to,
    isActive: dto.is_active,
    archived: dto.archived,
  };
}

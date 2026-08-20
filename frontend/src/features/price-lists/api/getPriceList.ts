import { http } from "../../../shared/api/http";
import type { PriceListRead } from "../model/types";
import { mapPriceList } from "./priceListMapper";
import type { PriceListApiDto } from "./types";

export async function getPriceList(
  priceListId: string,
): Promise<PriceListRead> {
  const response = await http.get<PriceListApiDto>(
    `/price-lists/${priceListId}`,
  );

  return mapPriceList(response.data);
}

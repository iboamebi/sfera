import { useQuery } from "@tanstack/react-query";

import { getPriceList } from "../api/getPriceList";

export function usePriceList(priceListId: string) {
  return useQuery({
    queryKey: ["price-lists", priceListId],
    queryFn: () => getPriceList(priceListId),
    enabled: Boolean(priceListId),
  });
}

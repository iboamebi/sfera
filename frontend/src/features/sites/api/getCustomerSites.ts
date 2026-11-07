import { http } from "../../../shared/api/http";
import { mapSite } from "./siteMapper";
import type { SiteApiDto } from "./types";
import type { SiteRead } from "../model/types";

export async function getCustomerSites(customerId: string): Promise<SiteRead[]> {
  const response = await http.get<SiteApiDto[]>(
    `/sites/customer/${customerId}`,
  );

  return response.data.map(mapSite);
}

import { http } from "../../../shared/api/http";
import { mapSite } from "./siteMapper";
import type { SiteRead } from "../model/types";
import type { SiteApiDto } from "./types";

export interface CreateSiteInput {
  customerId: string;
  name: string;
  address: string;
}

export async function createSite(input: CreateSiteInput): Promise<SiteRead> {
  const response = await http.post<SiteApiDto>("/sites/", {
    customer_id: input.customerId,
    name: input.name,
    address: input.address,
  });

  return mapSite(response.data);
}

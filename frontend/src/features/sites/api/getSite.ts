import { http } from "../../../shared/api/http";
import type { SiteRead } from "../model/types";
import { mapSite } from "./siteMapper";
import type { SiteApiDto } from "./types";

export async function getSite(siteId: string): Promise<SiteRead> {
  const response = await http.get<SiteApiDto>(`/sites/${siteId}`);

  return mapSite(response.data);
}

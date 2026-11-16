import { http } from "../../../shared/api/http";
import type { SiteRead } from "../model/types";
import { mapSite } from "./siteMapper";
import type { SiteApiDto } from "./types";

export async function getSites(): Promise<SiteRead[]> {
  const response = await http.get<SiteApiDto[]>("/sites/");

  return response.data.map(mapSite);
}

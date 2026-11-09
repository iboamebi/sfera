import type { SiteRead } from "../model/types";
import type { SiteApiDto } from "./types";

export function mapSite(dto: SiteApiDto): SiteRead {
  return {
    id: dto.id,
    customerId: dto.customer_id,
    name: dto.name,
    address: dto.address,
    archived: dto.archived,
  };
}

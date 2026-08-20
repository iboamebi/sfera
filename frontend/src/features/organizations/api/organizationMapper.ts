import type { OrganizationApiDto } from "./types";
import type { OrganizationRead } from "../model/types";

export function mapOrganization(dto: OrganizationApiDto): OrganizationRead {
  return {
    id: dto.id,
    name: dto.name,
    shortName: dto.short_name,
    inn: dto.inn,
    kpp: dto.kpp,
    ogrn: dto.ogrn,
    address: dto.address,
    phone: dto.phone,
    email: dto.email,
    website: dto.website,
    comment: dto.comment,
  };
}

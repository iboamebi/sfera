import { http } from "../../../shared/api/http";
import type { OrganizationRead } from "../model/types";
import { mapOrganization } from "./organizationMapper";
import type { OrganizationApiDto } from "./types";
import type { CreateOrganizationForm } from "../model/types";

export async function createOrganization(
  data: CreateOrganizationForm,
): Promise<OrganizationRead> {
  const response = await http.post<OrganizationApiDto>("/organizations/", {
    name: data.name,
    short_name: data.shortName?.trim() || null,
    inn: data.inn?.trim() || null,
    kpp: data.kpp?.trim() || null,
    ogrn: data.ogrn?.trim() || null,
    address: data.address?.trim() || null,
    phone: data.phone?.trim() || null,
    email: data.email?.trim() || null,
    website: data.website?.trim() || null,
    comment: data.comment?.trim() || null,
  });

  return mapOrganization(response.data);
}

import { http } from "../../../shared/api/http";
import type { OrganizationRead, CreateOrganizationForm } from "../model/types";
import { mapOrganization } from "./organizationMapper";
import type { OrganizationApiDto } from "./types";

export async function updateOrganization(
  organizationId: string,
  data: CreateOrganizationForm,
): Promise<OrganizationRead> {
  const response = await http.patch<OrganizationApiDto>(
    `/organizations/${organizationId}`,
    {
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
    },
  );

  return mapOrganization(response.data);
}

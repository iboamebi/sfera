import { http } from "../../../shared/api/http";
import type { OrganizationRead } from "../model/types";
import { mapOrganization } from "./organizationMapper";
import type { OrganizationApiDto } from "./types";

export async function getOrganization(
  organizationId: string,
): Promise<OrganizationRead> {
  const response = await http.get<OrganizationApiDto>(
    `/organizations/${organizationId}`,
  );

  return mapOrganization(response.data);
}

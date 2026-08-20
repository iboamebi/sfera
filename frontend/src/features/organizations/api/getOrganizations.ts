import { http } from "../../../shared/api/http";
import type { OrganizationRead } from "../model/types";
import { mapOrganization } from "./organizationMapper";
import type { OrganizationApiDto } from "./types";

export async function getOrganizations(): Promise<OrganizationRead[]> {
  const response = await http.get<OrganizationApiDto[]>("/organizations/");

  return response.data.map(mapOrganization);
}

import { http } from "../../../shared/api/http";
import { mapAuthenticatedUser } from "./mapAuthenticatedUser";
import type { AuthenticatedUserDto } from "./mapAuthenticatedUser";
import type { CurrentUser } from "../model/types";

export async function getCurrentUser(): Promise<CurrentUser> {
  const response = await http.get<AuthenticatedUserDto>("/auth/me");

  return mapAuthenticatedUser(response.data);
}

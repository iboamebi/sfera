import { http } from "../../../shared/api/http";
import type { CurrentUser } from "../model/types";

export async function getCurrentUser(): Promise<CurrentUser> {
  const response = await http.get<CurrentUser>("/auth/me");

  return response.data;
}

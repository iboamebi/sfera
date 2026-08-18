import { http } from "../../../shared/api/http";
import type { AuthenticatedUser } from "../model/types";

type LoginRequest = {
  username: string;
  password: string;
};

export async function login(data: LoginRequest): Promise<AuthenticatedUser> {
  const response = await http.post<AuthenticatedUser>("/auth/login", data);

  return response.data;
}

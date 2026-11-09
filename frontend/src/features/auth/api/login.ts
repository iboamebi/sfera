import { http } from "../../../shared/api/http";
import { mapAuthenticatedUser } from "./mapAuthenticatedUser";
import type { AuthenticatedUserDto } from "./mapAuthenticatedUser";
import type { AuthenticatedUser } from "../model/types";

type LoginRequest = {
  username: string;
  password: string;
};

export async function login(data: LoginRequest): Promise<AuthenticatedUser> {
  const response = await http.post<AuthenticatedUserDto>("/auth/login", data);

  return mapAuthenticatedUser(response.data);
}

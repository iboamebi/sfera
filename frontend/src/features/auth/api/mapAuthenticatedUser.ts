import type { AuthenticatedUser } from "../model/types";

export interface AuthenticatedUserDto {
  id: string;
  username: string;
  role: AuthenticatedUser["role"];
  must_change_password: boolean;
}

export function mapAuthenticatedUser(
  dto: AuthenticatedUserDto,
): AuthenticatedUser {
  return {
    id: dto.id,
    username: dto.username,
    role: dto.role,
    mustChangePassword: dto.must_change_password,
  };
}

import type { UserRole } from "../model/types";

export interface UserApiDto {
  id: string;
  username: string;
  role: UserRole;
  is_active: boolean;
  archived: boolean;
  must_change_password: boolean;
}

export interface UserCreatedApiDto extends UserApiDto {
  temporary_password: string;
}

export interface UserCreateApiRequest {
  username: string;
  role: UserRole;
}

export interface UserRoleApiRequest {
  role: UserRole;
}

export interface UserActiveApiRequest {
  is_active: boolean;
}

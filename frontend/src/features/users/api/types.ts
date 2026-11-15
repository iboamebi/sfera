import type { UserRole } from "../model/types";

export interface UserApiDto {
  id: string;
  username: string;
  full_name: string | null;
  phone: string | null;
  position: string | null;
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
  full_name: string;
  phone: string | null;
  position: string | null;
  role: UserRole;
}

export interface UserProfileApiRequest {
  full_name: string;
  phone: string | null;
  position: string | null;
}

export interface UserRoleApiRequest {
  role: UserRole;
}

export interface UserActiveApiRequest {
  is_active: boolean;
}

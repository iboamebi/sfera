export type UserRole =
  | "admin"
  | "operator"
  | "metrologist"
  | "technician"
  | "warehouse";

export interface UserRead {
  id: string;
  username: string;
  fullName: string | null;
  phone: string | null;
  position: string | null;
  role: UserRole;
  isActive: boolean;
  archived: boolean;
  mustChangePassword: boolean;
}

export interface UserProfileInput {
  fullName: string;
  phone: string;
  position: string;
}

export interface UserCreateInput extends UserProfileInput {
  username: string;
  role: UserRole;
}

export interface UserCreated extends UserRead {
  temporaryPassword: string;
}

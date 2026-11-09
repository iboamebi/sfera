export type UserRole =
  | "admin"
  | "operator"
  | "metrologist"
  | "technician"
  | "warehouse";

export interface UserRead {
  id: string;
  username: string;
  role: UserRole;
  isActive: boolean;
  archived: boolean;
  mustChangePassword: boolean;
}

export interface UserCreated extends UserRead {
  temporaryPassword: string;
}

export type UserRole =
  | "admin"
  | "operator"
  | "metrologist"
  | "technician"
  | "warehouse";

export interface AuthenticatedUser {
  id: string;
  username: string;
  role: UserRole;
  mustChangePassword: boolean;
}

export type CurrentUser = AuthenticatedUser;

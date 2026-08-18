export interface AuthenticatedUser {
  id: string;
  username: string;
}

export type CurrentUser = AuthenticatedUser;

import type { ReactNode } from "react";
import { useCurrentUser } from "./useCurrentUser";

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  useCurrentUser();

  return children;
}

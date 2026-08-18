import type { ReactNode } from "react";
import { Navigate, useLocation } from "react-router";

import { useCurrentUser } from "../model/useCurrentUser";

interface RequireAuthProps {
  children: ReactNode;
}

export function RequireAuth({ children }: RequireAuthProps) {
  const location = useLocation();
  const { data: user, isPending, isError } = useCurrentUser();

  if (isPending) {
    return null;
  }

  if (isError || !user) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  return children;
}

import type { ReactNode } from "react";
import { Navigate, useLocation } from "react-router";

import { useCurrentUser } from "../model/useCurrentUser";

interface RequireAuthProps {
  children: ReactNode;
}

const PASSWORD_CHANGE_PATH = "/change-password";

export function RequireAuth({ children }: RequireAuthProps) {
  const location = useLocation();
  const { data: user, isPending, isError } = useCurrentUser();

  if (isPending) {
    return null;
  }

  if (isError || !user) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  if (user.mustChangePassword && location.pathname !== PASSWORD_CHANGE_PATH) {
    return <Navigate to={PASSWORD_CHANGE_PATH} replace />;
  }

  if (!user.mustChangePassword && location.pathname === PASSWORD_CHANGE_PATH) {
    return <Navigate to="/orders" replace />;
  }

  return children;
}

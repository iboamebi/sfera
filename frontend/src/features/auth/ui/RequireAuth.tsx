import type { ReactNode } from "react";
import { Navigate, useLocation } from "react-router";

import { useCurrentUser } from "../model/useCurrentUser";
import { AppShell } from "../../app/AppShell";

interface RequireAuthProps {
  children: ReactNode;
  adminOnly?: boolean;
}

const PASSWORD_CHANGE_PATH = "/change-password";

export function RequireAuth({ children, adminOnly = false }: RequireAuthProps) {
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

  if (adminOnly && user.role !== "admin") {
    return <Navigate to="/orders" replace />;
  }

  if (location.pathname === PASSWORD_CHANGE_PATH) {
    return children;
  }

  return <AppShell user={user}>{children}</AppShell>;
}

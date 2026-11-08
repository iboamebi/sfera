import type { ReactNode } from "react";
import { Alert, AppBar, Box, Button, Stack, Toolbar, Typography } from "@mui/material";
import { Link, useLocation, useNavigate } from "react-router";

import { useLogout } from "../features/auth/model/useLogout";
import type { AuthenticatedUser } from "../features/auth/model/types";

interface AppShellProps {
  user: AuthenticatedUser;
  children: ReactNode;
}

const navigation = [
  { label: "Заказы", path: "/orders" },
  { label: "Клиенты", path: "/customers" },
  { label: "Организации", path: "/organizations" },
  { label: "СИ", path: "/devices" },
  { label: "Материалы", path: "/materials" },
];

export function AppShell({ user, children }: AppShellProps) {
  const location = useLocation();
  const navigate = useNavigate();
  const logout = useLogout();

  const handleLogout = () => {
    logout.mutate(undefined, {
      onSuccess: () => navigate("/login", { replace: true }),
    });
  };

  return (
    <Box sx={{ minHeight: "100vh" }}>
      <AppBar position="static">
        <Toolbar sx={{ gap: 2, flexWrap: "wrap", py: 1 }}>
          <Typography variant="h6" sx={{ mr: 1 }}>
            Sfera
          </Typography>

          <Stack
            direction="row"
            spacing={0.5}
            useFlexGap
            sx={{ flexWrap: "wrap", flex: 1 }}
          >
            {navigation.map(({ label, path }) => {
              const active = location.pathname === path || location.pathname.startsWith(`${path}/`);

              return (
                <Button
                  key={path}
                  component={Link}
                  to={path}
                  color="inherit"
                  variant={active ? "outlined" : "text"}
                  aria-current={active ? "page" : undefined}
                  sx={{ textTransform: "none" }}
                >
                  {label}
                </Button>
              );
            })}

            {user.role === "admin" && (
              <Button
                component={Link}
                to="/users"
                color="inherit"
                variant={
                  location.pathname === "/users" ||
                  location.pathname.startsWith("/users/")
                    ? "outlined"
                    : "text"
                }
                aria-current={location.pathname === "/users" ? "page" : undefined}
                sx={{ textTransform: "none" }}
              >
                Пользователи
              </Button>
            )}
          </Stack>

          <Stack direction="row" spacing={1} sx={{ alignItems: "center" }}>
            <Typography variant="body2" sx={{ whiteSpace: "nowrap" }}>
              {user.username}
            </Typography>
            <Button
              color="inherit"
              size="small"
              disabled={logout.isPending}
              onClick={handleLogout}
            >
              {logout.isPending ? "Выход..." : "Выйти"}
            </Button>
          </Stack>
        </Toolbar>
      </AppBar>

      {logout.isError && (
        <Alert severity="error" sx={{ borderRadius: 0 }}>
          Не удалось завершить сеанс. Проверьте соединение и повторите попытку.
        </Alert>
      )}

      <Box
        component="main"
        sx={{
          width: "100%",
          maxWidth: 1600,
          mx: "auto",
          p: { xs: 2, md: 3 },
        }}
      >
        {children}
      </Box>
    </Box>
  );
}

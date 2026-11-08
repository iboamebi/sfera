import type { ReactNode } from "react";
import { AppBar, Box, Button, Stack, Toolbar, Typography } from "@mui/material";
import { Link, useLocation } from "react-router";

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

          <Typography variant="body2" sx={{ whiteSpace: "nowrap" }}>
            {user.username}
          </Typography>
        </Toolbar>
      </AppBar>

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

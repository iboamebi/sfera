import { useEffect, useRef, useState, type ReactNode } from "react";
import { Alert, AppBar, Box, Button, Fab, Stack, Toolbar, Typography } from "@mui/material";
import { isAxiosError } from "axios";
import { useQueryClient } from "@tanstack/react-query";
import { Link, useLocation, useNavigate } from "react-router";

import { http } from "../shared/api/http";
import { useLogout } from "../features/auth/model/useLogout";
import type { AuthenticatedUser } from "../features/auth/model/types";

interface AppShellProps {
  user: AuthenticatedUser;
  children: ReactNode;
}

const INACTIVITY_TIMEOUT_MS = 60 * 60 * 1000;
const ACTIVITY_HEARTBEAT_INTERVAL_MS = 5 * 60 * 1000;

const navigation = [
  { label: "Обзор", path: "/" },
  { label: "Заказы", path: "/orders" },
  { label: "Поверки", path: "/verifications" },
  { label: "Клиенты", path: "/customers" },
  { label: "Узлы", path: "/sites" },
  { label: "Организации", path: "/organizations" },
  { label: "СИ", path: "/devices" },
  { label: "Материалы", path: "/materials" },
];

export function AppShell({ user, children }: AppShellProps) {
  const location = useLocation();
  const navigate = useNavigate();
  const logout = useLogout();
  const [showScrollTop, setShowScrollTop] = useState(false);

  const queryClient = useQueryClient();
  const lastActivityAt = useRef(Date.now());
  const lastHeartbeatAt = useRef(0);

  useEffect(() => {
    let inactivityTimer: ReturnType<typeof setTimeout>;
    let heartbeatTimer: ReturnType<typeof setTimeout>;
    let heartbeatInFlight = false;
    let activityVersion = 0;
    let heartbeatVersion = 0;
    let lastHeartbeatAt = 0;

    const expireSession = () => {
      queryClient.clear();
      navigate("/login", { replace: true });
    };

    const scheduleInactivityCheck = () => {
      window.clearTimeout(inactivityTimer);
      const remaining = INACTIVITY_TIMEOUT_MS - (Date.now() - lastActivityAt.current);
      inactivityTimer = window.setTimeout(expireSession, Math.max(remaining, 0));
    };

    const scheduleHeartbeat = (retryDelay = 0) => {
      if (activityVersion <= heartbeatVersion || heartbeatInFlight) {
        return;
      }

      window.clearTimeout(heartbeatTimer);
      const throttleDelay = Math.max(
        lastHeartbeatAt + ACTIVITY_HEARTBEAT_INTERVAL_MS - Date.now(),
        0,
      );
      heartbeatTimer = window.setTimeout(
        () => sendHeartbeat(),
        Math.max(throttleDelay, retryDelay),
      );
    };

    const sendHeartbeat = () => {
      if (heartbeatInFlight || activityVersion <= heartbeatVersion) {
        return;
      }

      const sentActivityVersion = activityVersion;
      heartbeatInFlight = true;

      void http.post("/auth/activity")
        .then(() => {
          heartbeatVersion = sentActivityVersion;
          lastHeartbeatAt = Date.now();
          scheduleHeartbeat();
        })
        .catch((error: unknown) => {
          if (isAxiosError(error) && error.response?.status === 401) {
            expireSession();
            return;
          }
          scheduleHeartbeat(30_000);
        })
        .finally(() => {
          heartbeatInFlight = false;
          scheduleHeartbeat();
        });
    };

    const recordActivity = () => {
      const now = Date.now();

      if (now - lastActivityAt.current >= INACTIVITY_TIMEOUT_MS) {
        expireSession();
        return;
      }

      lastActivityAt.current = now;
      activityVersion += 1;
      scheduleInactivityCheck();
      scheduleHeartbeat();
    };

    const events: (keyof WindowEventMap)[] = [
      "pointerdown",
      "keydown",
      "scroll",
      "touchstart",
      "mousemove",
    ];

    events.forEach((event) =>
      window.addEventListener(event, recordActivity, { passive: true }),
    );
    recordActivity();

    return () => {
      window.clearTimeout(inactivityTimer);
      window.clearTimeout(heartbeatTimer);
      events.forEach((event) => window.removeEventListener(event, recordActivity));
    };
  }, [navigate, queryClient]);

  useEffect(() => {
    const updateScrollTopVisibility = () => {
      setShowScrollTop(window.scrollY > 400);
    };

    updateScrollTopVisibility();
    window.addEventListener("scroll", updateScrollTopVisibility, { passive: true });
    return () => window.removeEventListener("scroll", updateScrollTopVisibility);
  }, []);

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
                to="/audit"
                color="inherit"
                variant={location.pathname === "/audit" ? "outlined" : "text"}
                aria-current={location.pathname === "/audit" ? "page" : undefined}
                sx={{ textTransform: "none" }}
              >
                Журнал аудита
              </Button>
            )}

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

      {showScrollTop && (
        <Fab
          color="primary"
          size="medium"
          aria-label="Наверх"
          onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
          sx={{ position: "fixed", right: 24, bottom: 24, zIndex: 1200 }}
        >
          ↑
        </Fab>
      )}
    </Box>
  );
}

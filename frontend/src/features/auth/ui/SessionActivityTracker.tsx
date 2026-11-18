import { useEffect, useRef } from "react";
import { isAxiosError } from "axios";
import { useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "react-router";

import { http } from "../../../shared/api/http";

const INACTIVITY_TIMEOUT_MS = 60 * 60 * 1000;
const ACTIVITY_HEARTBEAT_INTERVAL_MS = 5 * 60 * 1000;

/** Enforce the idle timeout and persist user activity for every authenticated route. */
export function SessionActivityTracker() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const lastActivityAt = useRef(Date.now());

  useEffect(() => {
    let inactivityTimer: ReturnType<typeof setTimeout>;
    let heartbeatTimer: ReturnType<typeof setTimeout>;
    let heartbeatInFlight = false;
    let heartbeatRetryDelay = 0;
    let sessionExpired = false;
    let activityVersion = 0;
    let heartbeatVersion = 0;
    let lastHeartbeatAt = 0;

    const expireSession = () => {
      if (sessionExpired) return;
      sessionExpired = true;
      queryClient.clear();
      navigate("/login", { replace: true });
    };

    const scheduleInactivityCheck = () => {
      window.clearTimeout(inactivityTimer);
      const remaining = INACTIVITY_TIMEOUT_MS - (Date.now() - lastActivityAt.current);
      inactivityTimer = window.setTimeout(expireSession, Math.max(remaining, 0));
    };

    const scheduleHeartbeat = (retryDelay = 0) => {
      if (sessionExpired || activityVersion <= heartbeatVersion || heartbeatInFlight) {
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
      if (sessionExpired || heartbeatInFlight || activityVersion <= heartbeatVersion) {
        return;
      }

      const sentActivityVersion = activityVersion;
      heartbeatInFlight = true;

      void http.post("/auth/activity")
        .then(() => {
          heartbeatVersion = sentActivityVersion;
          lastHeartbeatAt = Date.now();
          heartbeatRetryDelay = 0;
        })
        .catch((error: unknown) => {
          if (isAxiosError(error) && error.response?.status === 401) {
            expireSession();
            return;
          }
          heartbeatRetryDelay = 30_000;
        })
        .finally(() => {
          heartbeatInFlight = false;
          scheduleHeartbeat(heartbeatRetryDelay);
          heartbeatRetryDelay = 0;
        });
    };

    const recordActivity = () => {
      if (sessionExpired) return;
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

  return null;
}

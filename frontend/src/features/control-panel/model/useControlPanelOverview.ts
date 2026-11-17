import { useQuery } from "@tanstack/react-query";

import { getControlPanelOverview } from "../api/getControlPanelOverview";

export function useControlPanelOverview() {
  return useQuery({
    queryKey: ["control-panel", "overview"],
    queryFn: getControlPanelOverview,
  });
}

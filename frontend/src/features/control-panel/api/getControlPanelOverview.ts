import { http } from "../../../shared/api/http";
import type { ControlPanelOverview } from "../model/types";

export async function getControlPanelOverview(): Promise<ControlPanelOverview> {
  const response = await http.get<ControlPanelOverview>("/control-panel/overview");
  return response.data;
}

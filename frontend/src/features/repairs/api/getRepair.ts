import { http } from "../../../shared/api/http";
import type { RepairRead } from "../model/types";
import { mapRepair } from "./repairMapper";
import type { RepairApiDto } from "./types";

export async function getRepair(repairId: string): Promise<RepairRead> {
  const response = await http.get<RepairApiDto>(`/repairs/${repairId}`);

  return mapRepair(response.data);
}

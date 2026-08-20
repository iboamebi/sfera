import type { RepairRead } from "../model/types";
import type { RepairApiDto } from "./types";

export function mapRepair(dto: RepairApiDto): RepairRead {
  return {
    id: dto.id,
    orderItemId: dto.order_item_id,
    status: dto.status,
    description: dto.description,
    result: dto.result,
  };
}

import type { DeviceRead } from "../model/types";
import type { DeviceApiDto } from "./types";

export function mapDevice(dto: DeviceApiDto): DeviceRead {
  return {
    id: dto.id,
    instrumentTypeId: dto.instrument_type_id,
    name: dto.name,
    serialNumber: dto.serial_number,
    registryNumber: dto.registry_number,
    modification: dto.modification,
    manufactureYear: dto.manufacture_year,
    inventoryNumber: dto.inventory_number,
    comment: dto.comment,
    status: dto.status,
  };
}

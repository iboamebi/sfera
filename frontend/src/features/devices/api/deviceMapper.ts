import type { DeviceRead } from "../model/types";
import type { DeviceApiDto } from "./types";

export function mapDevice(dto: DeviceApiDto): DeviceRead {
  return {
    id: dto.id,
    instrumentTypeId: dto.instrument_type_id,
    serialNumber: dto.serial_number,
    status: dto.status,
    registryNumber: dto.registry_number ?? null,
    modification: dto.modification ?? null,
    factoryNumber: dto.factory_number ?? null,
    manufactureYear: dto.manufacture_year ?? null,
    inventoryNumber: dto.inventory_number ?? null,
    comment: dto.comment ?? null,
  };
}

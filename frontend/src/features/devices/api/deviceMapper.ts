import type { DeviceRead } from "../model/types";
import type { DeviceApiDto } from "./types";

export function mapDevice(dto: DeviceApiDto): DeviceRead {
  return {
    id: dto.id,
    instrumentTypeId: dto.instrument_type_id,
    serialNumber: dto.serial_number,
    status: dto.status,
  };
}

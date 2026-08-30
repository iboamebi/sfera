import { http } from "../../../shared/api/http";
import { mapDevice } from "./deviceMapper";
import type { DeviceRead } from "../model/types";
import type { DeviceApiDto } from "./types";

type UpdateDeviceInput = {
  deviceId: string;
  instrumentTypeId: string;
  serialNumber: string;
  registryNumber?: string | null;
  modification?: string | null;
  factoryNumber?: string | null;
  manufactureYear?: number | null;
  inventoryNumber?: string | null;
  comment?: string | null;
};

export async function updateDevice(
  input: UpdateDeviceInput,
): Promise<DeviceRead> {
  const response = await http.put<DeviceApiDto>(`/devices/${input.deviceId}`, {
    instrument_type_id: input.instrumentTypeId,
    serial_number: input.serialNumber,
    registry_number: input.registryNumber,
    modification: input.modification,
    factory_number: input.factoryNumber,
    manufacture_year: input.manufactureYear,
    inventory_number: input.inventoryNumber,
    comment: input.comment,
  });

  return mapDevice(response.data);
}

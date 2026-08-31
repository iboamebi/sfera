import { http } from "../../../shared/api/http";
import { mapDevice } from "./deviceMapper";
import type { UpdateDeviceInput, DeviceRead } from "../model/types";
import type { DeviceApiDto } from "./types";

export async function updateDevice(
  deviceId: string,
  data: UpdateDeviceInput,
): Promise<DeviceRead> {
  const response = await http.put<DeviceApiDto>(`/devices/${deviceId}`, {
    name: data.name,
    serial_number: data.serialNumber,
    registry_number: data.registryNumber,
    modification: data.modification,
    manufacture_year: data.manufactureYear,
    inventory_number: data.inventoryNumber,
    comment: data.comment,
  });

  return mapDevice(response.data);
}

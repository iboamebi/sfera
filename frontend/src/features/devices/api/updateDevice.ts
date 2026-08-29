import { http } from "../../../shared/api/http";
import { mapDevice } from "./deviceMapper";
import type { DeviceRead } from "../model/types";
import type { DeviceApiDto } from "./types";

type UpdateDeviceInput = {
  deviceId: string;
  serialNumber?: string;
  modification?: string | null;
};

export async function updateDevice(
  input: UpdateDeviceInput,
): Promise<DeviceRead> {
  const response = await http.put<DeviceApiDto>(`/devices/${input.deviceId}`, {
    ...(input.serialNumber !== undefined && {
      serial_number: input.serialNumber,
    }),
    ...(input.modification !== undefined && {
      modification: input.modification,
    }),
  });

  return mapDevice(response.data);
}

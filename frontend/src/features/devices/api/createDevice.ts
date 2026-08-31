import { http } from "../../../shared/api/http";
import { mapDevice } from "./deviceMapper";
import type { DeviceRead } from "../model/types";
import type { DeviceApiDto } from "./types";

type CreateDeviceInput = {
  instrumentTypeId: string;
  name: string;
  serialNumber: string;
};

export async function createDevice(
  input: CreateDeviceInput,
): Promise<DeviceRead> {
  const response = await http.post<DeviceApiDto>("/devices/", {
    instrument_type_id: input.instrumentTypeId,
    name: input.name,
    serial_number: input.serialNumber,
  });

  return mapDevice(response.data);
}

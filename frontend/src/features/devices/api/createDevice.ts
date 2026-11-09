import { http } from "../../../shared/api/http";
import { mapDevice } from "./deviceMapper";
import type { DeviceRead } from "../model/types";
import type { DeviceApiDto } from "./types";

export type CreateDeviceInput = {
  instrumentTypeId: string;
  customerId: string;
  siteId?: string | null;
  name: string;
  serialNumber: string;
};

export async function createDevice(
  input: CreateDeviceInput,
): Promise<DeviceRead> {
  const response = await http.post<DeviceApiDto>("/devices/", {
    instrument_type_id: input.instrumentTypeId,
    customer_id: input.customerId,
    site_id: input.siteId ?? null,
    name: input.name,
    serial_number: input.serialNumber,
  });

  return mapDevice(response.data);
}

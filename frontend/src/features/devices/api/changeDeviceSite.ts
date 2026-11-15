import { http } from "../../../shared/api/http";
import { mapDevice } from "./deviceMapper";
import type { DeviceRead } from "../model/types";
import type { DeviceApiDto } from "./types";

export interface ChangeDeviceSiteInput {
  siteId: string | null;
  reason: string;
}

export async function changeDeviceSite(
  deviceId: string,
  data: ChangeDeviceSiteInput,
): Promise<DeviceRead> {
  const response = await http.patch<DeviceApiDto>(
    `/devices/${deviceId}/site`,
    {
      site_id: data.siteId,
      reason: data.reason,
    },
  );

  return mapDevice(response.data);
}

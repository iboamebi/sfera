import { http } from "../../../shared/api/http";
import { mapDevice } from "./deviceMapper";
import type { DeviceRead } from "../model/types";
import type { DeviceApiDto } from "./types";

export async function getDevices(): Promise<DeviceRead[]> {
  const response = await http.get<DeviceApiDto[]>("/devices/");

  return response.data.map(mapDevice);
}

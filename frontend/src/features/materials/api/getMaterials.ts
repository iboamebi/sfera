import { http } from "../../../shared/api/http";
import type { MaterialRead } from "../model/types";
import { mapMaterial } from "./materialMapper";
import type { MaterialApiDto } from "./types";

export async function getMaterials(): Promise<MaterialRead[]> {
  const response = await http.get<MaterialApiDto[]>("/materials/");

  return response.data.map(mapMaterial);
}

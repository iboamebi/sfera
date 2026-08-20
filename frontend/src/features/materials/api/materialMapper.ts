import type { MaterialRead } from "../model/types";
import type { MaterialApiDto } from "./types";

export function mapMaterial(dto: MaterialApiDto): MaterialRead {
  return {
    id: dto.id,
    name: dto.name,
    article: dto.article,
    unit: dto.unit,
    description: dto.description,
    archived: dto.archived,
  };
}

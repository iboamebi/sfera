import type { UUID } from "crypto";

export interface CurrentUser {
  id: UUID;
  username: string;
}

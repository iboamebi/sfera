import { z } from "zod";

export const createSiteSchema = z.object({
  name: z.string().trim().min(1, "Укажите название"),
  address: z.string().trim().min(1, "Укажите адрес"),
});

export type CreateSiteSchema = z.infer<typeof createSiteSchema>;

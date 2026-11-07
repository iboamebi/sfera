import { z } from "zod";

export const createDeviceSchema = z.object({
  instrumentTypeId: z.string().uuid("Выберите тип СИ"),
  siteId: z.string().uuid().nullable(),
  name: z.string().trim().min(1, "Укажите наименование"),
  serialNumber: z.string().trim().min(1, "Укажите заводской номер"),
});

export type CreateDeviceSchema = z.infer<typeof createDeviceSchema>;

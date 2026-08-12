import { z } from "zod";

export const createOrderSchema = z.object({
  number: z.string().trim().min(1),
  customerId: z.string().uuid(),
});

export type CreateOrderSchema = z.infer<typeof createOrderSchema>;

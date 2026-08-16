import { z } from "zod";

export const createOrderSchema = z.object({
  number: z.string().trim().min(1),
  customerId: z.string().uuid(),
  plannedIssueAt: z
    .string()
    .regex(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/)
    .optional(),
  comment: z.string().trim().optional(),
});

export type CreateOrderSchema = z.infer<typeof createOrderSchema>;

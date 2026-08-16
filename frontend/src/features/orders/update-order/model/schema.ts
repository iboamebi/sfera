import { z } from "zod";

export const updateOrderSchema = z.object({
  plannedIssueAt: z
    .string()
    .regex(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/)
    .optional(),
  comment: z.string().trim().optional(),
});

export type UpdateOrderSchema = z.infer<typeof updateOrderSchema>;

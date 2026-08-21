import { z } from "zod";

export const createCustomerSchema = z.object({
  organizationId: z.string().uuid(),
  name: z.string().trim().min(1),
  contactPerson: z.string().trim().optional(),
  phone: z.string().trim().optional(),
  email: z.string().trim().email().optional().or(z.literal("")),
  comment: z.string().trim().optional(),
  discountPercent: z.number().min(0).max(100),
});

export type CreateCustomerSchema = z.infer<typeof createCustomerSchema>;

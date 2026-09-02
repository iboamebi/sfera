import { z } from "zod";

export const createOrganizationSchema = z.object({
  name: z.string().trim().min(1),
  shortName: z.string().trim().optional(),
  inn: z.string().trim().optional(),
  kpp: z.string().trim().optional(),
  ogrn: z.string().trim().optional(),
  address: z.string().trim().optional(),
  phone: z.string().trim().optional(),
  email: z.string().trim().email().optional().or(z.literal("")),
  website: z.string().trim().url().optional().or(z.literal("")),
  comment: z.string().trim().optional(),
});

export type CreateOrganizationSchema = z.infer<
  typeof createOrganizationSchema
>;

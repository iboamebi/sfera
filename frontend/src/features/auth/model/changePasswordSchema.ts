import { z } from "zod";

export const changePasswordSchema = z
  .object({
    currentPassword: z.string().min(1, "Введите текущий пароль"),
    newPassword: z.string().min(1, "Введите новый пароль"),
    confirmPassword: z.string().min(1, "Повторите новый пароль"),
  })
  .refine((values) => values.newPassword === values.confirmPassword, {
    message: "Пароли не совпадают",
    path: ["confirmPassword"],
  });

export type ChangePasswordFormValues = z.infer<typeof changePasswordSchema>;

import { zodResolver } from "@hookform/resolvers/zod";
import { Button, Stack, TextField } from "@mui/material";
import { useForm } from "react-hook-form";

import {
  createSiteSchema,
  type CreateSiteSchema,
} from "../model/schema";

interface SiteFormProps {
  onSubmit: (data: CreateSiteSchema) => void;
  isPending?: boolean;
}

export function SiteForm({
  onSubmit,
  isPending = false,
}: SiteFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CreateSiteSchema>({
    resolver: zodResolver(createSiteSchema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Stack spacing={2}>
        <TextField
          label="Название объекта"
          {...register("name")}
          error={Boolean(errors.name)}
          helperText={errors.name?.message}
          disabled={isPending}
        />

        <TextField
          label="Адрес"
          {...register("address")}
          error={Boolean(errors.address)}
          helperText={errors.address?.message}
          disabled={isPending}
        />

        <Button type="submit" variant="contained" disabled={isPending}>
          {isPending ? "Создание..." : "Создать объект"}
        </Button>
      </Stack>
    </form>
  );
}

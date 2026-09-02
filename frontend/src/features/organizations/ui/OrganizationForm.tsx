import { zodResolver } from "@hookform/resolvers/zod";
import { Button, Stack, TextField } from "@mui/material";
import { useForm } from "react-hook-form";

import {
  createOrganizationSchema,
  type CreateOrganizationSchema,
} from "../model/schema";

interface OrganizationFormProps {
  onSubmit: (data: CreateOrganizationSchema) => void;
  isPending?: boolean;
}

export function OrganizationForm({
  onSubmit,
  isPending = false,
}: OrganizationFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CreateOrganizationSchema>({
    resolver: zodResolver(createOrganizationSchema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Stack spacing={2}>
        <TextField
          label="Название"
          {...register("name")}
          error={Boolean(errors.name)}
          helperText={errors.name?.message}
          disabled={isPending}
        />

        <TextField
          label="Краткое название"
          {...register("shortName")}
          error={Boolean(errors.shortName)}
          helperText={errors.shortName?.message}
          disabled={isPending}
        />

        <TextField
          label="ИНН"
          {...register("inn")}
          error={Boolean(errors.inn)}
          helperText={errors.inn?.message}
          disabled={isPending}
        />

        <TextField
          label="КПП"
          {...register("kpp")}
          error={Boolean(errors.kpp)}
          helperText={errors.kpp?.message}
          disabled={isPending}
        />

        <TextField
          label="ОГРН"
          {...register("ogrn")}
          error={Boolean(errors.ogrn)}
          helperText={errors.ogrn?.message}
          disabled={isPending}
        />

        <TextField
          label="Адрес"
          {...register("address")}
          error={Boolean(errors.address)}
          helperText={errors.address?.message}
          disabled={isPending}
        />

        <TextField
          label="Телефон"
          {...register("phone")}
          error={Boolean(errors.phone)}
          helperText={errors.phone?.message}
          disabled={isPending}
        />

        <TextField
          label="Email"
          type="email"
          {...register("email")}
          error={Boolean(errors.email)}
          helperText={errors.email?.message}
          disabled={isPending}
        />

        <TextField
          label="Сайт"
          {...register("website")}
          error={Boolean(errors.website)}
          helperText={errors.website?.message}
          disabled={isPending}
        />

        <TextField
          label="Комментарий"
          multiline
          minRows={3}
          {...register("comment")}
          error={Boolean(errors.comment)}
          helperText={errors.comment?.message}
          disabled={isPending}
        />

        <Button type="submit" variant="contained" disabled={isPending}>
          {isPending ? "Создание..." : "Создать организацию"}
        </Button>
      </Stack>
    </form>
  );
}

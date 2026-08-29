import { zodResolver } from "@hookform/resolvers/zod";
import { Button, MenuItem, Stack, TextField } from "@mui/material";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { useQueryClient } from "@tanstack/react-query";

import { useCreateOrganization } from "../../organizations/model/useCreateOrganization";
import type { CreateOrganizationForm } from "../../organizations/model/schema";
import { useOrganizations } from "../../organizations/model/useOrganizations";
import { OrganizationForm } from "../../organizations/ui/OrganizationForm";
import {
  createCustomerSchema,
  type CreateCustomerSchema,
} from "../model/schema";

interface CustomerFormProps {
  onSubmit: (data: CreateCustomerSchema) => void;
  isPending?: boolean;
}

export function CustomerForm({
  onSubmit,
  isPending = false,
}: CustomerFormProps) {
  const [isCreateOrganizationOpen, setIsCreateOrganizationOpen] = useState(false);
  const queryClient = useQueryClient();
  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<CreateCustomerSchema>({
    resolver: zodResolver(createCustomerSchema),
    defaultValues: {
      discountPercent: 0,
    },
  });

  const {
    data: organizations = [],
    isLoading: isOrganizationsLoading,
    isError: isOrganizationsError,
  } = useOrganizations();

  const createOrganizationMutation = useCreateOrganization({
    onSuccess: async (organization) => {
      await queryClient.invalidateQueries({ queryKey: ["organizations"] });
      setValue("organizationId", organization.id, { shouldValidate: true });
      setIsCreateOrganizationOpen(false);
    },
  });

  const handleCreateOrganization = (data: CreateOrganizationForm) => {
    createOrganizationMutation.mutate(data);
  };

  if (isCreateOrganizationOpen) {
    return (
      <Stack spacing={2}>
        <OrganizationForm
          onSubmit={handleCreateOrganization}
          isPending={createOrganizationMutation.isPending}
        />
        <Button
          onClick={() => setIsCreateOrganizationOpen(false)}
          disabled={createOrganizationMutation.isPending}
        >
          Вернуться к клиенту
        </Button>
      </Stack>
    );
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Stack spacing={2}>
        <TextField
          select
          label="Организация"
          {...register("organizationId")}
          error={Boolean(errors.organizationId)}
          helperText={
            errors.organizationId?.message ??
            (isOrganizationsError
              ? "Не удалось загрузить организации"
              : organizations.length === 0 && !isOrganizationsLoading
                ? "Создайте организацию, чтобы зарегистрировать клиента"
                : undefined)
          }
          disabled={isPending || isOrganizationsLoading || isOrganizationsError}
        >
          {organizations.map((organization) => (
            <MenuItem key={organization.id} value={organization.id}>
              {organization.name}
            </MenuItem>
          ))}
        </TextField>

        <Button
          onClick={() => setIsCreateOrganizationOpen(true)}
          variant="outlined"
          disabled={isPending}
        >
          Создать организацию
        </Button>

        <TextField
          label="Название"
          {...register("name")}
          error={Boolean(errors.name)}
          helperText={errors.name?.message}
          disabled={isPending}
        />

        <TextField
          label="Контактное лицо"
          {...register("contactPerson")}
          error={Boolean(errors.contactPerson)}
          helperText={errors.contactPerson?.message}
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
          label="Комментарий"
          multiline
          minRows={3}
          {...register("comment")}
          error={Boolean(errors.comment)}
          helperText={errors.comment?.message}
          disabled={isPending}
        />

        <TextField
          label="Скидка, %"
          type="number"
          slotProps={{ input: { inputProps: { min: 0, max: 100, step: 0.01 } } }}
          {...register("discountPercent", { valueAsNumber: true })}
          error={Boolean(errors.discountPercent)}
          helperText={errors.discountPercent?.message}
          disabled={isPending}
        />

        <Button
          type="submit"
          variant="contained"
          disabled={
            isPending ||
            isOrganizationsLoading ||
            isOrganizationsError ||
            organizations.length === 0
          }
        >
          {isPending ? "Создание..." : "Создать клиента"}
        </Button>
      </Stack>
    </form>
  );
}

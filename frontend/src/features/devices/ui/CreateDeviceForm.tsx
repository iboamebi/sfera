import { zodResolver } from "@hookform/resolvers/zod";
import { Button, MenuItem, Stack, TextField } from "@mui/material";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { useInstrumentTypes } from "../../instrument-type/model/useInstrumentTypes";

const createDeviceSchema = z.object({
  instrumentTypeId: z.string().uuid("Выберите тип средства измерений"),
  serialNumber: z.string().trim().min(1, "Укажите серийный номер"),
});

type CreateDeviceFormValues = z.infer<typeof createDeviceSchema>;

interface CreateDeviceFormProps {
  onSubmit: (data: CreateDeviceFormValues) => void;
  isPending?: boolean;
}

export function CreateDeviceForm({
  onSubmit,
  isPending = false,
}: CreateDeviceFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CreateDeviceFormValues>({
    resolver: zodResolver(createDeviceSchema),
  });

  const {
    data: instrumentTypes = [],
    isLoading: isInstrumentTypesLoading,
    isError: isInstrumentTypesError,
  } = useInstrumentTypes();

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Stack spacing={2}>
        <TextField
          select
          label="Тип средства измерений"
          {...register("instrumentTypeId")}
          error={Boolean(errors.instrumentTypeId)}
          helperText={
            errors.instrumentTypeId?.message ??
            (isInstrumentTypesError
              ? "Не удалось загрузить типы средств измерений"
              : undefined)
          }
          disabled={
            isPending || isInstrumentTypesLoading || isInstrumentTypesError
          }
        >
          {instrumentTypes
            .filter((instrumentType) => !instrumentType.archived)
            .map((instrumentType) => (
              <MenuItem key={instrumentType.id} value={instrumentType.id}>
                {instrumentType.name}
              </MenuItem>
            ))}
        </TextField>

        <TextField
          label="Серийный номер"
          {...register("serialNumber")}
          error={Boolean(errors.serialNumber)}
          helperText={errors.serialNumber?.message}
          disabled={isPending}
        />

        <Button
          type="submit"
          variant="contained"
          disabled={
            isPending || isInstrumentTypesLoading || isInstrumentTypesError
          }
        >
          {isPending ? "Создание..." : "Создать СИ"}
        </Button>
      </Stack>
    </form>
  );
}

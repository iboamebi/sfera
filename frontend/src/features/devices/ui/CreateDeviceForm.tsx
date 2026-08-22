import { useEffect } from "react";

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
  instrumentTypeId?: string;
  onSubmit: (data: CreateDeviceFormValues) => void;
  onCreateInstrumentType?: () => void;
  isPending?: boolean;
}

export function CreateDeviceForm({
  instrumentTypeId,
  onSubmit,
  onCreateInstrumentType,
  isPending = false,
}: CreateDeviceFormProps) {
  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<CreateDeviceFormValues>({
    resolver: zodResolver(createDeviceSchema),
    defaultValues: {
      instrumentTypeId: instrumentTypeId ?? "",
    },
  });

  useEffect(() => {
    if (instrumentTypeId) {
      setValue("instrumentTypeId", instrumentTypeId, {
        shouldValidate: true,
      });
    }
  }, [instrumentTypeId, setValue]);

  const {
    data: instrumentTypes = [],
    isLoading: isInstrumentTypesLoading,
    isError: isInstrumentTypesError,
  } = useInstrumentTypes();

  const activeInstrumentTypes = instrumentTypes.filter(
    (instrumentType) => !instrumentType.archived,
  );

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
          {activeInstrumentTypes.map((instrumentType) => (
            <MenuItem key={instrumentType.id} value={instrumentType.id}>
              {instrumentType.name}
            </MenuItem>
          ))}
        </TextField>

        {onCreateInstrumentType && (
          <Button
            type="button"
            variant="outlined"
            onClick={onCreateInstrumentType}
            disabled={isPending}
          >
            Создать тип СИ
          </Button>
        )}

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

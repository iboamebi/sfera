import { zodResolver } from "@hookform/resolvers/zod";
import {
  Button,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Stack,
  TextField,
} from "@mui/material";
import { useForm } from "react-hook-form";

import { useInstrumentTypes } from "../../instrument-type/model/useInstrumentTypes";
import { useCustomerSites } from "../../sites/model/useCustomerSites";
import {
  createDeviceSchema,
  type CreateDeviceSchema,
} from "../model/schema";

interface DeviceFormProps {
  customerId: string;
  onSubmit: (data: CreateDeviceSchema) => void;
  isPending?: boolean;
}

export function DeviceForm({
  customerId,
  onSubmit,
  isPending = false,
}: DeviceFormProps) {
  const { data: instrumentTypes } = useInstrumentTypes();
  const { data: sites } = useCustomerSites(customerId);
  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors },
  } = useForm<CreateDeviceSchema>({
    resolver: zodResolver(createDeviceSchema),
    defaultValues: {
      siteId: null,
    },
  });

  const siteId = watch("siteId");

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Stack spacing={2}>
        <FormControl error={Boolean(errors.instrumentTypeId)} disabled={isPending}>
          <InputLabel id="instrument-type-label">Тип СИ</InputLabel>
          <Select
            labelId="instrument-type-label"
            label="Тип СИ"
            value={watch("instrumentTypeId") ?? ""}
            onChange={(event) =>
              setValue("instrumentTypeId", event.target.value, {
                shouldValidate: true,
              })
            }
          >
            {instrumentTypes?.filter((item) => !item.archived).map((item) => (
              <MenuItem key={item.id} value={item.id}>
                {item.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <FormControl disabled={isPending}>
          <InputLabel id="site-label">Объект</InputLabel>
          <Select
            labelId="site-label"
            label="Объект"
            value={siteId ?? ""}
            onChange={(event) =>
              setValue("siteId", event.target.value || null)
            }
          >
            <MenuItem value="">Без объекта</MenuItem>
            {sites?.filter((site) => !site.archived).map((site) => (
              <MenuItem key={site.id} value={site.id}>
                {site.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <TextField
          label="Наименование СИ"
          {...register("name")}
          error={Boolean(errors.name)}
          helperText={errors.name?.message}
          disabled={isPending}
        />

        <TextField
          label="Заводской номер"
          {...register("serialNumber")}
          error={Boolean(errors.serialNumber)}
          helperText={errors.serialNumber?.message}
          disabled={isPending}
        />

        <Button type="submit" variant="contained" disabled={isPending}>
          {isPending ? "Создание..." : "Создать СИ"}
        </Button>
      </Stack>
    </form>
  );
}

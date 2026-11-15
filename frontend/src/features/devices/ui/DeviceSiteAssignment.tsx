import { useEffect, useState } from "react";
import {
  Alert,
  Button,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

import { useCustomerSites } from "../../sites/model/useCustomerSites";
import { useChangeDeviceSite } from "../model/useChangeDeviceSite";
import type { DeviceRead } from "../model/types";

interface DeviceSiteAssignmentProps {
  device: DeviceRead;
}

export function DeviceSiteAssignment({ device }: DeviceSiteAssignmentProps) {
  const { data: sites, isLoading, error } = useCustomerSites(device.customerId);
  const [siteId, setSiteId] = useState(device.siteId ?? "");
  const [reason, setReason] = useState("");
  const mutation = useChangeDeviceSite(device.id);

  useEffect(() => {
    setSiteId(device.siteId ?? "");
    setReason("");
  }, [device.id, device.siteId]);

  const currentSite = sites?.find((site) => site.id === device.siteId);
  const availableSites = sites?.filter(
    (site) => !site.archived || site.id === device.siteId,
  ) ?? [];
  const hasChanges = (siteId || null) !== device.siteId;

  const save = () => {
    mutation.mutate(
      { siteId: siteId || null, reason: reason.trim() },
      { onSuccess: () => setReason("") },
    );
  };

  return (
    <Stack spacing={1.5}>
      <Typography variant="h6">Объект размещения</Typography>
      <Typography color="text.secondary">
        Текущий объект: {isLoading ? "Загрузка..." : currentSite?.name ?? "Не назначен"}
        {currentSite?.archived ? " (в архиве)" : ""}
      </Typography>

      {error && (
        <Alert severity="error">Не удалось загрузить список объектов клиента.</Alert>
      )}

      <FormControl fullWidth disabled={isLoading || Boolean(error) || mutation.isPending}>
        <InputLabel id="device-site-label">Объект</InputLabel>
        <Select
          labelId="device-site-label"
          label="Объект"
          value={siteId}
          onChange={(event) => {
            setSiteId(event.target.value);
            mutation.reset();
          }}
        >
          <MenuItem value="">Без объекта</MenuItem>
          {availableSites.map((site) => (
            <MenuItem key={site.id} value={site.id}>
              {site.name}{site.archived ? " (в архиве)" : ""}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      <TextField
        label="Причина изменения"
        value={reason}
        onChange={(event) => {
          setReason(event.target.value);
          mutation.reset();
        }}
        multiline
        minRows={2}
        slotProps={{ htmlInput: { maxLength: 1000 } }}
        helperText="Причина обязательна и сохраняется в журнале аудита."
        disabled={mutation.isPending}
        fullWidth
      />

      {mutation.isError && (
        <Alert severity="error">
          Не удалось изменить объект. Проверьте данные и повторите попытку.
        </Alert>
      )}

      {mutation.isSuccess && (
        <Alert severity="success">Привязка к объекту обновлена.</Alert>
      )}

      <Button
        variant="contained"
        onClick={save}
        disabled={
          !hasChanges ||
          !reason.trim() ||
          reason.trim().length > 1000 ||
          isLoading ||
          Boolean(error) ||
          mutation.isPending
        }
        sx={{ alignSelf: "flex-start" }}
      >
        {mutation.isPending ? "Сохранение..." : "Сохранить привязку"}
      </Button>
    </Stack>
  );
}

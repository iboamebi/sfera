import {
  Autocomplete,
  Button,
  Checkbox,
  FormControl,
  FormControlLabel,
  InputLabel,
  ListItemText,
  MenuItem,
  Select,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { useEffect, useState } from "react";

import type { DeviceRead } from "../../../devices/model/types";
import { useDevices } from "../../../devices/model/useDevices";
import { useCustomerSites } from "../../../sites/model/useCustomerSites";

interface DeviceSelectorProps {
  value: string;
  customerId: string;
  onChange: (deviceId: string) => void;
  onCreateDevice?: () => void;
  instrumentTypeId?: string | null;
}

export function DeviceSelector({
  value,
  customerId,
  onChange,
  onCreateDevice,
  instrumentTypeId,
}: DeviceSelectorProps) {
  const { data: devices = [], isLoading, error } = useDevices();
  const {
    data: sites = [],
    isLoading: isSitesLoading,
    isError: isSitesError,
  } = useCustomerSites(customerId);
  const [selectedSiteIds, setSelectedSiteIds] = useState<string[]>([]);
  const [includeWithoutSite, setIncludeWithoutSite] = useState(true);

  const customerDevices = devices.filter(
    (device) => device.customerId === customerId,
  );
  const siteFilteredDevices = customerDevices.filter((device) => {
    if (device.siteId === null) {
      return includeWithoutSite;
    }

    return (
      selectedSiteIds.length === 0 || selectedSiteIds.includes(device.siteId)
    );
  });
  const availableDevices = instrumentTypeId
    ? siteFilteredDevices.filter(
        (device) => device.instrumentTypeId === instrumentTypeId,
      )
    : siteFilteredDevices;
  const selectedDevice =
    availableDevices.find((device) => device.id === value) ?? null;

  useEffect(() => {
    setSelectedSiteIds([]);
    setIncludeWithoutSite(true);
  }, [customerId]);

  useEffect(() => {
    if (
      !isLoading &&
      value &&
      !availableDevices.some((device) => device.id === value)
    ) {
      onChange("");
    }
  }, [availableDevices, isLoading, onChange, value]);

  if (error) {
    return (
      <Typography color="error">
        Не удалось загрузить средства измерений.
      </Typography>
    );
  }

  return (
    <Stack spacing={1} sx={{ width: "100%" }}>
      <FormControl fullWidth size="small" disabled={isSitesLoading}>
        <InputLabel id="device-site-filter-label">Площадки</InputLabel>
        <Select
          labelId="device-site-filter-label"
          multiple
          value={selectedSiteIds}
          label="Площадки"
          onChange={(event) => {
            const nextValue = event.target.value;
            setSelectedSiteIds(
              typeof nextValue === "string" ? nextValue.split(",") : nextValue,
            );
          }}
          renderValue={(selected) =>
            selected.length === 0
              ? "Все площадки"
              : sites
                  .filter((site) => selected.includes(site.id))
                  .map((site) => site.name)
                  .join(", ")
          }
        >
          {sites.map((site) => (
            <MenuItem key={site.id} value={site.id}>
              <Checkbox checked={selectedSiteIds.includes(site.id)} />
              <ListItemText
                primary={site.name}
                secondary={site.address}
              />
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      {isSitesError && (
        <Typography color="error" variant="caption">
          Не удалось загрузить площадки. Фильтр по площадкам недоступен.
        </Typography>
      )}

      <FormControlLabel
        control={
          <Checkbox
            checked={includeWithoutSite}
            onChange={(event) => setIncludeWithoutSite(event.target.checked)}
          />
        }
        label="Включать СИ без площадки"
      />

      <Autocomplete
        fullWidth
        options={availableDevices}
        value={selectedDevice}
        loading={isLoading}
        getOptionLabel={(device) => device.serialNumber}
        isOptionEqualToValue={(option, selected) => option.id === selected.id}
        onChange={(_, device: DeviceRead | null) =>
          onChange(device?.id ?? "")
        }
        renderInput={(params) => (
          <TextField
            {...params}
            fullWidth
            label="Средство измерений"
            placeholder="Введите серийный номер"
          />
        )}
      />

      {onCreateDevice && (
        <Button
          onClick={onCreateDevice}
          variant="outlined"
          disabled={isLoading}
        >
          Создать СИ
        </Button>
      )}
    </Stack>
  );
}

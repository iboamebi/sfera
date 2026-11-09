import {
  Alert,
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
  onCreateDevice?: (serialNumber: string) => void;
  instrumentTypeId?: string | null;
  requireUnmatchedSerial?: boolean;
}

export function DeviceSelector({
  value,
  customerId,
  onChange,
  onCreateDevice,
  instrumentTypeId,
  requireUnmatchedSerial = false,
}: DeviceSelectorProps) {
  const { data: devices = [], isLoading, error } = useDevices();
  const {
    data: sites = [],
    isLoading: isSitesLoading,
    isError: isSitesError,
  } = useCustomerSites(customerId);
  const [selectedSiteIds, setSelectedSiteIds] = useState<string[]>([]);
  const [includeWithoutSite, setIncludeWithoutSite] = useState(true);
  const [inputValue, setInputValue] = useState("");

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
  const normalizedInput = inputValue.trim().toLocaleLowerCase();
  const matchingDevice = normalizedInput
    ? customerDevices.find(
        (device) => device.serialNumber.trim().toLocaleLowerCase() === normalizedInput,
      ) ?? null
    : null;
  const matchingDeviceSite = matchingDevice?.siteId
    ? sites.find((site) => site.id === matchingDevice.siteId)?.name ?? "Площадка не найдена"
    : "Без площадки";
  const matchingDeviceTypeMatches =
    !instrumentTypeId || matchingDevice?.instrumentTypeId === instrumentTypeId;
  const matchingDeviceIsVisible = matchingDevice
    ? availableDevices.some((device) => device.id === matchingDevice.id)
    : false;

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
        <InputLabel id="device-site-filter-label" shrink>
          Площадки
        </InputLabel>
        <Select<string[]>
          labelId="device-site-filter-label"
          displayEmpty
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
        inputValue={inputValue}
        loading={isLoading}
        getOptionLabel={(device) => device.serialNumber}
        isOptionEqualToValue={(option, selected) => option.id === selected.id}
        onInputChange={(_, nextValue, reason) => {
          if (reason !== "reset") {
            setInputValue(nextValue);
          }
        }}
        onChange={(_, device: DeviceRead | null) => {
          onChange(device?.id ?? "");
          if (device) setInputValue(device.serialNumber);
        }}
        renderOption={(props, device) => (
          <li {...props} key={device.id}>
            <Stack spacing={0.25}>
              <Typography variant="body2">
                {device.name ?? "СИ"} — № {device.serialNumber}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {device.siteId
                  ? sites.find((site) => site.id === device.siteId)?.name ?? "Площадка не найдена"
                  : "Без площадки"}
              </Typography>
            </Stack>
          </li>
        )}
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
          onClick={() => onCreateDevice(inputValue.trim())}
          variant="outlined"
          disabled={
            isLoading ||
            (requireUnmatchedSerial && (!normalizedInput || Boolean(matchingDevice)))
          }
        >
          Создать СИ
        </Button>
      )}
      {matchingDevice && (
        <Alert
          severity={matchingDeviceTypeMatches ? "info" : "warning"}
          action={
            matchingDeviceTypeMatches && !matchingDeviceIsVisible ? (
              <Button
                color="inherit"
                size="small"
                onClick={() => {
                  setSelectedSiteIds([]);
                  setIncludeWithoutSite(true);
                }}
              >
                Показать СИ
              </Button>
            ) : undefined
          }
        >
          СИ с таким заводским номером уже существует: {matchingDevice.name ?? "без наименования"}, № {matchingDevice.serialNumber}. Текущая площадка: {matchingDeviceSite}.
          {matchingDeviceTypeMatches
            ? " Выберите существующее СИ в списке. Создание дубликата недоступно."
            : " Тип найденного СИ не совпадает с типом позиции заказа. Проверьте выбранный тип СИ."}
        </Alert>
      )}
    </Stack>
  );
}

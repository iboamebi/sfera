import {
  Alert,
  Autocomplete,
  Button,
  Checkbox,
  FormControl,
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
  excludedInstrumentIds?: string[];
}

export function DeviceSelector({
  value,
  customerId,
  onChange,
  onCreateDevice,
  instrumentTypeId,
  requireUnmatchedSerial = false,
  excludedInstrumentIds = [],
}: DeviceSelectorProps) {
  const { data: devices = [], isLoading, error } = useDevices();
  const {
    data: sites = [],
    isLoading: isSitesLoading,
    isError: isSitesError,
  } = useCustomerSites(customerId);
  const [selectedSiteIds, setSelectedSiteIds] = useState<string[]>([]);
  const [includeOtherSites, setIncludeOtherSites] = useState(false);
  const [inputValue, setInputValue] = useState("");

  const customerDevices = devices.filter(
    (device) => device.customerId === customerId,
  );
  const excludedIds = new Set(excludedInstrumentIds);
  const serialCounts = customerDevices.reduce((counts, device) => {
    const serial = device.serialNumber.trim().toLocaleLowerCase();
    counts.set(serial, (counts.get(serial) ?? 0) + 1);
    return counts;
  }, new Map<string, number>());
  const excludedSerials = new Set(
    customerDevices
      .filter((device) => excludedIds.has(device.id))
      .map((device) => device.serialNumber.trim().toLocaleLowerCase()),
  );
  const siteFilteredDevices = customerDevices.filter((device) => {
    const serial = device.serialNumber.trim().toLocaleLowerCase();
    if (
      excludedIds.has(device.id) ||
      excludedSerials.has(serial) ||
      (serialCounts.get(serial) ?? 0) > 1
    ) {
      return false;
    }

    return (
      includeOtherSites ||
      selectedSiteIds.length === 0 ||
      (device.siteId !== null && selectedSiteIds.includes(device.siteId))
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
  const hasVisibleSearchMatch = availableDevices.some((device) =>
    device.serialNumber.trim().toLocaleLowerCase().includes(normalizedInput),
  );
  const canExpandSiteSearch =
    selectedSiteIds.length > 0 && !includeOtherSites && !hasVisibleSearchMatch;
  const matchingDevices = normalizedInput
    ? customerDevices.filter(
        (device) => device.serialNumber.trim().toLocaleLowerCase() === normalizedInput,
      )
    : [];
  const matchingDevice = matchingDevices[0] ?? null;
  const matchingDeviceAlreadyInOrder = matchingDevices.some((device) =>
    excludedIds.has(device.id),
  );
  const matchingSerialIsAmbiguous = matchingDevices.length > 1;
  const matchingDeviceSite = matchingDevice?.siteId
    ? sites.find((site) => site.id === matchingDevice.siteId)?.name ?? "Площадка не найдена"
    : "Без площадки";
  const matchingDeviceTypeMatches =
    !instrumentTypeId || matchingDevice?.instrumentTypeId === instrumentTypeId;
  const matchingDeviceIsVisible = matchingDevice
    ? availableDevices.some((device) => device.id === matchingDevice.id)
    : false;
  const createDeviceDisabled =
    isLoading ||
    (requireUnmatchedSerial &&
      (!normalizedInput || Boolean(matchingDevice) || canExpandSiteSearch));
  const createDeviceDisabledReason = isLoading
    ? "Загружается список СИ. Создание станет доступно после завершения загрузки."
    : !normalizedInput
      ? "Введите заводской номер, чтобы создать новую карточку СИ."
      : canExpandSiteSearch
        ? "Сначала выполните поиск по всем площадкам — это исключит создание дубликата."
        : matchingDevice
          ? "Карточка с таким заводским номером уже существует. Выберите её в списке или проверьте найденную карточку."
          : "";

  useEffect(() => {
    setSelectedSiteIds([]);
    setIncludeOtherSites(false);
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
            setIncludeOtherSites(false);
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

      <Autocomplete
        fullWidth
        options={availableDevices}
        value={selectedDevice}
        inputValue={inputValue}
        loading={isLoading}
        loadingText="Загрузка средств измерений…"
        clearOnBlur={false}
        noOptionsText={
          normalizedInput
            ? "СИ не найдено"
            : "Начните вводить заводской номер."
        }
        getOptionLabel={(device) => device.serialNumber}
        isOptionEqualToValue={(option, selected) => option.id === selected.id}
        onInputChange={(_, nextValue, reason) => {
          if (reason === "input" || reason === "clear") {
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

      {canExpandSiteSearch && (
        <Alert
          severity="info"
          action={
            <Button
              color="inherit"
              size="small"
              onClick={() => setIncludeOtherSites(true)}
            >
              Искать везде
            </Button>
          }
        >
          На выбранной площадке СИ не найдено. Можно проверить карточки на других площадках и без площадки.
        </Alert>
      )}

      {onCreateDevice && (
        <Button
          onClick={() => onCreateDevice(inputValue.trim())}
          variant="outlined"
          disabled={createDeviceDisabled}
        >
          Создать карточку СИ
        </Button>
      )}
      {onCreateDevice && createDeviceDisabled && !matchingDevice && (
        <Typography variant="caption" color="text.secondary">
          {createDeviceDisabledReason}
        </Typography>
      )}
      {matchingDevice && (
        <Alert
          severity={matchingDeviceTypeMatches ? "info" : "warning"}
          action={
            matchingDeviceTypeMatches &&
            !matchingDeviceIsVisible &&
            !matchingDeviceAlreadyInOrder &&
            !matchingSerialIsAmbiguous ? (
              <Button
                color="inherit"
                size="small"
                onClick={() => {
                  setSelectedSiteIds([]);
                }}
              >
                Показать СИ
              </Button>
            ) : undefined
          }
        >
          {matchingSerialIsAmbiguous
            ? `В базе найдено несколько карточек СИ с заводским номером ${matchingDevice.serialNumber}. Выбор заблокирован: сначала необходимо устранить дубликаты карточек.`
            : matchingDeviceAlreadyInOrder
              ? `СИ с заводским номером ${matchingDevice.serialNumber} уже добавлено в этот заказ.`
              : `СИ с таким заводским номером уже существует: ${matchingDevice.name ?? "без наименования"}, № ${matchingDevice.serialNumber}. Текущая площадка: ${matchingDeviceSite}.`}
          {!matchingSerialIsAmbiguous && !matchingDeviceAlreadyInOrder &&
            (matchingDeviceTypeMatches
              ? " Выберите существующее СИ в списке. Создание дубликата недоступно."
              : " Тип найденного СИ не совпадает с типом позиции заказа. Проверьте выбранный тип СИ.")}
        </Alert>
      )}
    </Stack>
  );
}

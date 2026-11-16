import { useState } from "react";

import { isAxiosError } from "axios";
import {
  Button,
  Checkbox,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControlLabel,
  MenuItem,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

import { useCreateDevice } from "../../../devices/model/useCreateDevice";
import { CreateDeviceForm } from "../../../devices/ui/CreateDeviceForm";
import { useCreateInstrumentType } from "../../../instrument-type/model/useCreateInstrumentType";
import { useInstrumentTypes } from "../../../instrument-type/model/useInstrumentTypes";
import { CreateInstrumentTypeForm } from "../../../instrument-type/ui/CreateInstrumentTypeForm";
import type { OrderItemOperation } from "../../model/types";
import { useAddOrderItem } from "../model/useAddOrderItem";
import { DeviceSelector } from "./DeviceSelector";

const OPERATION_OPTIONS: Array<{
  value: OrderItemOperation;
  label: string;
}> = [
  { value: "verification", label: "Поверка" },
  { value: "diagnostic", label: "Диагностика" },
  { value: "repair", label: "Ремонт" },
  { value: "sale", label: "Продажа" },
];

interface AddOrderItemButtonProps {
  orderId: string;
  customerId: string;
  excludedInstrumentIds?: string[];
}

function getErrorMessage(error: unknown, fallback: string): string {
  if (isAxiosError(error)) {
    const detail = error.response?.data?.detail;
    if (typeof detail === "string" && detail.trim()) {
      return detail;
    }
  }

  if (error instanceof Error && error.message) {
    return error.message;
  }

  return fallback;
}

export function AddOrderItemButton({
  orderId,
  customerId,
  excludedInstrumentIds = [],
}: AddOrderItemButtonProps) {
  const [deviceId, setDeviceId] = useState("");
  const [instrumentTypeId, setInstrumentTypeId] = useState("");
  const [quantity, setQuantity] = useState(1);
  const [requestedOperations, setRequestedOperations] = useState<
    OrderItemOperation[]
  >(["verification"]);
  const [isCreateDeviceOpen, setIsCreateDeviceOpen] = useState(false);
  const [initialDeviceSerialNumber, setInitialDeviceSerialNumber] = useState("");
  const [initialDeviceSiteId, setInitialDeviceSiteId] = useState<string | null>(
    null,
  );
  const [initialDeviceSiteName, setInitialDeviceSiteName] = useState<
    string | null
  >(null);
  const [isCreateInstrumentTypeOpen, setIsCreateInstrumentTypeOpen] =
    useState(false);
  const addOrderItemMutation = useAddOrderItem(orderId);
  const createDeviceMutation = useCreateDevice();
  const createInstrumentTypeMutation = useCreateInstrumentType();
  const {
    data: instrumentTypes = [],
    isLoading: isInstrumentTypesLoading,
    isError: isInstrumentTypesError,
  } = useInstrumentTypes();

  const activeInstrumentTypes = instrumentTypes.filter(
    (instrumentType) => !instrumentType.archived,
  );

  const handleOperationChange = (operation: OrderItemOperation) => {
    setRequestedOperations((current) =>
      current.includes(operation)
        ? current.filter((value) => value !== operation)
        : [...current, operation],
    );
  };

  const handleAdd = () => {
    if (!deviceId && !instrumentTypeId) {
      return;
    }

    addOrderItemMutation.mutate(
      {
        instrumentId: deviceId || null,
        instrumentTypeId: instrumentTypeId || null,
        quantity: deviceId ? 1 : quantity,
        requestedOperations,
      },
      {
        onSuccess: () => {
          setDeviceId("");
          setInstrumentTypeId("");
          setQuantity(1);
          setRequestedOperations(["verification"]);
        },
      },
    );
  };

  const handleCreateDevice = (data: {
    instrumentTypeId: string;
    name: string;
    serialNumber: string;
  }) => {
    createDeviceMutation.mutate(
      {
        ...data,
        customerId,
        siteId: initialDeviceSiteId,
      },
      {
        onSuccess: (device) => {
          setInitialDeviceSerialNumber("");
          setInitialDeviceSiteId(null);
          setInitialDeviceSiteName(null);
          setDeviceId(device.id);
          setInstrumentTypeId(device.instrumentTypeId);
          setIsCreateDeviceOpen(false);
        },
      },
    );
  };

  const handleCreateInstrumentType = (data: { name: string }) => {
    createInstrumentTypeMutation.mutate(data, {
      onSuccess: (instrumentType) => {
        setInstrumentTypeId(instrumentType.id);
        setIsCreateInstrumentTypeOpen(false);
      },
    });
  };

  return (
    <Stack spacing={2} sx={{ width: "100%", maxWidth: 760 }}>
      <Stack
        direction="row"
        spacing={2}
        sx={{ alignItems: "flex-start", flexWrap: "wrap" }}
      >
        <TextField
          select
          label="Группа СИ"
          value={instrumentTypeId}
          onChange={(event) => setInstrumentTypeId(event.target.value)}
          disabled={isInstrumentTypesLoading || isInstrumentTypesError}
          helperText={
            isInstrumentTypesError
              ? "Не удалось загрузить группы СИ"
              : "Можно добавить позицию по группе без конкретного СИ"
          }
          sx={{
            minWidth: { xs: "100%", sm: 280 },
            flex: { xs: "1 1 100%", sm: "0 1 auto" },
          }}
        >
          <MenuItem value="">Не выбрана</MenuItem>
          {activeInstrumentTypes.map((instrumentType) => (
            <MenuItem key={instrumentType.id} value={instrumentType.id}>
              {instrumentType.name}
            </MenuItem>
          ))}
        </TextField>

        {!deviceId && instrumentTypeId && (
          <TextField
            label="Количество"
            type="number"
            value={quantity}
            onChange={(event) =>
              setQuantity(Math.max(1, Number(event.target.value)))
            }
            slotProps={{ htmlInput: { min: 1, step: 1 } }}
            required
            sx={{ width: 140 }}
          />
        )}
      </Stack>

      <DeviceSelector
        value={deviceId}
        customerId={customerId}
        instrumentTypeId={instrumentTypeId || null}
        excludedInstrumentIds={excludedInstrumentIds}
        onChange={setDeviceId}
        onCreateDevice={(serialNumber, siteId, siteName) => {
          setInitialDeviceSerialNumber(serialNumber);
          setInitialDeviceSiteId(siteId);
          setInitialDeviceSiteName(siteName);
          setIsCreateDeviceOpen(true);
        }}
        requireUnmatchedSerial
      />

      <Stack
        direction="row"
        spacing={1}
        sx={{ alignItems: "center", flexWrap: "wrap" }}
      >
        {OPERATION_OPTIONS.map((operation) => (
          <FormControlLabel
            key={operation.value}
            control={
              <Checkbox
                checked={requestedOperations.includes(operation.value)}
                onChange={() => handleOperationChange(operation.value)}
              />
            }
            label={operation.label}
          />
        ))}

        <Button
          disabled={
            (!deviceId && !instrumentTypeId) ||
            (!deviceId && quantity < 1) ||
            addOrderItemMutation.isPending
          }
          onClick={handleAdd}
          variant="contained"
          sx={{ marginLeft: "auto" }}
        >
          {addOrderItemMutation.isPending ? "Добавление…" : "Добавить позицию"}
        </Button>
      </Stack>

      {addOrderItemMutation.isError && (
        <Typography color="error" variant="body2">
          {getErrorMessage(
            addOrderItemMutation.error,
            "Не удалось добавить позицию",
          )}
        </Typography>
      )}

      <Dialog
        open={isCreateDeviceOpen}
        onClose={() => {
          if (!createDeviceMutation.isPending) {
            setIsCreateDeviceOpen(false);
          }
        }}
        fullWidth
        maxWidth="sm"
      >
        <DialogTitle>Создать новое СИ</DialogTitle>
        <DialogContent>
          <Stack spacing={2} sx={{ pt: 1 }}>
            <Typography variant="body2" color="text.secondary">
              {initialDeviceSiteName
                ? `Новый прибор будет закреплён за объектом «${initialDeviceSiteName}».`
                : "Новый прибор будет создан без привязки к объекту."}
            </Typography>
            <CreateDeviceForm
              key={isCreateDeviceOpen ? "open" : "closed"}
              instrumentTypeId={instrumentTypeId}
              initialSerialNumber={initialDeviceSerialNumber}
              isPending={createDeviceMutation.isPending}
              onSubmit={handleCreateDevice}
              onCreateInstrumentType={() => setIsCreateInstrumentTypeOpen(true)}
            />
            {createDeviceMutation.isError && (
              <Typography color="error" variant="body2">
                {getErrorMessage(
                  createDeviceMutation.error,
                  "Не удалось создать СИ",
                )}
              </Typography>
            )}
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button
            onClick={() => setIsCreateDeviceOpen(false)}
            disabled={createDeviceMutation.isPending}
          >
            Отмена
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog
        open={isCreateInstrumentTypeOpen}
        onClose={() => {
          if (!createInstrumentTypeMutation.isPending) {
            setIsCreateInstrumentTypeOpen(false);
          }
        }}
        fullWidth
        maxWidth="sm"
      >
        <DialogContent>
          <CreateInstrumentTypeForm
            isPending={createInstrumentTypeMutation.isPending}
            onSubmit={handleCreateInstrumentType}
            onCancel={() => setIsCreateInstrumentTypeOpen(false)}
          />
        </DialogContent>
      </Dialog>
    </Stack>
  );
}

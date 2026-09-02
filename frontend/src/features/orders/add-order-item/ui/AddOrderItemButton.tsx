import { useState } from "react";

import { isAxiosError } from "axios";
import {
  Button,
  Checkbox,
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
}

function getErrorMessage(error: unknown): string {
  if (isAxiosError(error)) {
    const detail = error.response?.data?.detail;
    if (typeof detail === "string" && detail.trim()) {
      return detail;
    }
  }

  if (error instanceof Error && error.message) {
    return error.message;
  }

  return "Не удалось добавить позицию";
}

export function AddOrderItemButton({ orderId }: AddOrderItemButtonProps) {
  const [deviceId, setDeviceId] = useState("");
  const [instrumentTypeId, setInstrumentTypeId] = useState("");
  const [quantity, setQuantity] = useState(1);
  const [requestedOperations, setRequestedOperations] = useState<
    OrderItemOperation[]
  >(["verification"]);
  const [isCreateDeviceOpen, setIsCreateDeviceOpen] = useState(false);
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
    createDeviceMutation.mutate(data, {
      onSuccess: (device) => {
        setDeviceId(device.id);
        setInstrumentTypeId(device.instrumentTypeId);
        setIsCreateDeviceOpen(false);
      },
    });
  };

  const handleCreateInstrumentType = (data: { name: string }) => {
    createInstrumentTypeMutation.mutate(data, {
      onSuccess: (instrumentType) => {
        setInstrumentTypeId(instrumentType.id);
        setIsCreateInstrumentTypeOpen(false);
      },
    });
  };

  if (isCreateInstrumentTypeOpen) {
    return (
      <CreateInstrumentTypeForm
        isPending={createInstrumentTypeMutation.isPending}
        onSubmit={handleCreateInstrumentType}
        onCancel={() => setIsCreateInstrumentTypeOpen(false)}
      />
    );
  }

  if (isCreateDeviceOpen) {
    return (
      <CreateDeviceForm
        instrumentTypeId={instrumentTypeId}
        isPending={createDeviceMutation.isPending}
        onSubmit={handleCreateDevice}
        onCreateInstrumentType={() => setIsCreateInstrumentTypeOpen(true)}
      />
    );
  }

  return (
    <Stack spacing={2}>
      <Stack direction="row" spacing={2} sx={{ alignItems: "flex-start" }}>
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
          sx={{ minWidth: 280 }}
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
            onChange={(event) => setQuantity(Math.max(1, Number(event.target.value)))}
            slotProps={{ htmlInput: { min: 1, step: 1 } }}
            required
            sx={{ width: 140 }}
          />
        )}
      </Stack>

      <Stack direction="row" spacing={2} sx={{ alignItems: "center" }}>
        <DeviceSelector
          value={deviceId}
          onChange={setDeviceId}
          onCreateDevice={() => setIsCreateDeviceOpen(true)}
        />
        <Button
          disabled={
            (!deviceId && !instrumentTypeId) ||
            (!deviceId && quantity < 1) ||
            addOrderItemMutation.isPending
          }
          onClick={handleAdd}
          variant="outlined"
        >
          {addOrderItemMutation.isPending ? "Добавление…" : "Добавить позицию"}
        </Button>
      </Stack>

      <Stack direction="row" spacing={1} sx={{ flexWrap: "wrap" }}>
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
      </Stack>

      {addOrderItemMutation.isError && (
        <Typography color="error" variant="body2">
          {getErrorMessage(addOrderItemMutation.error)}
        </Typography>
      )}
    </Stack>
  );
}

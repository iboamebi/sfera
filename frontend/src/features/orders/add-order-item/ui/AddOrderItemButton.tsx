import { useState } from "react";

import {
  Alert,
  Button,
  Checkbox,
  FormControlLabel,
  Stack,
} from "@mui/material";

import { useCreateDevice } from "../../../devices/model/useCreateDevice";
import { CreateDeviceForm } from "../../../devices/ui/CreateDeviceForm";
import { useCreateInstrumentType } from "../../../instrument-type/model/useCreateInstrumentType";
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

export function AddOrderItemButton({ orderId }: AddOrderItemButtonProps) {
  const [deviceId, setDeviceId] = useState("");
  const [instrumentTypeId, setInstrumentTypeId] = useState("");
  const [requestedOperations, setRequestedOperations] = useState<
    OrderItemOperation[]
  >(["verification"]);
  const [isCreateDeviceOpen, setIsCreateDeviceOpen] = useState(false);
  const [isCreateInstrumentTypeOpen, setIsCreateInstrumentTypeOpen] =
    useState(false);
  const addOrderItemMutation = useAddOrderItem(orderId);
  const createDeviceMutation = useCreateDevice();
  const createInstrumentTypeMutation = useCreateInstrumentType();

  const handleOperationChange = (operation: OrderItemOperation) => {
    setRequestedOperations((current) =>
      current.includes(operation)
        ? current.filter((value) => value !== operation)
        : [...current, operation],
    );
  };

  const handleAdd = () => {
    if (!deviceId) {
      return;
    }

    addOrderItemMutation.mutate(
      {
        instrumentId: deviceId,
        requestedOperations,
      },
      {
        onSuccess: () => {
          setDeviceId("");
          setRequestedOperations(["verification"]);
        },
      },
    );
  };

  const handleCreateDevice = (data: {
    instrumentTypeId: string;
    serialNumber: string;
  }) => {
    createDeviceMutation.mutate(data, {
      onSuccess: (device) => {
        setDeviceId(device.id);
        setInstrumentTypeId("");
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
    <Stack spacing={1}>
      <Stack direction="row" spacing={2} sx={{ alignItems: "center" }}>
        <DeviceSelector
          value={deviceId}
          onChange={(value) => {
            setDeviceId(value);
            addOrderItemMutation.reset();
          }}
          onCreateDevice={() => setIsCreateDeviceOpen(true)}
        />

        <Button
          disabled={!deviceId || addOrderItemMutation.isPending}
          onClick={handleAdd}
          variant="outlined"
        >
          {addOrderItemMutation.isPending ? "Добавление…" : "Добавить позицию"}
        </Button>
      </Stack>

      {addOrderItemMutation.isError && (
        <Alert severity="warning">
          {addOrderItemMutation.error?.response?.status === 409
            ? "СИ уже находится в другом активном заказе. Добавление невозможно."
            : "Не удалось добавить позицию в заказ."}
        </Alert>
      )}

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
    </Stack>
  );
}

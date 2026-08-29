import { useState } from "react";

import { Button, Stack } from "@mui/material";

import { useCreateDevice } from "../../../devices/model/useCreateDevice";
import { CreateDeviceForm } from "../../../devices/ui/CreateDeviceForm";
import { useCreateInstrumentType } from "../../../instrument-type/model/useCreateInstrumentType";
import { CreateInstrumentTypeForm } from "../../../instrument-type/ui/CreateInstrumentTypeForm";
import { useAddOrderItem } from "../model/useAddOrderItem";
import { DeviceSelector } from "./DeviceSelector";

interface AddOrderItemButtonProps {
  orderId: string;
  existingInstrumentIds?: string[];
}

export function AddOrderItemButton({
  orderId,
  existingInstrumentIds = [],
}: AddOrderItemButtonProps) {
  const [deviceId, setDeviceId] = useState("");
  const [instrumentTypeId, setInstrumentTypeId] = useState("");
  const [isCreateDeviceOpen, setIsCreateDeviceOpen] = useState(false);
  const [isCreateInstrumentTypeOpen, setIsCreateInstrumentTypeOpen] =
    useState(false);
  const addOrderItemMutation = useAddOrderItem(orderId);
  const createDeviceMutation = useCreateDevice();
  const createInstrumentTypeMutation = useCreateInstrumentType();

  const handleAdd = () => {
    if (!deviceId || existingInstrumentIds.includes(deviceId)) {
      return;
    }

    addOrderItemMutation.mutate(deviceId, {
      onSuccess: () => setDeviceId(""),
    });
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
    <Stack direction="row" spacing={2} sx={{ alignItems: "center" }}>
      <DeviceSelector
        value={deviceId}
        onChange={setDeviceId}
        onCreateDevice={() => setIsCreateDeviceOpen(true)}
        excludedDeviceIds={existingInstrumentIds}
      />

      <Button
        disabled={
          !deviceId ||
          existingInstrumentIds.includes(deviceId) ||
          addOrderItemMutation.isPending
        }
        onClick={handleAdd}
        variant="outlined"
      >
        {addOrderItemMutation.isPending ? "Добавление…" : "Добавить позицию"}
      </Button>
    </Stack>
  );
}

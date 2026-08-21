import { useState } from "react";

import { Button, Stack } from "@mui/material";

import { useAddOrderItem } from "../model/useAddOrderItem";
import { DeviceSelector } from "./DeviceSelector";

interface AddOrderItemButtonProps {
  orderId: string;
}

export function AddOrderItemButton({ orderId }: AddOrderItemButtonProps) {
  const [deviceId, setDeviceId] = useState("");
  const mutation = useAddOrderItem(orderId);

  const handleAdd = () => {
    if (!deviceId) {
      return;
    }

    mutation.mutate(deviceId, {
      onSuccess: () => setDeviceId(""),
    });
  };

  return (
    <Stack direction="row" spacing={2} sx={{ alignItems: "center" }}>
      <DeviceSelector value={deviceId} onChange={setDeviceId} />

      <Button
        disabled={!deviceId || mutation.isPending}
        onClick={handleAdd}
        variant="outlined"
      >
        {mutation.isPending ? "Добавление…" : "Добавить позицию"}
      </Button>
    </Stack>
  );
}

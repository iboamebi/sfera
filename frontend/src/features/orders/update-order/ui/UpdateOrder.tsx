import { useQueryClient } from "@tanstack/react-query";

import type { OrderRead } from "../../model/types";
import { useUpdateOrder } from "../model/useUpdateOrder";
import type { UpdateOrderSchema } from "../model/schema";
import { UpdateOrderError } from "./UpdateOrderError";
import { UpdateOrderForm } from "./UpdateOrderForm";

interface UpdateOrderProps {
  order: OrderRead;
}

export function UpdateOrder({
  order,
}: UpdateOrderProps) {
  const queryClient = useQueryClient();

  const mutation = useUpdateOrder({
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["orders", order.id],
      });
    },
  });

  const handleSubmit = (data: UpdateOrderSchema) => {
    mutation.mutate({
      orderId: order.id,
      data,
    });
  };

  return (
    <>
      <UpdateOrderForm
        order={order}
        onSubmit={handleSubmit}
        isPending={mutation.isPending}
      />

      {mutation.isError && <UpdateOrderError />}
    </>
  );
}

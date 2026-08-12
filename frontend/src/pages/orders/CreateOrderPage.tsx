import { useNavigate } from "react-router-dom";

import { useCreateOrder } from "../../features/orders/create-order/model/useCreateOrder";
import { CreateOrderForm } from "../../features/orders/create-order/ui/CreateOrderForm";

export function CreateOrderPage() {
  const navigate = useNavigate();
  const { mutate } = useCreateOrder({
    onSuccess: (order) => {
      navigate(`/orders/${order.id}`);
    },
  });

  return <CreateOrderForm onSubmit={mutate} />;
}

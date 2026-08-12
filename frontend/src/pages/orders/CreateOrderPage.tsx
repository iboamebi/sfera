import { CreateOrderForm } from "../../features/orders/create-order/ui/CreateOrderForm";
import { useCreateOrder } from "../../features/orders/create-order/model/useCreateOrder";

export function CreateOrderPage() {
  const { mutate } = useCreateOrder();

  return <CreateOrderForm onSubmit={mutate} />;
}

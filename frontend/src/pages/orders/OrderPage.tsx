import { useParams } from "react-router-dom";

import { useOrder } from "../../features/orders/model/useOrder";

export function OrderPage() {
  const { orderId } = useParams<{ orderId: string }>();
  const { data, error, isLoading } = useOrder(orderId ?? "");

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Failed to load order.</div>;
  }

  if (!data) {
    return <div>Order not found.</div>;
  }

  return (
    <div>
      <h1>Order {data.number}</h1>
      <p>ID: {data.id}</p>
      <p>Customer: {data.customerId}</p>
      <p>Status: {data.status}</p>
    </div>
  );
}

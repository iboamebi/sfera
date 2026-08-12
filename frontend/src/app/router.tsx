import { createBrowserRouter } from "react-router-dom";

export const router = createBrowserRouter([
  {
    path: "/orders",
    element: <div>Orders</div>,
  },
  {
    path: "/orders/new",
    element: <div>Create Order</div>,
  },
  {
    path: "/orders/:orderId",
    element: <div>Order</div>,
  },
]);

import { createBrowserRouter } from "react-router-dom";

import { OrdersPage } from "../pages/orders/OrdersPage";

export const router = createBrowserRouter([
  {
    path: "/orders",
    element: <OrdersPage />,
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

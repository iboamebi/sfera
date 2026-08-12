import { createBrowserRouter } from "react-router-dom";

import { CreateOrderPage } from "../pages/orders/CreateOrderPage";
import { OrdersPage } from "../pages/orders/OrdersPage";

export const router = createBrowserRouter([
  {
    path: "/orders",
    element: <OrdersPage />,
  },
  {
    path: "/orders/new",
    element: <CreateOrderPage />,
  },
  {
    path: "/orders/:orderId",
    element: <div>Order</div>,
  },
]);

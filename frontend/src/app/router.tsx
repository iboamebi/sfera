import { createBrowserRouter } from "react-router";

import { CreateOrderPage } from "../pages/orders/CreateOrderPage";
import { OrderPage } from "../pages/orders/OrderPage";
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
    element: <OrderPage />,
  },
]);

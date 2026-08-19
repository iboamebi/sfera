import { createBrowserRouter } from "react-router";

import { RequireAuth } from "../features/auth/ui/RequireAuth";
import { LoginPage } from "../pages/auth/LoginPage";
import { CreateOrderPage } from "../pages/orders/CreateOrderPage";
import { OrderPage } from "../pages/orders/OrderPage";
import { OrdersPage } from "../pages/orders/OrdersPage";

export const router = createBrowserRouter([
  {
    path: "/login",
    element: <LoginPage />,
  },
  {
    path: "/",
    element: (
      <RequireAuth>
        <OrdersPage />
      </RequireAuth>
    ),
  },
  {
    path: "/orders",
    element: (
      <RequireAuth>
        <OrdersPage />
      </RequireAuth>
    ),
  },
  {
    path: "/orders/new",
    element: (
      <RequireAuth>
        <CreateOrderPage />
      </RequireAuth>
    ),
  },
  {
    path: "/orders/:orderId",
    element: (
      <RequireAuth>
        <OrderPage />
      </RequireAuth>
    ),
  },
]);

import { createBrowserRouter } from "react-router";

import { RequireAuth } from "../features/auth/ui/RequireAuth";
import { LoginPage } from "../pages/auth/LoginPage";
import { CustomersPage } from "../pages/customers/CustomersPage";
import { CustomerPage } from "../pages/customers/CustomerPage";
import { MaterialsPage } from "../pages/materials/MaterialsPage";
import { MaterialPage } from "../pages/materials/MaterialPage";
import { OrganizationsPage } from "../pages/organizations/OrganizationsPage";
import { OrganizationPage } from "../pages/organizations/OrganizationPage";
import { VerificationPage } from "../pages/verifications/VerificationPage";
import { CreateOrderPage } from "../pages/orders/CreateOrderPage";
import { OrderPage } from "../pages/orders/OrderPage";
import { OrdersPage } from "../pages/orders/OrdersPage";
import { InstrumentTypePage } from "../pages/instrument-types/InstrumentTypePage";
import { InstrumentTypesPage } from "../pages/instrument-types/InstrumentTypesPage";

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
  {
    path: "/customers",
    element: (
      <RequireAuth>
        <CustomersPage />
      </RequireAuth>
    ),
  },
  {
    path: "/customers/:customerId",
    element: (
      <RequireAuth>
        <CustomerPage />
      </RequireAuth>
    ),
  },
  {
    path: "/organizations",
    element: (
      <RequireAuth>
        <OrganizationsPage />
      </RequireAuth>
    ),
  },
  {
    path: "/organizations/:organizationId",
    element: (
      <RequireAuth>
        <OrganizationPage />
      </RequireAuth>
    ),
  },
  {
    path: "/materials",
    element: (
      <RequireAuth>
        <MaterialsPage />
      </RequireAuth>
    ),
  },
  {
    path: "/materials/:materialId",
    element: (
      <RequireAuth>
        <MaterialPage />
      </RequireAuth>
    ),
  },
  {
    path: "/verifications/:verificationId",
    element: (
      <RequireAuth>
        <VerificationPage />
      </RequireAuth>
    ),
  },
  {
    path: "/instrument-types",
    element: (
      <RequireAuth>
        <InstrumentTypesPage />
      </RequireAuth>
    ),
  },
  {
    path: "/instrument-types/:instrumentTypeId",
    element: (
      <RequireAuth>
        <InstrumentTypePage />
      </RequireAuth>
    ),
  },
]);

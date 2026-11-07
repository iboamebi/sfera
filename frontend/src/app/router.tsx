import { createBrowserRouter } from "react-router";

import { RequireAuth } from "../features/auth/ui/RequireAuth";
import { LoginPage } from "../pages/auth/LoginPage";
import { ChangePasswordPage } from "../pages/auth/ChangePasswordPage";
import { CustomersPage } from "../pages/customers/CustomersPage";
import { CustomerPage } from "../pages/customers/CustomerPage";
import { CreateCustomerPage } from "../pages/customers/CreateCustomerPage";
import { CreateSitePage } from "../pages/customers/CreateSitePage";
import { CreateDevicePage } from "../pages/customers/CreateDevicePage";
import { MaterialsPage } from "../pages/materials/MaterialsPage";
import { MaterialPage } from "../pages/materials/MaterialPage";
import { OrganizationsPage } from "../pages/organizations/OrganizationsPage";
import { OrganizationPage } from "../pages/organizations/OrganizationPage";
import { CreateOrganizationPage } from "../pages/organizations/CreateOrganizationPage";
import { VerificationPage } from "../pages/verifications/VerificationPage";
import { DiagnosticPage } from "../pages/diagnostics/DiagnosticPage";
import { RepairPage } from "../pages/repairs/RepairPage";
import { PriceListPage } from "../pages/price-lists/PriceListPage";
import { CreateOrderPage } from "../pages/orders/CreateOrderPage";
import { OrderPage } from "../pages/orders/OrderPage";
import { OrdersPage } from "../pages/orders/OrdersPage";
import { DevicePage } from "../pages/devices/DevicePage";
import { DevicesPage } from "../pages/devices/DevicesPage";
import { InstrumentTypePage } from "../pages/instrument-types/InstrumentTypePage";
import { InstrumentTypesPage } from "../pages/instrument-types/InstrumentTypesPage";
import { WarehouseStockPage } from "../pages/warehouses/WarehouseStockPage";
import { UsersPage } from "../pages/users/UsersPage";

export const router = createBrowserRouter([
  {
    path: "/login",
    element: <LoginPage />,
  },
  {
    path: "/change-password",
    element: <RequireAuth><ChangePasswordPage /></RequireAuth>,
  },
  {
    path: "/",
    element: <RequireAuth><OrdersPage /></RequireAuth>,
  },
  {
    path: "/orders",
    element: <RequireAuth><OrdersPage /></RequireAuth>,
  },
  {
    path: "/orders/new",
    element: <RequireAuth><CreateOrderPage /></RequireAuth>,
  },
  {
    path: "/orders/:orderId",
    element: <RequireAuth><OrderPage /></RequireAuth>,
  },
  {
    path: "/customers",
    element: <RequireAuth><CustomersPage /></RequireAuth>,
  },
  {
    path: "/customers/new",
    element: <RequireAuth><CreateCustomerPage /></RequireAuth>,
  },
  {
    path: "/customers/:customerId",
    element: <RequireAuth><CustomerPage /></RequireAuth>,
  },
  {
    path: "/customers/:customerId/sites/new",
    element: <RequireAuth><CreateSitePage /></RequireAuth>,
  },
  {
    path: "/customers/:customerId/devices/new",
    element: <RequireAuth><CreateDevicePage /></RequireAuth>,
  },
  {
    path: "/organizations",
    element: <RequireAuth><OrganizationsPage /></RequireAuth>,
  },
  {
    path: "/organizations/new",
    element: <RequireAuth><CreateOrganizationPage /></RequireAuth>,
  },
  {
    path: "/organizations/:organizationId",
    element: <RequireAuth><OrganizationPage /></RequireAuth>,
  },
  {
    path: "/materials",
    element: <RequireAuth><MaterialsPage /></RequireAuth>,
  },
  {
    path: "/materials/:materialId",
    element: <RequireAuth><MaterialPage /></RequireAuth>,
  },
  {
    path: "/verifications/:verificationId",
    element: <RequireAuth><VerificationPage /></RequireAuth>,
  },
  {
    path: "/diagnostics/:diagnosticId",
    element: <RequireAuth><DiagnosticPage /></RequireAuth>,
  },
  {
    path: "/repairs/:repairId",
    element: <RequireAuth><RepairPage /></RequireAuth>,
  },
  {
    path: "/price-lists/:priceListId",
    element: <RequireAuth><PriceListPage /></RequireAuth>,
  },
  {
    path: "/devices",
    element: <RequireAuth><DevicesPage /></RequireAuth>,
  },
  {
    path: "/devices/:deviceId",
    element: <RequireAuth><DevicePage /></RequireAuth>,
  },
  {
    path: "/instrument-types",
    element: <RequireAuth><InstrumentTypesPage /></RequireAuth>,
  },
  {
    path: "/instrument-types/:instrumentTypeId",
    element: <RequireAuth><InstrumentTypePage /></RequireAuth>,
  },
  {
    path: "/warehouses/:warehouseId/stocks",
    element: <RequireAuth><WarehouseStockPage /></RequireAuth>,
  },
  {
    path: "/users",
    element: <RequireAuth><UsersPage /></RequireAuth>,
  },
]);

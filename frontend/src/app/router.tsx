import { lazy, Suspense, type ReactNode } from "react";
import { Typography } from "@mui/material";
import { createBrowserRouter } from "react-router";

import { RequireAuth } from "../features/auth/ui/RequireAuth";

const LoginPage = lazy(() => import("../pages/auth/LoginPage").then((module) => ({ default: module.LoginPage })));
const ChangePasswordPage = lazy(() => import("../pages/auth/ChangePasswordPage").then((module) => ({ default: module.ChangePasswordPage })));
const CustomersPage = lazy(() => import("../pages/customers/CustomersPage").then((module) => ({ default: module.CustomersPage })));
const SitesPage = lazy(() => import("../pages/sites/SitesPage").then((module) => ({ default: module.SitesPage })));
const SitePage = lazy(() => import("../pages/sites/SitePage").then((module) => ({ default: module.SitePage })));
const CreateSiteDirectoryPage = lazy(() => import("../pages/sites/CreateSiteDirectoryPage").then((module) => ({ default: module.CreateSiteDirectoryPage })));
const CustomerPage = lazy(() => import("../pages/customers/CustomerPage").then((module) => ({ default: module.CustomerPage })));
const CreateCustomerPage = lazy(() => import("../pages/customers/CreateCustomerPage").then((module) => ({ default: module.CreateCustomerPage })));
const CreateSitePage = lazy(() => import("../pages/customers/CreateSitePage").then((module) => ({ default: module.CreateSitePage })));
const MaterialsPage = lazy(() => import("../pages/materials/MaterialsPage").then((module) => ({ default: module.MaterialsPage })));
const MaterialPage = lazy(() => import("../pages/materials/MaterialPage").then((module) => ({ default: module.MaterialPage })));
const OrganizationsPage = lazy(() => import("../pages/organizations/OrganizationsPage").then((module) => ({ default: module.OrganizationsPage })));
const OrganizationPage = lazy(() => import("../pages/organizations/OrganizationPage").then((module) => ({ default: module.OrganizationPage })));
const CreateOrganizationPage = lazy(() => import("../pages/organizations/CreateOrganizationPage").then((module) => ({ default: module.CreateOrganizationPage })));
const VerificationPage = lazy(() => import("../pages/verifications/VerificationPage").then((module) => ({ default: module.VerificationPage })));
const VerificationsPage = lazy(() => import("../pages/verifications/VerificationsPage").then((module) => ({ default: module.VerificationsPage })));
const DiagnosticPage = lazy(() => import("../pages/diagnostics/DiagnosticPage").then((module) => ({ default: module.DiagnosticPage })));
const RepairPage = lazy(() => import("../pages/repairs/RepairPage").then((module) => ({ default: module.RepairPage })));
const PriceListPage = lazy(() => import("../pages/price-lists/PriceListPage").then((module) => ({ default: module.PriceListPage })));
const CreateOrderPage = lazy(() => import("../pages/orders/CreateOrderPage").then((module) => ({ default: module.CreateOrderPage })));
const OrderPage = lazy(() => import("../pages/orders/OrderPage").then((module) => ({ default: module.OrderPage })));
const OrdersPage = lazy(() => import("../pages/orders/OrdersPage").then((module) => ({ default: module.OrdersPage })));
const DashboardPage = lazy(() => import("../pages/dashboard/DashboardPage").then((module) => ({ default: module.DashboardPage })));
const DevicePage = lazy(() => import("../pages/devices/DevicePage").then((module) => ({ default: module.DevicePage })));
const DevicesPage = lazy(() => import("../pages/devices/DevicesPage").then((module) => ({ default: module.DevicesPage })));
const InstrumentTypePage = lazy(() => import("../pages/instrument-types/InstrumentTypePage").then((module) => ({ default: module.InstrumentTypePage })));
const InstrumentTypesPage = lazy(() => import("../pages/instrument-types/InstrumentTypesPage").then((module) => ({ default: module.InstrumentTypesPage })));
const WarehouseStockPage = lazy(() => import("../pages/warehouses/WarehouseStockPage").then((module) => ({ default: module.WarehouseStockPage })));
const UsersPage = lazy(() => import("../pages/users/UsersPage").then((module) => ({ default: module.UsersPage })));
const AuditPage = lazy(() => import("../pages/audit/AuditPage").then((module) => ({ default: module.AuditPage })));

function renderPage(page: ReactNode) {
  return (
    <Suspense fallback={<Typography sx={{ p: 3 }}>Загрузка раздела...</Typography>}>
      {page}
    </Suspense>
  );
}









import { CreateDevicePage as CreateCustomerDevicePage } from "../pages/customers/CreateDevicePage";
import { CreateDevicePage as CreateStandaloneDevicePage } from "../pages/devices/CreateDevicePage";






















export const router = createBrowserRouter([
  {
    path: "/login",
    element: renderPage(<LoginPage />,
  },
  {
    path: "/change-password",
    element: <RequireAuth><ChangePasswordPage /></RequireAuth>),
  },
  {
    path: "/",
    element: renderPage(<RequireAuth><DashboardPage /></RequireAuth>),
  },
  {
    path: "/orders",
    element: renderPage(<RequireAuth><OrdersPage /></RequireAuth>),
  },
  {
    path: "/orders/new",
    element: renderPage(<RequireAuth><CreateOrderPage /></RequireAuth>),
  },
  {
    path: "/orders/:orderId",
    element: renderPage(<RequireAuth><OrderPage /></RequireAuth>),
  },
  {
    path: "/customers",
    element: renderPage(<RequireAuth><CustomersPage /></RequireAuth>),
  },
  {
    path: "/sites",
    element: renderPage(<RequireAuth><SitesPage /></RequireAuth>),
  },
  {
    path: "/sites/new",
    element: renderPage(<RequireAuth><CreateSiteDirectoryPage /></RequireAuth>),
  },
  {
    path: "/sites/:siteId",
    element: renderPage(<RequireAuth><SitePage /></RequireAuth>),
  },
  {
    path: "/customers/new",
    element: renderPage(<RequireAuth><CreateCustomerPage /></RequireAuth>),
  },
  {
    path: "/customers/:customerId",
    element: renderPage(<RequireAuth><CustomerPage /></RequireAuth>),
  },
  {
    path: "/customers/:customerId/sites/new",
    element: renderPage(<RequireAuth><CreateSitePage /></RequireAuth>),
  },
  {
    path: "/customers/:customerId/devices/new",
    element: renderPage(<RequireAuth><CreateCustomerDevicePage /></RequireAuth>),
  },
  {
    path: "/organizations",
    element: renderPage(<RequireAuth><OrganizationsPage /></RequireAuth>),
  },
  {
    path: "/organizations/new",
    element: renderPage(<RequireAuth><CreateOrganizationPage /></RequireAuth>),
  },
  {
    path: "/organizations/:organizationId",
    element: renderPage(<RequireAuth><OrganizationPage /></RequireAuth>),
  },
  {
    path: "/materials",
    element: renderPage(<RequireAuth><MaterialsPage /></RequireAuth>),
  },
  {
    path: "/materials/:materialId",
    element: renderPage(<RequireAuth><MaterialPage /></RequireAuth>),
  },
  {
    path: "/verifications",
    element: renderPage(<RequireAuth><VerificationsPage /></RequireAuth>),
  },
  {
    path: "/verifications/:verificationId",
    element: renderPage(<RequireAuth><VerificationPage /></RequireAuth>),
  },
  {
    path: "/diagnostics/:diagnosticId",
    element: renderPage(<RequireAuth><DiagnosticPage /></RequireAuth>),
  },
  {
    path: "/repairs/:repairId",
    element: renderPage(<RequireAuth><RepairPage /></RequireAuth>),
  },
  {
    path: "/price-lists/:priceListId",
    element: renderPage(<RequireAuth><PriceListPage /></RequireAuth>),
  },
  {
    path: "/devices/new",
    element: renderPage(<RequireAuth><CreateStandaloneDevicePage /></RequireAuth>),
  },
  {
    path: "/devices",
    element: renderPage(<RequireAuth><DevicesPage /></RequireAuth>),
  },
  {
    path: "/devices/:deviceId",
    element: renderPage(<RequireAuth><DevicePage /></RequireAuth>),
  },
  {
    path: "/instrument-types",
    element: renderPage(<RequireAuth><InstrumentTypesPage /></RequireAuth>),
  },
  {
    path: "/instrument-types/:instrumentTypeId",
    element: renderPage(<RequireAuth><InstrumentTypePage /></RequireAuth>),
  },
  {
    path: "/warehouses/:warehouseId/stocks",
    element: renderPage(<RequireAuth><WarehouseStockPage /></RequireAuth>),
  },
  {
    path: "/users",
    element: renderPage(<RequireAuth adminOnly><UsersPage /></RequireAuth>),
  },
  {
    path: "/audit",
    element: renderPage(<RequireAuth adminOnly><AuditPage /></RequireAuth>),
  },
]);

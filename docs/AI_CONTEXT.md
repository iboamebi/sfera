# Sfera Project AI Context

## Назначение

Этот документ содержит изменяющееся техническое состояние проекта «Сфера», checkpoints и ближайшее направление работы.

Постоянные правила работы ИИ находятся в:

```text
docs/AI_WORKING_PROTOCOL.md
```

Нормативные архитектурные правила находятся в:

```text
docs/architecture/PROJECT_CONSTITUTION.md
```

## Проект

Сфера — информационная система сервисного центра и метрологической лаборатории.

Основные направления:

- учёт средств измерений;
- поверка;
- ремонт;
- диагностика;
- документы;
- склад;
- финансы;
- интеграция с ФГИС Аршин.

Repository:

```text
git@github.com:iboamebi/sfera.git
```

Working branch:

```text
develop
```

Local root:

```text
~/sfera
```

## Architecture

Project architecture:

```text
DDD + Clean Architecture
```

Dependency direction:

```text
API
  ↓
Application
  ↓
Domain
  ↓
Repository Interface
  ↑
Infrastructure Repository
  ↓
Database
```

Legacy CRUD migration is complete and must not be reintroduced.

## Backend Current State

Backend migration to DDD/Clean Architecture:

```text
COMPLETE
```

Legacy CRUD:

```text
REMOVED
```

Authorization is implemented for concrete business use cases with a defined owner. Do not broaden authorization mechanically.

Current role ownership:

```text
Order
  → OPERATOR / ADMIN

Customer
  → OPERATOR / ADMIN

Organization
  → OPERATOR / ADMIN

Material
  → WAREHOUSE / ADMIN

Warehouse
  → WAREHOUSE / ADMIN

Verification
  → METROLOGIST / ADMIN

Diagnostic
  → TECHNICIAN / ADMIN

Repair
  → TECHNICIAN / ADMIN
```

Do not add authorization to `Device`, `InstrumentType`, `PriceList` or `Workflow` without an explicit business requirement.

Authorization contract:

```text
docs/architecture/AUTHORIZATION.md
```

## Order Items Checkpoint

Order item persistence and read contract are complete:

```text
OrderModel.order_items
        ↓
OrderMapper.to_domain()
        ↓
Domain Order.items
        ↓
OrderRead.items
```

Frontend:

```text
OrderApiDto.items
        ↓
orderMapper
        ↓
OrderRead.items
        ↓
OrderItems
```

`OrderItems` contains presentation only.

## Frontend Current State

Frontend stack:

```text
React 19
TypeScript 7
Vite 8
React Router 8
TanStack Query 5
Axios
Material UI 9
React Hook Form
Zod
```

Architecture:

```text
feature-oriented
+ Feature-Sliced Design principles
```

Current protected routes are defined in `frontend/src/app/router.tsx`:

```text
/
/orders
/orders/new
/orders/:orderId
/customers
/customers/:customerId
/organizations
/organizations/:organizationId
/materials
/materials/:materialId
/verifications/:verificationId
/diagnostics/:diagnosticId
/repairs/:repairId
/price-lists/:priceListId
/instrument-types
/instrument-types/:instrumentTypeId
```

Public route:

```text
/login
```

## Completed Frontend Slices

### Orders

Complete current flows:

- orders list;
- loading/error/empty states;
- order creation;
- order detail;
- order items display;
- order registration;
- cache update after registration;
- customer selection.

### Customer

List/detail integration is implemented, including API/model boundary, query hooks and detail page.

### Organization

List/detail integration is implemented. The organization list is linked to detail.

### Material

List/detail integration is implemented. The material list is linked to detail.

### Verification

Detail read slice is complete:

```text
API DTO
  ↓
mapper
  ↓
frontend model
  ↓
getVerification()
  ↓
useVerification()
  ↓
VerificationPage
  ↓
/verifications/:verificationId
```

### Diagnostic

Detail read slice is complete:

```text
API DTO → mapper → frontend model → getDiagnostic() → useDiagnostic() → DiagnosticPage
```

Route:

```text
/diagnostics/:diagnosticId
```

### Repair

Detail read slice is complete:

```text
API DTO → mapper → frontend model → getRepair() → useRepair() → RepairPage
```

Route:

```text
/repairs/:repairId
```

### PriceList

Detail read slice is complete:

```text
API DTO
  ↓
mapper
  ↓
frontend model
  ↓
getPriceList()
  ↓
usePriceList()
  ↓
PriceListPage
  ↓
/price-lists/:priceListId
```

No confirmed existing frontend source of `priceListId` was found for list→detail navigation, so no link was added.

### InstrumentType

List and detail read slices are complete.

Backend contract includes:

```text
GET /instrument-types/
GET /instrument-types/{instrument_type_id}
POST /instrument-types/
PUT /instrument-types/{instrument_type_id}
POST /instrument-types/{instrument_type_id}/archive
POST /instrument-types/{instrument_type_id}/restore
```

Frontend currently implements only read/list/detail. CRUD mutations remain intentionally absent.

## API Boundary Rule

Common frontend flow:

```text
FastAPI backend
      ↓
Axios API layer
      ↓
backend DTO
      ↓
mapper
      ↓
frontend model
      ↓
React Query hook
      ↓
Page / Feature UI
```

Backend `snake_case` must not leak into UI models. Example:

```text
instrument_id → instrumentId
measurement_type → measurementType
```

Generated TypeScript API client is not used.

## Authentication State

Authentication uses server-side sessions:

```text
Browser
  ↓
HttpOnly session cookie
  ↓
server-side auth_sessions
  ↓
SessionRepository
  ↓
PostgreSQL
```

Authentication and authorization remain separate concerns.

Authentication foundation includes User domain/repository, Argon2 password hashing, session domain/repository/persistence, login/current-user/logout API, HttpOnly cookie and CSRF protection.

Contract:

```text
docs/architecture/AUTHENTICATION.md
```

## Production State

Production topology remains:

```text
ZeroTier client
    ↓
DNS: top.vlsfera.ru
    ↓
10.147.17.242:80
    ↓
nginx
    ├── React SPA
    │     /var/www/sfera
    │
    └── /api/*
          ↓
        127.0.0.1:8000
          ↓
        sfera-backend.service
          ↓
        PostgreSQL
```

Production frontend is built with Vite and served through nginx. Vite development server is not a production dependency.

## Validation Checkpoint

Latest frontend validation:

```text
npm run typecheck — passed
npm run build     — passed
```

Latest build:

```text
1227 modules transformed
vite build — passed
```

Vite reports only a chunk-size warning (>500 kB). This is not a build failure.

Latest frontend feature commit before documentation renewal:

```text
b953cb5 feat: add price list detail route
```

Documentation renewal commit follows this checkpoint.

## Documentation State

Working protocol:

```text
docs/AI_WORKING_PROTOCOL.md
```

Volatile project state:

```text
docs/AI_CONTEXT.md
```

Frontend architecture:

```text
docs/FRONTEND_ARCHITECTURE.md
```

Architecture governance:

```text
docs/architecture/PROJECT_CONSTITUTION.md
docs/ARCHITECTURE.md
docs/MIGRATION_STATUS.md
docs/architecture/MIGRATION_MATRIX.md
docs/architecture/AUTHENTICATION.md
docs/architecture/AUTHORIZATION.md
```

`PROJECT_CONSTITUTION.md` is normative and must not be changed as routine documentation.

## Next Direction

The current frontend phase has completed a broad sequence of read/list/detail slices.

Next work must start with an audit of the actual `develop` state and backend contracts.

Do not:

- add CRUD mechanically;
- invent list→detail links without a confirmed ID source;
- add authorization without an explicit business owner/requirement;
- reintroduce legacy CRUD architecture;
- follow an obsolete roadmap without checking current code.

Select the next independent user scenario from the actual repository state.

## Recovery Checkpoint

After a pause:

1. read `docs/AI_WORKING_PROTOCOL.md`;
2. read `docs/AI_CONTEXT.md`;
3. read relevant architecture/security documents;
4. verify current `develop` and latest commits;
5. audit backend/frontend state;
6. select the next independent user scenario;
7. work one file/small step at a time and validate before continuing.

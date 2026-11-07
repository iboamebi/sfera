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
feat/user-first-login-password
```

Base branch: `develop`.

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

Order read architecture:
- GET /orders/{id} uses dedicated OrderReadService.
- OrderReadRepository separated from command repository.
- Read model contract moved to domain layer.
- Infrastructure provides SQLAlchemy read implementation.

Warehouse stock read architecture:
- WarehouseStockReadService provides warehouse stock queries.
- WarehouseStockReadRepository separated from command repository.
- Warehouse stock read model moved to domain layer.
- Infrastructure provides SQLAlchemy read projection.
- GET /warehouse-stocks/warehouse/{warehouse_id} exposes read contract.

Warehouse stock read slice is complete:
- WarehouseStockReadService;
- WarehouseStockReadRepository;
- WarehouseStockReadData;
- SQLAlchemy read projection;
- GET /warehouse-stocks/warehouse/{warehouse_id};
- frontend warehouse stock page;
- route integration.

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

Order read side is complete:
- OrderReadService
- OrderReadRepository
- OrderReadData
- OrderReadMapper
- frontend order item read contract synchronization

## Audit Trail Checkpoint

Audit Trail foundation and the first transactional integration slice are complete:
- `AuditOperation` and `AuditRecord` application contracts;
- audit repository contracts;
- SQLAlchemy audit repositories;
- `audit_operations` and `audit_records` persistence models;
- Alembic migrations;
- dependency injection;
- Verification create/start/approve/reject audit integration;
- Repair completion audit integration;
- append-only database enforcement.

## Frontend Current State

Frontend uses React, TypeScript, Vite, React Router, TanStack Query, Axios, Material UI, React Hook Form and Zod.

Frontend architecture contract:

```text
docs/FRONTEND_ARCHITECTURE.md
```

### Verification

Backend lifecycle implementation separates registration and execution:
- create persists a Verification in `CREATED`;
- explicit `StartVerification` moves it to `IN_PROGRESS`;
- `started_at` records the actual start time and remains null before start;
- create and start are separately audited in the same Unit of Work as their mutations;
- API read contract exposes `status`, `created_at`, `started_at`, and `decision_at`.

Frontend detail and lifecycle UI are implemented:
```text
API DTO → mapper → frontend model
  ↓
getVerification() → useVerification()
  ↓
VerificationPage
  ├── CREATED → start
  └── IN_PROGRESS → approve / reject
```

Lifecycle mutations use backend start, approve and reject endpoints, invalidate the detail query after success, and display mutation errors. Actions are hidden for archived records and conditional on lifecycle status.

### Order → Verification

Order read contract exposes existing Verification IDs per OrderItem. Frontend OrderItems displays links to existing Verification details and allows creating a Verification for an OrderItem with an assigned Instrument.

Creation sends:
- `orderItemId`;
- `verificationDate`;
- `verificationType`;
- optional free-text `methodology`.

Successful creation navigates to the new Verification detail page.

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

The current authentication contract also includes:
- `must_change_password` persisted on User;
- `ChangePasswordApplicationService` verifies the current password and stores only an Argon2 hash;
- `POST /auth/change-password` is available to authenticated users and retains CSRF validation;
- login and `/auth/me` return `role` and `must_change_password`;
- all business routers, including read endpoints, require authentication and completion of the first-login password change;
- `/auth/login`, `/auth/me`, `/auth/change-password`, `/auth/logout`, and `/health` remain outside the first-login business-route gate.

Current active branch:
```text
feat/user-first-login-password
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

Latest frontend validation before the current Order page layout adjustment:
- `npm run typecheck` passed;
- `npm run build` passed;
- Vite emitted a non-blocking large-chunk warning (>500 kB).

## Initial business-data reset checkpoint — 2026-11-05

- User explicitly approved a one-time clean-slate reset: preserve all Organization rows and their legal requisites unchanged; preserve the existing `alex` user with `admin` role; no other user accounts are expected.
- Alembic revision `a6c8e1f3b520` clears existing Customer, Site, Instrument, Order/OrderItem, Verification, Repair, Diagnostic, Workflow execution, document, Arshin export, warehouse, stock/movement, price-list, methodology, instrument-type and other master/reference rows.
- The migration also clears legacy audit history and all authentication sessions. Existing sessions are invalidated; alex must sign in again. The alex user row, password hash, role, active/password-change flags, organization reference and RBAC assignments are preserved unchanged.
- Roles, permissions and role-permission definitions are retained as system authorization configuration. Only user-role assignments for users other than alex are removed.
- Organizations are not updated, deleted, recreated or re-linked. The migration aborts unless exactly one `users` row exists with `username='alex'` and `role='admin'`.
- The one-time migration uses PostgreSQL `TRUNCATE` for the pre-operational, untrusted audit rows; the row-level append-only trigger remains installed and enabled. This privileged migration-only reset does not change the normal Audit Trail rule. The user confirmed that no valid Verification history has yet been created.
- This reset does not reverse the agreed future Customer / Site / Instrument business model. It only removes existing records; future relationships will be entered by an operator or imported from XLS.
- The migration is intentionally irreversible. A database backup is required before applying it; restoring deleted rows requires restoring that backup, not Alembic downgrade.

## Order → Instrument creation and registration checkpoint — 2026-11-07

Frontend changes on `feat/user-first-login-password`:
- Device API/model contract carries required `customerId` and optional `siteId`.
- Device creation from the Order item form passes the Order's `customerId`.
- The Order item DeviceSelector filters instruments to the current Order's Customer, then optionally by InstrumentType.
- A newly created Device is selected in the Order item form after the create API call succeeds.
- Device creation API errors are displayed inside the inline creation form.
- Error-state UI change commit: `ad92bdb712850c9c54d39858b21d6a516665240c`.

User confirmed production browser smoke test on 2026-11-07:
- created an Instrument from the Order form;
- created and added the OrderItem;
- successfully registered the Order;
- browser back navigation and reopening the Order work;
- the OrderItem and associated Instrument are displayed;
- "Создать поверку" and "Редактировать карту СИ" are available;
- the Instrument card opens successfully.

The DeviceSelector cross-Customer filtering scenario remains unconfirmed. Do not repeat successful create/add/register or Instrument card checks unless a regression occurs.

## Verification creation UI review — 2026-11-07

User browser observations:
- Create Verification exposes verification type, free-text Methodology field, and "Сохранить поверку".
- Methodology field does not search or offer choices.

Source audit:
- OrderItems currently offers PRIMARY / PERIODIC / AFTER_REPAIR as three VerificationType values.
- Create flow posts `order_item_id`, `verification_date`, `verification_type`, and optional free-text `methodology`.
- Successful create navigates to `/verifications/{id}`.
- The Verification detail page exposes the lifecycle action for CREATED as Start Verification, and approve/reject actions for IN_PROGRESS. It does not expose a separate verification-registration command.
- Runtime Method / MethodVersion catalogue and search endpoint/UI are not present in the inspected frontend slice. `docs/metrology/VERIFICATION_METHODS.md` is an analytical registry, not a runtime lookup API.

Regulatory terminology review:
- Current Article 13(1) of Federal Law 102-FZ classifies verification before commissioning as primary and verification during operation, including after repair, as periodic.
- Therefore AFTER_REPAIR should not be treated as a third peer legal verification type by default. It is better modeled as the reason/occasion (after repair) alongside the legal type (primary/periodic). Do not remove or migrate the enum until compatibility and historical-data implications are audited.

Open next steps:
- Decide the domain split between legal verification type (PRIMARY/PERIODIC) and occasion/reason (e.g. AFTER_REPAIR), then audit API/DB/history compatibility before implementation.
- Define runtime Method/MethodVersion lookup contract before adding a searchable method selector; do not mistake the Markdown registry for a runtime catalogue.

## Order page layout checkpoint — 2026-11-07

User proposed improving page layout and button placement rather than changing button behavior or business semantics.

Source inspection confirmed the Order page composition:
- `OrderDetails` contains order summary, OrderItems, and per-item actions including Verification creation.
- `OrderActions` contains the separate Order registration mutation.
- `UpdateOrder` contains the form for planned issue date and comment.

Minimal frontend change in `frontend/src/pages/orders/OrderPage.tsx`:
- kept all existing actions, handlers, conditions, and mutations unchanged;
- visually separated Order registration into its own outlined card with a clear heading and explanatory text;
- placed planned issue date/comment editing into a separate outlined card with its own heading and explanation;
- increased vertical spacing between page sections.

Commit: `6a007025bf6ae5e597c73b1f2e14ca40fdc0a4e1`.

Local typecheck/build and browser review are still required before considering this layout adjustment complete.

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
- Order registration audit integration (`order.registered`) using the same operation id as `OrderRegistered`;
- Repair completion audit integration (`repair.completed`) recording status/result changes;
- Diagnostic completion audit integration (`diagnostic.completed`) recording conclusion changes;
- shared SQLAlchemy session with the business mutation and `UnitOfWork`;
- automated audit/verification tests;
- PostgreSQL trigger enforcement preventing `UPDATE` and `DELETE` on `audit_records` through migration `9f2a6c4d8e10`;
- functional database check: `INSERT` allowed, `UPDATE` and `DELETE` blocked with SQLSTATE `55000`.

Current scope:

```text
Audit foundation:              COMPLETE
Persistence:                   COMPLETE
Verification integration:      COMPLETE
System-wide audit coverage:    IN PROGRESS
Audit read/query:              OPEN
DB append-only enforcement:    COMPLETE
```

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
/warehouse-stocks/warehouse/:warehouseId
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

Backend lifecycle implementation separates registration and execution:

- create persists a verification in `CREATED`;
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

Lifecycle mutations use the backend start, approve and reject endpoints, invalidate the detail query after success, and display mutation errors. Actions are hidden for archived records and are conditional on lifecycle status.

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

API contract documentation commit:

```text
f769417 docs: align authentication contract with implementation
```

Latest API test correction:

```text
83251a2 test: inspect FastAPI included routers for first-login gate
```

Local backend validation after that correction:
- 30 tests passed;
- Ruff check passed;
- formatting check passed.

Frontend first-login integration and user administration UI are implemented on this branch. The latest local `npm run typecheck` and `npm run build` passed after Order → Verification navigation was added; Vite emits a non-blocking large-chunk warning.

User administration backend currently supports:
- administrator-only user listing, including inactive accounts and optional archived accounts;
- administrator-only user creation with a selected role;
- administrator-only role changes;
- administrator-only activation/deactivation for non-archived accounts;
- cryptographically secure temporary password generation;
- Argon2 password hash storage and mandatory first-login password change;
- temporary password returned only in the creation response;
- duplicate username mapped to HTTP 409, including archived usernames;
- missing target user mapped to HTTP 404 for role changes.

Frontend user administration UI is implemented on the active branch:
- list users, optionally including archived accounts;
- create users with a selected role;
- display and copy the temporary password from the creation response, with an explicit hide action;
- change roles;
- activate/deactivate non-archived accounts;
- archive and restore accounts.

The existing `alex` account role was updated to ADMIN after inspecting its actual local database row.

Order → Verification navigation is implemented and locally validated on this branch. Backend read repository, read model, API schema/mapper, frontend DTO/model/mapper, and OrderItems links expose existing verifications for each order item. Focused backend mapper test passed (1 passed); scoped Ruff check passed; scoped format check passed; frontend `npm run typecheck` and `npm run build` passed. Vite reports only the non-blocking large-chunk warning (>500 kB). Full backend suite was not run as part of this checkpoint.

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

Latest frontend validation before the lifecycle error-state update:

```text
npm run typecheck — passed
npm run build     — passed
1276 modules transformed
```

Vite reports only a chunk-size warning (>500 kB). This is not a build failure. The lifecycle error-state update still requires local typecheck/build validation.

Backend validation at the latest architecture checkpoint:

```text
137 passed
1 warning
```

The Order domain-event foundation was separately validated with:

```text
3 passed
```

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

Verification method registry:

```text
docs/metrology/VERIFICATION_METHODS.md
```

`PROJECT_CONSTITUTION.md` is normative and must not be changed as routine documentation.

## Next Direction

Current active work is first-login authentication and user administration. Sequence:

1. Frontend login/current-user integration, forced password-change screen, and protected route guard are implemented; local typecheck/build validation is the current step.
2. Validate the user administration API list/create slice locally.
3. Role change, activation/deactivation, archive and restore Application/API slices are implemented on the active branch; locally validate the user administration test slice and scoped lint/format checks.
4. User administration frontend UI and API integration are implemented; run local typecheck/build and review the UI behavior.
5. The existing `alex` role update was completed locally after inspecting the actual database row.
6. Complete Order → Verification navigation using the confirmed order-item/verification relationship, then run local backend and frontend validation.

The metrology methodology consolidation direction below remains valid but is not the active implementation stage.

The current frontend phase has completed a broad sequence of read/list/detail slices.

The backend DDD/Clean Architecture migration is complete. Verification registration and execution are distinct application use cases. The Verification lifecycle is:

```text
CREATED → IN_PROGRESS → DECIDED
                         ├── SUITABLE
                         └── UNSUITABLE
```

The current metrology stage is to consolidate verification methodology knowledge before introducing methodology-specific execution models:

- maintain the verification methods registry;
- accumulate and analyze real verification methods;
- record completeness and unresolved normative questions explicitly;
- keep Method / MethodVersion / MethodVariant distinct from Verification;
- audit the Verification domain/application/infrastructure model against the documented lifecycle and invariants.

Do not:

- add CRUD mechanically;
- invent list→detail links without a confirmed ID source;
- add authorization without an explicit business owner/requirement;
- reintroduce legacy CRUD architecture;
- follow an obsolete roadmap without checking current code;
- implement a universal verification engine;
- introduce universal measurement or uncertainty models before method analysis requires them;
- encode incomplete verification methods as finalized normative rules;
- implement methodology-specific persistence/UI prematurely.

## Order Lifecycle Audit Checkpoint

Дата: 2026-08-23

Проведён аудит Order lifecycle без изменения кода.

Документ:

```text
docs/architecture/ORDER_LIFECYCLE_AUDIT.md
```

Основные выводы:

- Order lifecycle сейчас реализован до состояния REGISTERED.
- Реализованы:
  - create;
  - add_item;
  - update;
  - register.

- Не реализованы переходы:
  - REGISTERED → IN_WORK;
  - IN_WORK → WAITING;
  - WAITING → COMPLETED;
  - COMPLETED → ISSUED;
  - ISSUED → CLOSED.

Аудит связей:

OrderItem является центром исполнения работ:

OrderItem
 ├── Repair
 ├── Diagnostic
 └── WorkflowInstance

Verification является отдельным результатом поверки и не имеет подтверждённой orchestration-связи с OrderItem.

Workflow domain существует:
- Workflow;
- WorkflowInstance;
- WorkflowApplicationService.

Но интеграция с бизнес-сценариями отсутствует.

## DDD Events Foundation Checkpoint

Статус: COMPLETE

Реализовано:

- `AggregateRoot` с накоплением domain events;
- `DomainEvent` с `event_id`, `occurred_at` и опциональным `operation_id`;
- `OrderRegistered` domain event;
- `Order.register()` создаёт `OrderRegistered`;
- `UnitOfWork` регистрирует aggregate для последующего сбора событий;
- `SqlAlchemyUnitOfWork` после успешного commit собирает события и передаёт их в `EventDispatcher`;
- `operation_id` из `OperationContext` переносится в domain event;
- `EventDispatcher` выполняет зарегистрированные handlers.

Текущая реализация связывает операцию и domain event на границе UnitOfWork.

## Recovery Checkpoint

After a pause:

1. read `docs/AI_WORKING_PROTOCOL.md`;
2. read `docs/AI_CONTEXT.md`;
3. read relevant architecture/security documents;
4. verify current `develop` and latest commits;
5. audit backend/frontend state;
6. select the next independent user scenario;
7. work one file/small step at a time and validate before continuing.


## Audit Trail — Repair completion checkpoint

- Added transactional audit persistence for `RepairApplicationService.complete`.
- Stable action: `repair.completed`; entity type: `repair`.
- Captures status and result old/new values; actor and initiator are the authenticated user.
- Audit repositories are injected through the existing dependency provider and share the Unit of Work session boundary.
- Added focused Application tests for successful audit persistence and unauthorized access.
- Remaining Repair operations (create/start/cancel) are not yet audited.
- Local validation is pending for this slice.


## Audit Trail — Diagnostic completion checkpoint

- Added transactional audit persistence for `DiagnosticApplicationService.complete`.
- Stable action: `diagnostic.completed`; entity type: `diagnostic`.
- Captures conclusion old/new values; actor and initiator are the authenticated user.
- Audit repositories are injected through the existing dependency provider and share the Unit of Work session boundary.
- Added focused Application tests for successful audit persistence and unauthorized access.
- Diagnostic creation and recommendation changes remain outside this slice pending separate business-significance review.
- Repair completion audit was locally validated: 2 focused tests passed; Ruff check and format check passed.
- Diagnostic completion local validation is pending.


## Business model checkpoint — Customer / Site / Order grouping (2026-11-04)

- Confirmed: Site belongs to Customer, not to payer Organization.
- If the Customer has one legal entity, its Organization may also act as the customer-facing contracting party; with multiple legal entities, Customer is the shared client identity and Organizations are separate legal entities selectable per transaction. Customer and Organization remain distinct data-model entities.
- Customer may own multiple Sites; each Site groups concrete instrument instances.
- One Order may include a subset of a Site's instruments and instruments from multiple Sites.
- Readiness/release is evaluated per Site within the specific Order using only that Order's OrderItems. Instruments assigned to the Site but absent from the Order are outside this Order's scope and do not block release.
- Different Site groups in one Order may be released independently when their included instruments are ready.
- Verification queue is a separate production-planning concept. It may group work across orders/Sites, but it does not change ownership, Order membership, Verification facts or Site release readiness.
- Current code mismatch: Site requires organization_id; Instrument.site_id exists but is absent from Device Domain/mapper/commands/API; Verification is linked to OrderItem; no dedicated verification queue use case/entity was found.
- Updated business model: docs/architecture/CUSTOMER_ORGANIZATION_SITE_MODEL.md.
- Detailed source audit: Checkpoint 14 in docs/architecture/LEGACY_FUNCTIONALITY_AUDIT.md.
- No application code or database schema changed in this checkpoint.



## Customer / Organization / Site dependency checkpoint (2026-11-04)

Current source inspected at HEAD `a376aac`; detailed findings are in Checkpoint 15 of `docs/architecture/LEGACY_FUNCTIONALITY_AUDIT.md`.

- Customer still requires one Organization through Domain, Application, ORM, API and frontend. The `customer_organizations` table/ORM relationship exists and is backfilled, but the active Customer workflow does not use it.
- Site is still Organization-owned through Domain, command, Application, repository, mapper, ORM and API; frontend Site management does not exist.
- Instrument ORM has nullable `site_id`, but Device Domain/mapper/commands/API/frontend omit it. Instrument has no direct `customer_id` in the inspected ORM model, so ownership of instruments without a Site is not represented.
- Order still requires `organization_id`; OrderApplicationService copies it from Customer. Order also has optional `site_id`, distinct from Instrument.site_id.
- The existing migrations do not safely establish Customer ownership for Sites. Deriving Customer from Site.organization_id is ambiguous if multiple Customers share one Organization.
- No local/production database inventory or applied migration revision has been inspected. Do not write a destructive or data migration before this inventory.
- Next: complete reference inventory, then inspect local database rows/revision and define a data-preserving transition. No code/schema change in this checkpoint.


## Site ownership transition checkpoint — 2026-11-05

- Site now belongs to Customer through Domain, command, Application, repository, mapper, ORM and API.
- The Site list endpoint by owner is now `GET /sites/customer/{customer_id}`; create/read schemas expose `customer_id`.
- Customer has the inverse ORM `sites` relationship; Organization no longer has a Site relationship.
- Alembic revision `9f2a6c4d8e13` replaces `sites.organization_id` with required `sites.customer_id`.
- The migration aborts when Site rows exist, because Organization → Customer cannot be inferred safely. Last supplied database inventory reported 0 Sites.
- `Order.site_id` and `Instrument.site_id` remain nullable and unchanged.
- Backend Site API, Application, Repository and Mapper tests were updated for Customer ownership.


## Customer / Organization / Site Model Checkpoint — 2026-11-05

Business decisions:
- Customer is an independent customer context and does not own or contain a list of Organizations.
- Organization is an independent legal-entity record. Its legal requisites must be preserved.
- No permanent Customer–Organization association is maintained. Existing `customer_organizations` rows are not trusted business relationships and are not migrated.
- During order work, the operator will be able to select the relevant Organization and Site context. The interface assists with search and selection; it must not infer or create permanent Customer–Organization links. Exact order-context persistence and Organization cardinality are a separate implementation decision.
- Site belongs to Customer. A Customer may have multiple Sites.
- Instrument belongs directly to Customer; `site_id` is optional. If assigned, Site and Instrument must belong to the same Customer. Direct `Instrument.customer_id` ownership and its validation are a subsequent implementation stage.
- Site is a location/grouping and instrument-discovery aid, not a required production step. An Instrument without Site remains usable in orders and all production operations.
- Order belongs to Customer. Site selection in order workflows is used to find and select instruments; it does not change an Instrument's permanent Site assignment.

Implementation stage 1 is the removal of the obsolete Customer–Organization association from ORM, DI, Application, API and migrations while preserving Organization records and requisites. Follow-up stages cover Instrument ownership, order context, Site-based instrument discovery and controlled Site reassignment history.


## Initial business-data reset checkpoint — 2026-11-05

- User explicitly approved a one-time clean-slate reset: preserve all Organization rows and their legal requisites unchanged; preserve the existing `alex` user with `admin` role; no other user accounts are expected.
- Alembic revision `a6c8e1f3b520` clears existing Customer, Site, Instrument, Order/OrderItem, Verification, Repair, Diagnostic, Workflow execution, document, Arshin export, warehouse, stock/movement, price-list, methodology, instrument-type and other master/reference rows.
- The migration also clears legacy audit history and all authentication sessions. Existing sessions are invalidated; alex must sign in again. The alex user row, password hash, role, active/password-change flags, organization reference and RBAC assignments are preserved unchanged.
- Roles, permissions and role-permission definitions are retained as system authorization configuration. Only user-role assignments for users other than alex are removed.
- Organizations are not updated, deleted, recreated or re-linked. The migration aborts unless exactly one `users` row exists with `username='alex'` and `role='admin'`.
- The one-time migration uses PostgreSQL `TRUNCATE` for the pre-operational, untrusted audit rows; the row-level append-only trigger remains installed and enabled. This privileged migration-only reset does not change the normal Audit Trail rule. The user confirmed that no valid Verification history has yet been created.
- This reset does not reverse the agreed future Customer / Site / Instrument business model. It only removes existing records; future relationships will be entered by an operator or imported from XLS.
- The migration is intentionally irreversible. A database backup is required before applying it; restoring deleted rows requires restoring that backup, not Alembic downgrade.

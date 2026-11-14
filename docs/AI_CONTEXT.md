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
develop
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


## Order → Instrument creation and registration checkpoint — 2026-11-07

Frontend changes on `feat/user-first-login-password`:

- Device API/model contract carries required `customerId` and optional `siteId`.
- Device creation from the Order item form passes the Order's `customerId`.
- The Order item DeviceSelector filters instruments to the current Order's Customer, then optionally by InstrumentType.
- A newly created Device is selected in the Order item form after the create API call succeeds.
- Device creation API errors are now displayed inside the inline creation form instead of leaving the form open without feedback.
- Error-state UI change commit: `ad92bdb712850c9c54d39858b21d6a516665240c`.

User confirmed production browser smoke test on 2026-11-07:
- created an Instrument from the Order form;
- created and added the OrderItem;
- successfully registered the Order.

This confirms the inline Instrument creation → OrderItem addition → Order registration path. It does not yet confirm the selector's existing-instrument filtering behavior across two different Customers.

Next local validation:
- open an Order for a Customer with at least one existing Instrument and confirm that Instrument appears in the selector;
- confirm an Instrument owned by another Customer is absent.

Do not repeat the already successful create/add/register scenario unless a regression occurs.


Follow-up browser validation reported by the user on 2026-11-07:
- returning from the previous page works;
- reopening the same registered Order shows its OrderItem;
- the associated Instrument is displayed;
- the actions "Создать поверку" and "Редактировать карту СИ" are available;
- the Instrument card opens successfully.

This confirms persistence/readback of the registered OrderItem and Instrument after navigation, plus access to the Instrument card. It does not confirm the behavior of the DeviceSelector for instruments belonging to another Customer.

Next useful browser scenario: exercise "Создать поверку" for the registered OrderItem and verify that the created Verification is linked to that OrderItem. Do not repeat order creation/registration or Instrument card access checks.


## Verification creation UI review — 2026-11-07

User browser observations:
- Create Verification exposes verification type, free-text Methodology field, and "Сохранить поверку".
- Methodology field does not search or offer choices.
- User found multiple visible actions named "Зарегистрировать" and "Сохранить" and could not distinguish their purpose; exact screen placement needs a screenshot before changing labels/actions.

Source audit:
- OrderItems currently offers PRIMARY / PERIODIC / AFTER_REPAIR as three VerificationType values.
- `VerificationType` is a Domain value object with those three enum values.
- Create flow posts `order_item_id`, `verification_date`, `verification_type`, and optional free-text `methodology`.
- Successful create navigates to `/verifications/{id}`.
- The Verification detail page currently exposes the lifecycle action for CREATED as "Start verification" (English in source), and approve/reject actions for IN_PROGRESS. It does not expose a separate verification-registration command.
- Runtime Method / MethodVersion catalogue and search endpoint/UI are not present in the inspected frontend slice. `docs/metrology/VERIFICATION_METHODS.md` is a working analytical registry, not a runtime lookup API.

Regulatory terminology review:
- From 2025-03-01, current wording of Article 13(1) of Federal Law 102-FZ classifies verification before commissioning as primary and verification during operation, including after repair, as periodic.
- Minpromtorg recommendations dated 2025-03-31 clarify that post-repair verification during operation is periodic; where an existing method describes a primary-verification volume after repair, that volume may still be required, while the legal classification is periodic.
- Therefore AFTER_REPAIR should not be treated as a third peer legal verification type by default. It is better modeled as the reason/occasion (after repair) alongside the legal type (primary/periodic), with the method defining the required scope. Do not remove or migrate the enum until compatibility and historical-data implications are audited.

References reviewed:
- Federal Law 102-FZ Article 13: https://www.consultant.ru/document/cons_doc_LAW_77904/3bfb763ea01f7fc945dd7b589037fea5b6c90643/
- Minpromtorg letter/recommendations 31.03.2025 No. АГ-35953/10: https://base.garant.ru/411846506/

Open next steps:
- Clarify with a screenshot which exact page contains the "Зарегистрировать" and "Сохранить" buttons, then align labels with Order vs Verification lifecycle actions.
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

## Order item Instrument card navigation checkpoint — 2026-11-07

- In `frontend/src/features/orders/ui/OrderItems.tsx`, the Instrument name is now an inline link when `instrumentId` exists.
- The link opens the same edit route as the former "Редактировать карту СИ" button: `/devices/{instrumentId}?edit=1&returnToOrder={orderId}`.
- The separate "Редактировать карту СИ" button was removed.
- When no Instrument is assigned, the displayed name remains non-clickable; the existing "Назначить СИ" action remains available.
- No navigation target, mutation, or business behavior was otherwise changed.
- Commit: `3744a18a1fae9709f776c68590cd315388c7534f`.
- Local typecheck/build and browser verification are pending.


## Instrument card link visual emphasis — 2026-11-07

- User confirmed the previous local typecheck, build, and browser checks passed: the Instrument name opens the card in edit mode, return navigation goes back to the same Order, and the separate edit button is absent.
- Updated the inline Instrument link in `frontend/src/features/orders/ui/OrderItems.tsx` to use the theme's `primary` color and semibold text, retaining hover underline. This follows the visual link treatment used for Order numbers in `OrderListItem`.
- Navigation behavior is unchanged.
- Commit: `f26987b851be1f16883dcca2a352f23baf72a3f4`.
- Local typecheck/build and browser confirmation of the visual emphasis are pending.

## Order items table layout checkpoint — 2026-11-07

- Refactored `frontend/src/features/orders/ui/OrderItems.tsx` from vertically stacked position blocks into a horizontally structured MUI table.
- Columns: position number, Instrument name, Instrument type, model, serial number, requested operations, and right-aligned actions.
- Instrument name remains a primary-colored link to the same Instrument edit route with return-to-Order navigation.
- Existing verification links are displayed beneath the Instrument name.
- Actions are grouped in the rightmost column; assignment, Verification creation, and operation editing forms expand beneath their corresponding table row.
- Existing mutation hooks, handlers, visibility conditions, payloads, and navigation targets were preserved; no backend/API/domain changes.
- The table has a minimum width and horizontal scrolling through MUI TableContainer for narrower viewports.
- Implementation commits:
  - `3676dfab7c61c4286f174bb681ec3ad58a6a2fb4` — table layout;
  - `79b5ff3f84fafd3045d38207b6f8e5078af6f1c3` — stable React fragment key.
- Local typecheck/build and browser review of table layout and expanded actions are pending.


## Order registration and parameter controls checkpoint — 2026-11-07

- The Order page now shows the separate registration card only while Order.status === NEW. After successful registration, the updated order cache causes the card to disappear; the status chip in OrderDetails remains the visible registration/status indicator.
- The planned issue date/comment form remains available as a separate section; its Save button is aligned to the left rather than stretching across the page.
- The Register button is also aligned to the left while the order is still NEW.
- No order lifecycle, update, registration mutation, or API behavior was changed.
- Local typecheck/build and browser verification are pending.

## Order comment inline editing checkpoint — 2026-11-07

- The Order card now displays the comment in read-only mode with a compact "Редактировать" action.
- Editing opens an inline multiline field with "Сохранить" and "Отмена"; successful save closes the editor and invalidates the Order detail query.
- The "Параметры заказа" form now contains only the planned issue date.
- Updating the planned issue date explicitly resubmits the current comment to preserve it because the existing backend update command accepts both fields as nullable values and does not distinguish omitted fields from explicit null.
- Comment editing reuses the existing Order PATCH API and `useUpdateOrder` mutation; no backend contract or persistence behavior was changed.
- The existing order update timestamp remains the only displayed timestamp. Per-comment author/time/reason metadata remains a deferred enhancement.
- Local frontend typecheck, build, and browser verification are pending.

## Order comment save API correction — 2026-11-07

- Fixed `PATCH /orders/{order_id}`: after `OrderApplicationService.update`, the API now reloads and returns the `OrderRead` read model through `OrderReadService`, consistent with other Order mutation endpoints. Previously it returned the domain `Order` directly despite declaring `response_model=OrderRead`, which could fail response validation (e.g. missing `customer_name`).
- Added a focused API router test asserting that update returns the read model.
- Corrected the Order page helper text to mention only the planned issue date; comment editing remains inline in OrderDetails.
- Backend test and local frontend/browser validation are pending.


## Order parameter save visibility checkpoint — 2026-11-07

- In `frontend/src/features/orders/update-order/ui/UpdateOrderForm.tsx`, the planned-issue-date form now renders its Save button only while React Hook Form reports `isDirty`.
- The form resets its baseline values when the Order's `plannedIssueAt` changes after a successful reload, so the Save button disappears after saving and also disappears if the user restores the original date.
- No API, backend, or business behavior changed.
- Implementation commit: `ad428dedf1b059e8fb92cd09037365e34d59268f`.
- Local typecheck/build and browser confirmation are pending.


## Order planned issue date editor placement checkpoint — 2026-11-07

- Removed the separate `Параметры заказа` card from `OrderPage`.
- Moved the existing planned-issue-date editor into the Order details card, in the same metadata section as the other order dates.
- The date picker label is now `Планируемая выдача`; its Save button remains conditional on form dirtiness and disappears when the value returns to its saved baseline.
- The existing update mutation, comment-preservation behavior, and API contract are unchanged.
- Implementation commits: `4b9512b`, `cb19fa6`, `1ee86bf`, `0da8dd0`.
- Local typecheck/build and browser review are pending.


## Order header and date metadata checkpoint — 2026-11-07

- Moved the customer name into the Order card header beneath the order number; the separate Customer row was removed.
- Replaced the separate Created, Received, and Updated metadata rows with a compact two-column date table.
- Kept the planned issue date editor and issued date display in the existing details section.
- Used the existing `OrderRead.customerName` field; removed the now-unnecessary customer detail query from OrderDetails.
- No API, backend, or business behavior changed.
- Implementation commit: `3f33f7116f6d2844ea93aa4b8b294e50bbb88fb6`.
- Local frontend typecheck, build, and browser review are pending.

## Order issued date table checkpoint — 2026-11-07

- Moved the existing `Выдан` date row into the same compact two-column metadata table as `Создан`, `Получен`, and `Изменён`.
- The displayed value still comes from `OrderRead.issuedAt`; no date formatting, lifecycle, API, or business behavior changed.
- Implementation commit: `82203d4cacb39c28d73f434e5afc7fe393e19556`.
- Local frontend typecheck, build, and browser review are pending.

## Application navigation and admin user access checkpoint — 2026-11-08

- Frontend previously exposed `/users` directly but had no shared application navigation; users had to know or remember the URL.
- Added `frontend/src/app/AppShell.tsx` as the minimal authenticated application shell.
- Main navigation now provides direct access to Orders, Customers, Organizations, Instruments, and Materials.
- Administrators additionally see a direct `Пользователи` navigation entry.
- The authenticated username is displayed in the application header.
- `RequireAuth` now supports an `adminOnly` guard and wraps authenticated pages in the application shell; the password-change page remains outside the shell.
- The `/users` route is now explicitly frontend-admin-only and redirects non-admin users to `/orders`. Backend authorization remains the security boundary.
- No backend/API/domain behavior was changed.
- Implementation commits:
  - `26d5d743eb5bba87a4596240fe176efb8edc1be8` — application navigation shell;
  - `7d3196e97c99f66ad1e17259ebc01506f728d171` — authenticated shell and admin guard;
  - `d1d4f7e49b0fd88de49203c8e8ed051d4e00208f` — admin-only Users route;
  - `98d17e3959e26b4a5bd654ff2aff7f937058b15f` — explicit ReactNode type.
- Local frontend typecheck, build, and browser review are required before considering this navigation stage complete.


## Last active administrator protection checkpoint — 2026-11-08

- Confirmed the user-administration backend previously allowed the last active administrator to be archived, deactivated, or demoted.
- Added an Application error for attempts that would leave zero active, non-archived administrators; the API maps it to HTTP 409.
- Added a UserRepository operation that loads all user rows with deterministic ordering and `SELECT FOR UPDATE`; the existing Unit of Work holds these locks through the state change and commit, serializing concurrent administrator lifecycle operations.
- Applied the guard to archive, deactivation, and role demotion. Inactive and archived administrators do not count as available administrators; promoting, activating, restoring, and non-admin lifecycle changes retain their existing behavior.
- Added Application regression tests for all three blocked operations, allowed archive when a second active administrator exists, and exclusion of inactive administrators; added API 409 mapping tests.
- Backend and frontend local validation have not yet been run for this checkpoint.


## User Authentication UI Checkpoint — 2026-11-08

Current branch: `feat/user-first-login-password`.

Verified from current source:

- Backend already exposes `POST /auth/logout`, revokes the current server-side session, and clears the authentication and CSRF cookies.
- Frontend previously displayed the username in `AppShell` but had no logout action.
- Added frontend logout API adapter and React Query mutation.
- Added **Выйти** action to the authenticated application header. On confirmed server logout, the frontend clears the query cache and navigates to `/login`; on failure, the user remains on the page and sees an error.
- Updated `docs/architecture/AUTHENTICATION.md` with the frontend logout flow.
- Last-active-administrator protection was already present in Application service and frontend UI before this checkpoint. Backend guards cover archive, deactivate, and demote; service tests cover the last-admin rejection and allow changes when another active admin exists. Do not duplicate this protection without finding a concrete gap.

GitHub commits for logout UI stage:

- `3a9b3747de80b2475e0391fcd65a4564652bb81c` — frontend logout API.
- `1db474cfba6662bfa0aa8c5834456ce55647fafa` — logout mutation.
- `788c87201bbf823e4c9339cb45a3e30ed27dd8b9` — logout action in AppShell.
- `d065655b5c33500007c71e38e87571ae8d041f4f` — authentication documentation.

The user reported **All Passed** for local frontend typecheck, production build, and deployment on 2026-11-08. The next independent feature is administrator-assisted password recovery, implemented in the checkpoint below.

Administrator-assisted password recovery has now been implemented; see the checkpoint below. Do not repeat the implementation. The next step is local backend/frontend validation followed by browser verification of password reset and password copying.


## Administrator password reset checkpoint — 2026-11-08

- Local validation for the logout UI stage was reported as **All Passed**.
- Current backend code confirmed that account creation already uses `secrets.token_urlsafe(18)`, Argon2 hashing, and a one-time `temporary_password` response; the existing `SessionRepository.revoke_all_for_user(user_id)` is the session invalidation contract.
- Added administrator-only reset of an existing active, non-archived user through `POST /users/{user_id}/reset-password`.
- Reset generates a new temporary password, stores only its Argon2 hash, sets `must_change_password = true`, and revokes all target-user sessions in the same Unit of Work. The temporary plaintext is returned only once.
- Added Application and API tests for authorization, inactive/missing users, password state, session revocation, and client-safe response.
- Frontend adds a per-user **Сбросить пароль** action; the returned temporary password is shown in the existing one-time credential notice.
- The password-copy handler now tries the selected-text fallback first because the browser clipboard action was previously reported to copy an unexpected value. Local browser verification is required to confirm the copy behavior.
- No migration is required.


## Backend test-fixture correction — 2026-11-08

- User ran the backend suite after the administrator password-reset implementation: **283 passed, 11 failed**.
- The 10 authentication Application failures were caused by three test-only `FakeUserRepository` classes not implementing the current abstract `get_all_for_update()` repository contract. Added the method to those fakes; production repository code was not changed.
- The remaining order API test directly invoked `update_order()` without supplying its `read_service` dependency, so FastAPI's `Depends` marker was treated as the service object. Updated the test to pass a small fake read service, matching the direct-call pattern already used by the register-order test.
- These are test fixture corrections only. Local backend test/lint validation is pending.


## Backend validation and Alembic lint cleanup — 2026-11-08

- User reran the complete backend suite after the test-fixture corrections: **294 passed**.
- Ruff identified pre-existing lint violations in three Alembic migration files: unused imports, import ordering, collections.abc usage, and Union annotations.
- Updated only migration metadata/import formatting; migration revision identifiers, dependency graph, and upgrade/downgrade operations are unchanged.
- Commits:
  - `a1c4ea1908c28cf258f1258537bb278d4780dd14`
  - `322fd19243328fe9da97056ba77a142c56e9066b`
  - `e823dc9b3fc47603da6c9061388672701ebf97d8`
- Local `ruff check .` and `ruff format --check .` must be rerun after synchronizing these changes. Backend pytest is already green; do not repeat it unless a later change affects runtime behavior.


## Alembic lint follow-up — 2026-11-08

- The first Ruff cleanup pass did not fully resolve import-order findings and exposed additional legacy violations in two adjacent migrations.
- Normalized five migration files: `071a88b4b6da`, `4c9e2a7b1d60`, `4d7a9c2e1f30`, `7c2f1a9e4b60`, and `8a4d2f6b1c90`.
- Changes are limited to imports and equivalent type annotations (`tuple` for the migration `down_revision` sequence type); migration identifiers, dependency values, and upgrade/downgrade operations are unchanged.
- Commits: `0d69e77333efaf73acbdce68bb0de91b70488eec`, `445cc81be90f8fae6f3e314123d6a26c2c504b9c`, `c136b003a3db5c8ffdec109d0804ee9ab2e8b37f`, `913eece3392038fcfc379495fb93c27caaeea8e6`, `a105b0700397c2292cb1f2c7e717c05e98b38f51`.
- User's latest local run also reported 26 files not matching Ruff formatting. Do not mass-format unrelated files blindly; collect the exact file list and compare against the feature diff before deciding whether a separate repository-wide formatting cleanup is appropriate.
- Next local validation: `ruff check .`; then identify the 26 formatting paths with `ruff format --check .` output. Backend pytest already passed (294 tests).


## Ruff lint follow-up — 2026-11-08

- After the previous migration cleanup, the user's next `ruff check .` run exposed remaining style-only findings in adjacent Alembic migrations and the existing Device/Order API routers.
- Normalized import grouping/order, replaced legacy `typing.Union` annotations with `|`, and wrapped two overlong Device-router exception lines.
- No migration revision IDs, `down_revision` values, migration operations, API routes, request/response contracts, or runtime behavior were changed.
- Local `ruff check .` must be rerun after synchronizing these changes.
- The user's `ruff format --check .` still reports 24 files requiring formatting. Do not mass-format them without reviewing the exact file list and separating unrelated formatting debt from the current feature.


## Ruff cleanup continuation — 2026-11-08

- The next local `ruff check .` run reported 31 findings across Alembic migration metadata, existing Application services, API routers, ORM/domain imports, and tests.
- Corrected the two undefined annotation names left by the previous cleanup (`Union` / `Sequence`), normalized migration import groups and tuple metadata annotations, and addressed remaining import-order, unused-import, and line-length findings.
- User-administration service changes are formatting-only; last-active-administrator conditions and password-reset behavior are unchanged.
- Device/Order application, authentication services, Customer/Organization models, and tests received import/format-only edits; no business logic or API contracts changed.
- The branch contains 22 style-fix commits after `4b7cdbd465064ba4f8d8ecd9590d3f1d750e8642`. Local Ruff validation is still required; do not consider lint clean until `ruff check .` passes.
- Repository-wide `ruff format --check .` previously reported 24 files needing formatting. The exact file list is still needed before deciding whether those formatting changes are related to the current feature or constitute a separate cleanup.
- Backend pytest previously passed (294 tests); rerun it only if the final Ruff edits are found to affect runtime behavior.

## Ruff lint follow-up — 2026-11-08 (continued)

- The latest local run narrowed Ruff lint from 31 findings to 10: import ordering in seven Alembic migrations, two undefined `Union` annotations, and one overlong condition in the user-administration Application service.
- Corrected the Alembic import grouping, changed the remaining `Union` annotation to the equivalent `|` form, and wrapped the active-administrator condition.
- No migration revision/dependency metadata, migration operations, or business behavior changed.
- Local `ruff check .` must be rerun after pulling these commits.
- The latest format check lists 20 files requiring Ruff formatting. This remains separate from lint; inspect/format only after confirming the current lint result.

## Ruff import-grouping correction — 2026-11-08

- The user's follow-up lint run narrowed the remaining findings to seven `I001` import-grouping errors in Alembic migrations.
- Inspected the actual backend Ruff configuration: import sorting (`I`) is enabled. The migration directory's `alembic` module is classified separately from third-party SQLAlchemy imports, so the required ordering includes a blank line before `from alembic import op`.
- Applied that grouping to the affected migrations and removed the extra blank line before the revision metadata comment in the single-import migration.
- Migration revision IDs, dependency values, and operations are unchanged. A fresh local `ruff check .` is still required; no lint pass is claimed yet.


## Ruff import-order final correction — 2026-11-08

- The user's latest local `ruff check .` run narrowed the remaining findings to two `I001` errors in migrations `8d4f6a1b2c30` and `f3a8c1d9e720`.
- Read both current files from the feature branch and applied Ruff's exact ordering: standard-library imports, SQLAlchemy imports (including `sqlalchemy.dialects`), then a separate `alembic` import group.
- Only import ordering changed; migration identifiers, dependencies, and operations remain unchanged.
- Local `ruff check .` must be rerun after pulling the two fixes. Formatting remains a separate, not-yet-approved cleanup.


## Ruff migration import layout — 2026-11-08 (follow-up)

- The user's rerun still reported two `I001` findings in migrations `8d4f6a1b2c30` and `f3a8c1d9e720`.
- Re-read the exact current files and followed Ruff's diagnostic: removed the blank line between `from alembic import op` and the Alembic revision-identifiers comment. The import groups themselves remain ordered as Ruff specifies.
- Only whitespace/comment grouping changed; migration metadata and operations are untouched.
- Commits: `ccb571c3d8aded1b02ef37d80b8d2e558229da16`, `daa054698fd489e393ff9632ea25640743d37727`.
- Local `ruff check .` must be rerun. No clean result is claimed.


## Ruff Alembic comment-spacing correction — 2026-11-08

- The user's latest local Ruff output explicitly showed the required layout: one blank line after `from alembic import op` and before the Alembic revision-identifiers comment.
- Restored that blank line in migrations `8d4f6a1b2c30` and `f3a8c1d9e720`. This supersedes the immediately preceding checkpoint's statement that the blank line should be removed.
- Only whitespace changed; migration identifiers, dependencies, and operations are unchanged.
- Commits: `68529487eafec27e594a767c1e7da1a342923deb`, `2d6a30400d80f5c1357c2f668ac626e8d6d8cd49`.
- Local `ruff check .` must be rerun after pulling. No lint pass is claimed yet.


## Ruff validation checkpoint — 2026-11-08

- User confirmed the full backend `ruff check .` run passes with **All checks passed**.
- The subsequent `ruff format --check .` reports 15 files requiring formatting (507 files already formatted).
- Compared the reported paths against the feature branch diff from baseline commit `4b7cdbd465064ba4f8d8ecd9590d3f1d750e8642`. All 15 formatter findings are pre-existing formatting debt; none of the reported formatting hunks was introduced by the current user-administration/password-reset work.
- No repository-wide or unrelated formatting changes were made. The 15 files are deferred as a separate cleanup task.
- Ruff lint is locally validated clean. Ruff formatting check remains non-clean due to the 15 pre-existing files; this is explicitly not a regression from the current branch changes.
- Next: continue with frontend local typecheck/build, then deployment and browser verification of administrator password reset, especially exact password copying and forced first-login password change.


## Frontend validation checkpoint — 2026-11-08

- User ran frontend validation after synchronizing the current branch:
  - `npm run typecheck` — passed;
  - `npm run build` — passed.
- Vite production build transformed 1306 modules and completed successfully.
- Vite emitted the existing non-blocking warning that the main minified chunk exceeds 500 kB; no build or type errors occurred.
- Next: deploy the validated frontend with the existing production deployment script, then browser-verify administrator password reset and exact temporary-password copying.


## Password reset frontend deployment — 2026-11-08

- User synchronized the feature branch with `develop`; the fast-forward pull completed successfully.
- Production frontend deployment completed successfully through `frontend/scripts/deploy-production.sh`.
- Deployment output confirms frontend typecheck, production build, copy to `/var/www/sfera`, ownership correction, and directory/file permission correction all completed.
- Vite transformed 1306 modules. The only build warning is the existing non-blocking chunk-size warning (>500 kB).
- Browser validation by the user passed for the administrator password-reset interface:
  - reset action visibility for an active, non-archived target user;
  - confirmation prompt;
  - one-time temporary password display;
  - copying the exact displayed temporary password.
- Remaining browser validation: confirm the target user's previous session is invalidated, then authenticate with the temporary password, confirm redirect/gating to `/change-password`, set a new password, and verify normal access afterward. Use a non-critical test account, not `alex`.

## Password reset end-to-end validation — 2026-11-08

- User completed the remaining browser validation of the administrator password-reset flow; all checks passed.
- The target user's previously authenticated session became invalid after the administrator reset the password.
- Authentication with the one-time temporary password succeeded.
- The first-login gate required the user to open `/change-password` and set a new password.
- After changing the password, the user could access the application normally.
- Combined with the preceding deployment checkpoint, the complete password-reset flow is validated: reset action and confirmation, one-time password display and exact copying, session revocation, temporary-password login, mandatory password change, and normal post-change access.
- No additional code changes were required after browser validation.

## User session lifecycle security checkpoint — 2026-11-08

- User-administration audit found that deactivation and archive blocked existing sessions through account lookup, but did not revoke the persisted session records. Restoring/reactivating an account could therefore make an old session usable again.
- Deactivation and archive now revoke all sessions for the affected user in the same Unit of Work as the account-state update. Reactivation/restoration does not revive those sessions; the user must authenticate again.
- Authentication and current-user resolution now explicitly reject inactive users as well as missing or archived users, rather than relying solely on repository filtering.
- Added regression tests for session revocation on deactivation/archive and rejection of inactive accounts during authentication/current-user resolution.
- Local validation reported by the user: backend pytest **296 passed, 21 warnings**; `ruff check .` **All checks passed**.
- The scoped format check identified one touched test file. Applied Ruff's formatting-only changes to that file; no test behavior changed. Local `ruff format --check` for the six touched files must be rerun after synchronizing this final formatting commit.
- Implementation commits: `9f10cf6`, `f0c3200`, `f9a267d`, `81621b5`, `919b634`, `cceb197`; formatting commit: `66dd729`.

## Session revocation on account reactivation — 2026-11-08

- Follow-up audit identified a compatibility edge for accounts deactivated or archived before the session-revocation change: their historical session rows could still be unrevoked in the database.
- To prevent those legacy sessions from becoming valid again, activation and archive restoration now also revoke all sessions for the user. Session invalidation therefore occurs on both sides of the account availability transition: deactivate/archive and activate/restore.
- Added regression assertions for session revocation during activation and restoration.
- Commits: `af94232` (Application behavior), `b87b90d` (regression tests).
- Local backend pytest, Ruff lint, and scoped format validation are pending for these follow-up changes.

## Follow-up validation and auth-guard audit — 2026-11-08

- User local validation after the account reactivation/restoration session-revocation changes: backend pytest **296 passed, 21 warnings**; `ruff check .` passed; scoped `ruff format --check` passed for both changed files.
- The 21 warnings are existing dependency/deprecation warnings: Starlette `httpx` TestClient deprecation and `datetime.utcnow()` deprecations in price-list tests/domain code; no failures.
- Reviewed `backend/app/main.py`: `require_password_change_completed` is applied as a router-level dependency to all business and user-administration routers. The auth router remains outside that guard so login, `/auth/me`, password change, and logout remain available. This confirms first-login password enforcement is server-side, not only frontend navigation.
- Reviewed user lifecycle/domain, API router, repository, auth/current-user, session repository, and password-change service paths. Active/inactive and archived account checks are enforced in authentication/current-user resolution; all user administration mutations require the administrator application-service role check and CSRF protection at API level.
- Current audit finding closed: session revocation is performed on deactivate, activate, archive, restore, and password reset. No further change made in this pass.

## User administration frontend review — 2026-11-08

- Reviewed the current user administration API client, mutation hooks, `UsersPage`, authentication provider/route guard, and password-change page on `feat/user-first-login-password`.
- Confirmed the UI prevents role changes to archived accounts, disables actions that would remove the last active administrator, confirms archive/password-reset actions, and displays the one-time temporary password with the corrected exact-value copy implementation.
- Frontend route guard redirects users with `must_change_password` to `/change-password`; backend router-level guard independently enforces the same restriction.
- No additional frontend code changes were warranted in this audit pass.

## Customer edit validation checkpoint — 2026-11-09

- Implemented and validated the Customer edit flow on `feat/user-first-login-password`.
- Backend update handling distinguishes omitted fields from explicit `None`, so optional customer fields can be cleared without conflating them with an omitted update. Customer name and discount remain non-clearable by application rules.
- Frontend Customer edit support was added using the existing customer form/update API path; no Organization or Site behavior was changed in this stage.
- Local validation by the user:
  - backend `pytest -q`: **296 passed, 21 warnings**;
  - backend `ruff check .`: **All checks passed**;
  - scoped `ruff format --check`: **3 files already formatted**;
  - frontend `npm run typecheck`: passed;
  - frontend `npm run build`: passed; Vite transformed 1306 modules and emitted only the existing non-blocking main-chunk size warning.
- No local validation failures remain for this stage. The npm notice about a newer npm major version is informational and unrelated to the build result.


## Order instrument search by Customer Site — 2026-11-09

- Inspected the actual order creation and order-item UI, device API/domain/repository contracts, Site API, and the Customer / Organization / Site model document on the feature branch.
- Added a multi-select Site filter to the order-item `DeviceSelector`. The device list remains restricted to the order's Customer and any selected Instrument Type.
- Added an independent option to include/exclude Customer instruments whose `site_id` is null. With no selected Site, all Customer Sites remain in scope.
- Changing the selected Sites affects only the search result; it does not update `Instrument.site_id` or otherwise change permanent ownership/assignment.
- If a selected instrument becomes hidden by a changed filter, the selection is cleared to prevent adding an invisible instrument. Filter state resets when the order Customer changes.
- Site lookup failure is non-blocking: the Site filter reports its error while the device list remains usable.
- Organization selection was intentionally not added: the current Order domain/ORM/API/read contract has no Organization context field. The business model document requires cardinality and persistence to be decided before adding that selection.
- Implementation commits: `70bf39a` (Site filter), `cead4ee` (reset filter on Customer change and clarify Site-load error), and `00c4fb4` (explicit all-Sites placeholder and typed MUI Select).
- Local frontend validation is pending. Do not treat this slice as completed until the user reports `npm run typecheck` and `npm run build`.

## Order instrument search by Customer Site — local validation complete — 2026-11-09

- User ran frontend validation after the Site-filter implementation:
  - `npm run typecheck`: passed (`tsc --noEmit`);
  - `npm run build`: passed (`tsc -b && vite build`);
  - Vite transformed 1306 modules and completed the production build successfully.
- No TypeScript or build errors were reported. The Site-filter frontend slice is complete.
- No backend validation was repeated because this slice changed only the frontend.

## Next stage — Order / Organization context contract

- Begin with a read-only audit of the actual Order domain, persistence model, repository/mapper, Application use cases, API schemas/read model, and frontend create/edit flows.
- The business decision already recorded in `docs/architecture/CUSTOMER_ORGANIZATION_SITE_MODEL.md` is that Organization is selected in the context of an Order and is not a permanent Customer–Organization relation.
- Still unresolved: whether one Order may have exactly one Organization or multiple Organizations, when selection becomes required, and whether the selection is mutable after registration / document issuance.
- Do not add UI-only state or an Organization dropdown until the persistence and lifecycle contract is agreed.
- Propose the smallest set of business decisions after inspecting the current code; do not change the normative architecture or introduce a speculative model.


## Production synchronization checkpoint — 2026-11-09

- PR #18 (`feat/user-first-login-password`) was merged into `develop`; merge commit: `4e0ebc684e3a542a3a13f2d060e4c2609a8de873`.
- User synchronized the local `develop` checkout with `origin/develop`; the working tree was confirmed clean after removing eight empty untracked files.
- Database Alembic revision and the sole repository head both report `c2e5f7a9b310`; no migration upgrade was required.
- Local backend validation: `pytest -q` — **297 passed, 21 warnings**; `ruff check .` — passed.
- `ruff format --check .` reports 14 files requiring formatting (508 already formatted). This includes pre-existing/unrelated formatting debt; no mass-formatting was performed.
- Local frontend `npm run typecheck` — passed.
- Production backend restart completed; `sfera-backend.service` reported `active (running)`.
- `frontend/scripts/deploy-production.sh` completed successfully, including the production Vite build and publication to `/var/www/sfera`. Vite emitted only the non-blocking main-chunk warning (>500 kB).
- Local Nginx smoke checks returned HTTP 200 for the frontend and API health endpoint; API health response: `{"status":"ok"}`.
- DNS-based access by hostname was not required for these local server checks.
- Current synchronized branch: `develop`. Next work should begin by re-reading the current code and selecting the next independent business scenario; the previously recorded Order / Organization context contract remains unresolved and must be audited before implementation.


## Order item editing after registration — implementation checkpoint — 2026-11-09

- Business behavior: an order remains editable after registration until production work has started. Registration alone must not prevent correcting the order or filling reserved empty OrderItems.
- Domain now permits adding, updating, assigning an Instrument to, and removing OrderItems while Order status is `NEW` or `REGISTERED`.
- These mutations remain blocked for `IN_WORK`, `WAITING`, `COMPLETED`, `ISSUED`, `CLOSED`, and `CANCELLED`. The error now describes the production-work boundary rather than calling every non-NEW order active.
- Frontend exposes OrderItem editing and adding positions for both `NEW` and `REGISTERED`.
- This is an intentionally conservative first slice: the current Order lifecycle audit says the Order transitions beyond `REGISTERED` are not implemented. Per-OrderItem editability based on actual WorkflowInstance / Verification / Repair / Diagnostic activity remains a separate follow-up; do not infer that a whole-order status is a reliable per-item production state.
- Added domain and application regression tests for registered-order item changes and protection after work starts.
- Branch: `fix/order-edit-after-registration`. Local backend/frontend validation and PR creation are pending.


## OrderItem instrument assignment and missing-instrument creation — implementation checkpoint — 2026-11-09

- Started from the merged `develop` state after PR #19 (merge commit `2ff130278ce4b6e54a82e6cbdab2594283e54b5f`).
- The existing OrderItem UI already supported selecting an existing Customer instrument for a reserved empty position, but did not offer creation from that assignment flow.
- Updated the shared DeviceSelector to show each existing instrument's current Site (or "Без площадки") in search results.
- Exact serial-number matches are detected across all instruments belonging to the Customer, independently of the active Site and Instrument Type filters. The selector reports the existing card and its current Site and suppresses the create action, preventing an obvious duplicate from being created through this flow.
- When no exact serial-number match exists, the assignment flow offers creation of a minimal Instrument card. On successful creation, the new card is immediately assigned to the reserved OrderItem.
- The new card is created without a Site assignment; this does not alter any existing instrument's Site. Existing instrument Site assignments remain untouched by selection.
- Backend uniqueness constraints for serial numbers were not found in the current Instrument ORM model; this UI guard is scoped to the Customer's currently loaded instrument list and is not a database-level uniqueness guarantee.
- Frontend local validation is pending. Do not deploy until typecheck, build, and browser validation pass.


## Duplicate instrument selection in an Order — correction in progress — 2026-11-09

- User browser validation found two issues: the obsolete "Включать СИ без площадки" checkbox remained, and duplicate instrument cards already present in the Customer database could be selected and added as visually identical OrderItems.
- Removed the standalone checkbox. Instruments without a Site are now included automatically, including when a Site filter is active; the filter only narrows instruments that have a Site.
- The order selector now receives IDs of instruments already assigned to sibling OrderItems and excludes those instruments and all cards sharing their serial number.
- The selector also suppresses serial numbers that occur on multiple Customer cards. Typing such a serial reports that the database contains ambiguous duplicate cards and blocks selection/creation rather than choosing an arbitrary card.
- Added an Application-level guard for both adding an instrument to an Order and assigning one to a reserved OrderItem. It compares normalized serial numbers against instruments already on that Order, so separate database cards with the same serial cannot create duplicate-looking positions.
- Added regression tests for duplicate serials with different Instrument IDs in both add and assign flows. Backend and frontend local validation are pending; do not merge or deploy until they pass and the UI is checked again.

## Create Instrument from the main menu and global scroll-to-top — 2026-11-09

- Added a dedicated `/devices/new` route and a **«Создать СИ»** action on the global Instruments list.
- The creation page uses the existing DeviceForm and create-device mutation. It first requires selecting an active Customer because the current create API contract requires `customerId`; the Site remains optional and is loaded for the selected Customer.
- On successful creation, the user is redirected to the new Instrument card. The existing Customer-scoped creation route remains unchanged.
- Added a shared floating **«Наверх»** control in AppShell. It appears after scrolling more than 400 px and scrolls smoothly to the top; it is shared by all authenticated pages rather than copied into each page.
- Initial local validation found that `@mui/icons-material/KeyboardArrowUp` is unavailable because `@mui/icons-material` is not a frontend dependency. Replaced the icon with a text arrow inside the existing MUI Fab; no dependency was added.
- Local validation by the user completed successfully: frontend `npm run typecheck` and `npm run build` both passed; Vite transformed 1309 modules and produced the production bundle.
- Browser verification by the user passed: creation from the global Instruments list, creation without assigning a Site, redirect to the newly created Instrument card, appearance of the floating «Наверх» control on scroll, and smooth return to the page top.
- This frontend slice is locally and functionally validated. No production deployment is implied by this checkpoint.
- PR #21 was squash-merged into `develop`: `82018c893dca1499b488209e37b3bcdede2c69a5`.
- Local branch synchronization and production deployment remain separate operational steps; no production deployment is recorded here.

## OrderItem instrument assignment — local validation checkpoint — 2026-11-09

- User synchronized the feature branch through commit `2f6d866`.
- Backend local validation: `pytest -q tests/api/routers/test_order.py tests/application/order/test_order_application.py` — **20 passed**.
- `ruff check app/api/routers/order.py tests/api/routers/test_order.py` — passed.
- The initial scoped `ruff format --check` found formatting-only issues in `backend/tests/api/routers/test_order.py`. Corrected indentation and spacing in commit `7e71e9b`; no behavior changed. The user must rerun the scoped format check after pulling this commit.
- Frontend local validation: `npm run typecheck` and `npm run build` — passed. Vite emitted its non-blocking warning for a minified chunk larger than 500 kB.
- Added API regression coverage ensuring that assigning an Instrument belonging to another Customer maps `InstrumentCustomerMismatchApplicationError` to HTTP 409 rather than an unhandled server error.
- PR #20 remains open. Browser validation of the updated OrderItem assignment/search behavior and final PR checks are still required. Do not deploy as part of this stage.


## OrderItem instrument search — strict Site scope and fallback — 2026-11-09

- User confirmed the intended search rule: when one or more Sites are selected, the normal selector result must contain only instruments assigned to those selected Sites. Instruments without a Site and instruments assigned to other Sites must not be mixed into the normal result.
- If the current Site-scoped search has no matching instrument, the selector displays an informational prompt and an explicit **«Искать везде»** action. This expands the result to the Customer's instruments on other Sites and without a Site; each result continues to show its current Site.
- Creation is kept unavailable while that fallback action is still offered. After expanding the search, if no exact serial-number match exists anywhere in the Customer's cards, creation of a new Instrument card becomes available. Existing exact-match, ambiguous-serial, and already-in-order protections remain in force.
- The expanded search is temporary UI state; it does not change any Instrument's Site assignment. Changing the selected Sites returns the selector to strict Site scope; changing Customer resets the search state.
- Implementation commit: `27f8bc4`.
- Local frontend typecheck, build, and browser validation are pending. Do not merge or deploy PR #20 until the user verifies strict Site filtering, the explicit expanded-search fallback, duplicate handling, and creation behavior.


## OrderItem — создание СИ с неизвестным заводским номером — 2026-11-09

- После успешной проверки сохранения неизвестного номера пользователь предложил упорядочить блок добавления позиции и убрать растягивание на всю ширину страницы.
- Ограничена максимальная ширина блока до 760 px; группа СИ и количество остаются в компактной верхней строке с переносом; селектор занимает ширину блока; действие «Добавить позицию» перенесено на отдельную строку и визуально выделено как основное (contained), без растягивания на всю ширину.
- Коммит компоновки: `0cec3e9`. Локальные typecheck/build и браузерная проверка новой компоновки ожидаются.


- Follow-up browser validation exposed a second defect in the same flow: MUI Autocomplete cleared the typed serial on blur, which made the create action become disabled; its long empty-result message also obscured the action below the field.
- Fixed input-state handling to update only on actual typing/clear events, set `clearOnBlur={false}`, and shortened the popup empty-result text. The typed serial now remains available when focus moves to the create action.
- Follow-up implementation commit: `4dffdad`.
- Local typecheck/build and browser re-validation of unknown-serial creation are pending. Do not merge or deploy until the user confirms the field retains its value on blur and the create action opens the form with that serial prefilled.

- Browser validation exposed a UX defect: entering an unknown serial in the OrderItem Autocomplete produced “No options”, while the creation path and its disabled state were not explained clearly.
- The selector now provides explicit loading/empty-result text and explains why creating a card is unavailable (loading, empty input, existing serial, or required Site-search expansion). The action is labeled “Создать карточку СИ”.
- The selected Instrument Type is now passed into DeviceSelector so existing-serial matching can report a type mismatch accurately.
- Existing duplicate protection and the confirmed strict Site-search/fallback behavior are retained; this change does not alter backend contracts or Site assignments.
- Implementation commits: `c3f8267`, `5eb35e8` on `fix/order-item-unknown-device-creation`.
- Local typecheck, build, and browser validation are pending. Do not merge or deploy until those checks pass.


## OrderItem — расположение операций под селектором СИ — 2026-11-09

- Чекбоксы «Поверка», «Диагностика», «Ремонт», «Продажа» перенесены непосредственно под селектор «Средство измерений» и кнопку создания карточки СИ внутри селектора.
- Благодаря порядку элементов пустое состояние Autocomplete («СИ не найдено») больше не должно перекрывать кнопку создания; выбор операций и обработчики не менялись.
- Кнопка «Добавить позицию» остаётся ниже чекбоксов.
- Изменение интерфейса: локальные typecheck/build и браузерная проверка после синхронизации ветки ожидаются.


## OrderItem — create action visibility correction — 2026-11-09

- Production browser validation after PR #22 showed that the «Создать карточку СИ» action was still covered by the open MUI Autocomplete no-options popup. The earlier checkbox relocation did not resolve this overlay.
- In `DeviceSelector`, moved the create action and its disabled-reason text above the Autocomplete input. The popup opens below the input, so it cannot cover the action. The operation checkboxes remain directly below the complete DeviceSelector; the «Добавить позицию» action remains below the checkboxes.
- No search, duplicate-detection, Site-filter, creation, or order-item mutation behavior was changed.
- Branch: `fix/order-item-create-button-visibility`.
- Local typecheck/build and production browser validation are pending.


## Verification — archived state mapper correction — 2026-11-14

- Audited current Verification implementation on `develop` (`eb887867`) and local usage of `methodology`, `VerificationMethod`, and `archived`.
- Confirmed that the historical migration explicitly converted `verifications.methodology_id` into a nullable text `methodology` field and removed the FK. The current string contract is therefore an intentional migration outcome; do not restore the FK without a separate business decision.
- Confirmed a persistence defect: `VerificationMapper` did not map the inherited `archived` field in either direction, although Domain, ORM, API DTO, and frontend all expose/use it.
- Branch `fix/verification-archived-mapping`: mapper now copies `archived` in both directions; mapper tests cover ORM→Domain and Domain→ORM preservation.
- GitHub commits: `72a845b` (mapper fix), `839c538` (regression tests).
- Local backend test/ruff validation is pending. Do not merge or deploy until the user reports the scoped checks.


## Verification — action response contract — 2026-11-14

- Local validation of the archived-state mapper correction passed: 4 mapper tests, Ruff checks, and format check.
- Added explicit `response_model=VerificationRead` to the approve and reject API routes. The start route already declared this response model; the frontend consumes the same Verification DTO for all lifecycle actions.
- Commit: `d84c934` on `fix/verification-archived-mapping`.
- Local API validation is pending. Do not merge or deploy until the user reports the scoped checks.


## Verification — unsuitable reason invariant — 2026-11-14

- Local validation of the API response-model correction passed: 7 API router tests; Ruff and formatting checks passed. One existing Starlette/httpx deprecation warning remains.
- Domain validation in `Verification.mark_unsuitable` now rejects whitespace-only reasons using `reason.strip()`; accepted reason text is otherwise preserved.
- Added parameterized domain coverage for empty, space-only, and tab/newline-only reasons.
- Commits: `77e849c` (domain invariant), `5f848b0` (tests), `f106a8f` (control-character test case).
- Local domain validation is pending. Do not merge or deploy until the user reports the scoped checks.


## Verification — implementation slice locally validated — 2026-11-14

- Final branch audit against `develop` found exactly six changed files: Verification mapper, mapper tests, Verification action router, Verification Domain entity, Domain tests, and this context document. No unrelated files or database migrations are included.
- Branch `fix/verification-archived-mapping` is 9 commits ahead of `develop` and 0 commits behind it at the time of audit.
- User local validation passed after synchronizing through commit `4d1aa0a`: `tests/domains/verification/test_verification.py` — 12 passed; scoped Ruff check — passed; scoped Ruff format check — passed.
- Earlier scoped local validations also passed: Verification mapper tests — 4 passed; Verification API/router tests — 7 passed (one existing Starlette/httpx deprecation warning); Ruff and format checks passed in both stages.
- The three implementation corrections are complete: archived-state mapping in both directions, consistent `VerificationRead` response models for approve/reject, and rejection of whitespace-only unsuitable reasons.
- Before PR creation, run the combined Verification test scope (Domain, Application, API/router, and Infrastructure mapper tests) on the latest branch HEAD. Do not merge or deploy as part of this checkpoint.


## Verification — PR #26 merged and local validation — 2026-11-14

- PR #26 (`fix: correct Verification persistence and action contracts`) was squash-merged into `develop`; merge commit: `afd8f16f702d28212698139581dbd88c619dc117`.
- User synchronized the local `develop` branch with `origin/develop` using Fast-forward; the merge commit's six-file change set was received.
- Post-merge local backend validation on `develop` passed:
  `pytest -q tests/domains/verification tests/application/verification tests/api/routers/test_verification.py tests/api/routers/test_verification_actions_auth.py tests/infrastructure/mappers/test_verification_mapper.py` — **39 passed, 1 warning**.
- The only warning is the existing Starlette deprecation warning for using `httpx` with `starlette.testclient`; it does not cause test failures.
- PR-head Backend CI completed successfully before merge. No CI status was reported for the squash merge commit itself.
- No production deployment or backend restart was performed for this slice.
- Verification persistence/action-contract corrections are merged and locally validated on `develop`.


## Metrology — verification history and external source — 2026-11-14

- User confirmed that the Instrument card must show the latest known verification even when it was performed by an external laboratory and obtained from FGIS Arshin; it must not be limited to verifications performed in Sfera.
- The card's verification summary should identify the record's origin. At minimum, distinguish a verification performed/recorded in Sfera from an externally performed verification imported or recorded from an external source (for example, FGIS Arshin).
- Keep the verification date, result, and validity end date on the individual verification/history record. The Instrument card displays a derived summary from the latest applicable known record; do not duplicate editable verification dates on the Instrument entity.
- Preserve provenance on the record so users can tell who/what system supplied the information. Exact source model, import mechanism, and reconciliation rules require a separate audit of the current Arshin integration and existing Verification read contracts before implementation.
- Current Verification Domain already has `verification_date`, `valid_until`, `result`, `instrument_id`, and free-text `methodology`. Current methodology input remains free text for initial rollout; a structured Method/MethodVersion registry, managed document files, Device/Instrument applicability, and immutable revision linkage are future scope. Do not restore a methodology FK based on the historical migration without a separate design decision.
- No code or database changes are authorized by this checkpoint; this records the agreed business direction for a later implementation stage.


## Verification UI presentation checkpoint

- The verification detail page now presents the existing Verification read contract in Russian, grouped into main details, result/validity, execution history, and lifecycle actions.
- Lifecycle and result values use human-readable labels and status chips; archived records are visibly marked.
- Start/approve/reject controls use Russian labels; rejection requires a non-whitespace reason in the UI.
- No backend contract, persistence model, Arshin integration, or business lifecycle rules were changed.
- This is the first UI presentation stage only. Full browser scenario validation and final display debugging remain pending local validation.


## 2026-11-14 — Verification UI PR #27 merged

- Verification UI presentation branch `feat/verification-ui-presentation` merged into `develop` via squash.
- PR: https://github.com/iboamebi/sfera/pull/27
- Merge commit: `510aea4361fbeb7329c6312e39835f2bb99da313`.
- PR head: `3657b4b3146e92164e5feac7d3a6240adcd10dd4`; GitHub Backend CI run #1056 completed successfully.
- User local frontend validation on the feature branch: `npm run typecheck` passed; `npm run build` passed (Vite transformed 1307 modules).
- No backend, database, Arshin integration, or production deployment changes were made as part of the merge.
- Next: synchronize local `develop`, repeat frontend validation on the merged commit, then deploy frontend to production as requested and verify the Verification page in the browser.


## Verification UI — production appearance review — 2026-11-14

- Local `develop` was synchronized with `origin/develop`; working tree was clean. Merged frontend passed `npm run typecheck` and `npm run build`.
- User deployed the frontend with `frontend/scripts/deploy-production.sh`; script completed with `Production frontend deployed successfully`. Vite emitted a non-blocking chunk-size warning (main JS bundle approximately 854 KB).
- No backend restart, backend deployment, database migration, or Arshin integration was performed.
- Browser appearance review is now pending. Navigation: open `/orders`, open an order, then select the `Поверка N` link under an order item that already has a verification.
- Current Verification page still displays the raw `orderItemId` UUID as «Позиция заказа». The Order read model provides item details and verification IDs, but the Verification read DTO currently only provides `order_item_id`; review whether this should be replaced by contextual navigation or a richer read contract in a separate minimal change after visual feedback.
- Next sequence remains: visual appearance review → full lifecycle scenario → final display debugging. Use only current Sfera data/API; no Arshin assumptions.


## Verification UI — compact layout refinement

- Following production appearance review, the Verification detail page was tightened without changing API or domain contracts.
- Main details, result/validity, execution history, and lifecycle actions now use a responsive two-column layout on wider screens and a single column on narrow screens.
- Detail fields are arranged horizontally and wrap as needed; card padding and section spacing were reduced.
- Removed the raw `order_item_id` UUID from the user-facing page. The current Verification DTO does not expose an order ID or instrument details. Although the Order DTO contains item names and Verification IDs, resolving an order item from the verification page would require loading/searching the order collection; this is intentionally not added as an implicit expensive lookup. Contextual navigation requires a deliberate read-contract decision.
- No backend, database, lifecycle, or Arshin changes.
- Next: local frontend typecheck/build, then production visual recheck; only after appearance is accepted proceed to full lifecycle scenario testing.


## Verification UI — compact layout merged (PR #28)

- PR #28 `ui: compact Verification detail layout` merged into `develop` by squash.
- Merge commit: `c1cb0dab9190c04751b2488e85c3ed8099666a00`.
- Frontend page now uses responsive two-column layout on wide screens and one column on narrow screens; card padding/spacing reduced; detail fields wrap.
- Raw `order_item_id` UUID removed from the user-facing Verification page. Current Verification read DTO does not expose Order/Instrument context; contextual navigation remains a separate read-contract decision.
- User local validation on PR head `1b14d2c`: `npm run typecheck` passed; `npm run build` passed (Vite emitted existing >500 kB chunk advisory).
- Backend CI #1062 succeeded on PR head `1b14d2c`; no review comments or threads.
- No backend, database, lifecycle, or Arshin changes. Production has not yet received this compact-layout refinement.
- Next: synchronize local `develop`, validate merged frontend, deploy frontend only, then inspect appearance in production before starting full Verification lifecycle scenario.


## Verification UI — instrument context

- Production scenario feedback: Verification creation and transition to `IN_PROGRESS` work, but the detail page lacked the measuring instrument identity and attributes.
- The backend `VerificationRead` schema already includes nullable `instrument_id`; the frontend DTO/model/mapper had omitted it. No backend contract or database change is required.
- The Verification page now uses the existing Device detail query for the linked instrument and the existing InstrumentType detail query for its type name. It displays instrument name, type, serial number, registry number, modification, manufacture year, and inventory number, with separate loading/error handling for the related reads.
- The raw order-item UUID remains hidden. No order lookup, Arshin integration, lifecycle change, or persistence change was introduced.
- Branch: `feat/verification-instrument-context`. Local typecheck/build and browser validation are pending.


- User local validation completed on branch head `a7cb2adb`: `npm run typecheck` passed and `npm run build` passed (1307 modules; existing >500 kB bundle advisory not emitted in this build).
- GitHub Backend CI run #1065 completed successfully. PR review submissions and inline review threads are empty.
- PR #29 is ready for merge; production browser validation remains pending and must happen after merge/deployment.


## Verification — validity duration and correction

- Approval now accepts either a manually entered `valid_until` date or a duration in calendar years plus the operator's IANA timezone. When duration is used, the application captures one UTC `decision_at`, converts it to the supplied timezone, adds the requested number of calendar years, then subtracts one day.
- A February 29 anniversary that falls in a non-leap year is clamped to February 28 before subtracting one day.
- The frontend displays a preview based on the operator's current local date, but the backend remains authoritative and calculates from the actual persisted decision timestamp. An optional manually entered final date overrides the calculation.
- A separate correction operation is available only for a non-archived Verification with a DECIDED/SUITABLE result and an existing validity date. It requires a non-blank reason and writes an append-only `verification.valid_until_corrected` audit record with old/new dates and the reason.
- Approval and correction remain restricted to METROLOGIST and ADMIN and require authenticated, CSRF-protected API routes.
- Branch: `feat/verification-validity-correction`. Backend domain/application/API tests and frontend typecheck/build are pending local validation. Do not merge or deploy before those checks and user confirmation.


## Verification Decision Correction Checkpoint — 2026-11-14

A new backend use case is being implemented on branch `feat/verification-decision-correction`.

Business rule confirmed:
- A decided Verification may have its result corrected in either direction: SUITABLE ↔ UNSUITABLE.
- Every correction requires a non-blank correction reason.
- A corrected SUITABLE decision requires `valid_until` and clears `unsuitable_reason`.
- A corrected UNSUITABLE decision requires a non-blank `unsuitable_reason`, clears `valid_until`, and retains the correction reason separately.
- `decision_at` is updated to the correction timestamp.
- Each correction appends an immutable AuditRecord with old/new result, validity date, unsuitable reason and decision timestamp; the correction reason is stored as AuditRecord.reason.
- Only METROLOGIST / ADMIN may execute the use case, enforced in Application.

Current implementation files:
- Domain: `backend/app/domains/verification/entities/verification.py`, `backend/app/domains/verification/exceptions/__init__.py`.
- Application: `backend/app/application/verification/commands/correct_verification_decision.py`, `backend/app/application/verification/services/verification_application_service.py`.
- API: `backend/app/api/routers/verification_actions.py`, `backend/app/schemas/verification.py`.
- Tests: domain, application audit/authorization and API auth/CSRF tests.
- Authorization contract updated in `docs/architecture/AUTHORIZATION.md`.

No database migration is expected: Verification persistence already stores result, valid_until, unsuitable_reason and decision_at; audit uses the existing append-only audit tables.

The separate PR #31 (instrument-name link to Device card) remains open and has not been merged; do not merge without explicit user authorization. Its browser validation was confirmed by the user, although the PR body still needs its validation note refreshed.

Next: complete backend tests/CI, then implement the correction form in the Verification page after the branch coordination with PR #31 is resolved. Order operation-state read model and presentation remain a separate subsequent stage.


## Order — multiple verifications and per-position status — 2026-11-14

- Current backend already permits multiple Verification records for one OrderItem; the previous single-verification limitation was only in the OrderItems frontend condition that hid «Создать поверку» after the first record.
- Order read contract previously exposed only `verification_ids`. It now includes a per-item `verifications` summary: ID, creation timestamp, verification date/type, lifecycle status, result, validity end date, and archived flag. Existing IDs are retained for compatibility.
- Verification summaries are sorted by `created_at` and ID. The UI assigns one sequential number across all positions in an order, avoiding repeated «Поверка 1» labels for different positions.
- Each record is displayed with its lifecycle/result state and validity date where available. Creating another Verification remains possible whenever the position requests verification and has an assigned Instrument.
- Order already has `planned_issue_at`; the existing «Планируемая выдача» field remains the source of the estimated pickup date. This slice does not infer an ETA from verification durations or add scheduling logic.
- Do not label an entire instrument/order as ready solely from one Verification if other requested operations (repair/diagnostics) are not represented in this read model. A latest unsuitable or unfinished Verification must not be masked by an older suitable record.
- Branch: `feat/order-verification-status-summary`. Backend/frontend local validation is pending. No merge, production deployment, backend restart, or database migration has been performed.

## Verification decision correction backend consolidated on develop — 2026-11-14

- Enforced the one-way correction rule in the Verification Domain: `UNSUITABLE → SUITABLE` is rejected; a positive result requires a new Verification.
- Added Domain and Application regression tests proving the prohibited correction does not mutate the Verification or append audit records.
- Corrected the verification-start audit test expectation: one AuditOperation groups two AuditRecords (verification.started and order.started_work).
- No database migration. Frontend correction UI is the next integration stage; no production deployment or backend restart.


## Verification decision correction UI consolidated on develop — 2026-11-14

- Added the typed frontend API client and React Query mutation for audited decision correction.
- Exposed the correction form only for non-archived, decided verifications; the UI permits `SUITABLE → UNSUITABLE` and directs users to create a new Verification for a positive result after an unsuitable decision.
- The correction form requires an unsuitable reason and a separate correction reason, and refreshes the Verification detail after success.
- Preserved the current `develop` Verification page and validity-correction behavior; validity form now resets its date when server data changes and disables unchanged submissions.
- Backend one-way enforcement and regression tests are already on `develop` (`43dae81`). No migration, deployment, or backend restart.

## Order — multiple verifications and per-position status locally validated — 2026-11-14

- Local `develop` is synchronized with `origin/develop` at `1aa21e0`; working tree is clean.
- Backend mapper regression test passed: `1 passed`. Scoped Ruff check passed; all five scoped files are formatted.
- Frontend `npm run typecheck` passed. `npm run build` passed (1313 modules); Vite reports the existing advisory that a minified chunk exceeds 500 kB.
- Rechecked the implementation files from PR #36 against `develop`: all five backend and all four frontend implementation files are identical. Only `docs/AI_CONTEXT.md` differs; the feature branch checkpoint is older. No code needs to be transferred from PR #36, and the PR is left open pending a separate cleanup decision.
- No production deployment, backend restart, database migration, or PR merge was performed.
- Next: browser scenario review of an order with multiple positions and multiple verifications per position. Confirm global numbering, per-verification lifecycle/result/validity display, ability to create another verification, and that an older suitable result does not mask a newer unsuitable or unfinished result. Verify the order's planned issue date remains the displayed estimate; do not infer readiness from verification alone when other requested operations are outside the read model.

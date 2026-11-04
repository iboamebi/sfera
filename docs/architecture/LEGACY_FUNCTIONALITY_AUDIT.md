# Legacy Functionality Audit

## Purpose and method

This is a fact-based comparison of legacy business behavior with the current DDD/Clean Architecture implementation. It is not a plan to restore generic CRUD.

For each module inspect legacy routes, schemas, CRUD/service callers and frontend; then compare current Domain, Application, repository ports, Infrastructure, API, frontend, tests and migrations.

Classifications:
- **Migrated** — behavior exists in the current architecture.
- **Replaced** — a domain-specific use case replaces the old mechanism.
- **Missing (confirmed)** — an exposed or required business scenario has no current equivalent.
- **Potential gap** — evidence is incomplete.
- **Temporary stub/simplification** — placeholder, hardcoded, in-memory, no-op or incomplete behavior remains.
- **Not established as business behavior** — a generic helper exists without evidence of a business-facing workflow.

Never infer business requirements from generic CRUD methods alone.

## Checkpoint 1

- Branch: `feat/user-first-login-password`
- Starting HEAD: `e3fe4a66c7788c574bfa242d97fb134aac22509e`
- Legacy CRUD removal: `8be14a2680f5481378d0aa1f6038fbf60445d320`
- Parent revision: `1dd08fc3d21098b241b3bbf74b30886dbb2f6771`

### Generic CRUD removal

Commit `8be14a2` removed `backend/app/crud/base.py` and module-specific wrappers. The base class supplied generic `get`, `get_all`, `create`, `update`, and `archive`.

This proves that generic persistence helpers existed. It does not prove that every operation was exposed in API/UI or represented a business process. Actual routes and callers must be checked per module.

### Repair — preliminary comparison

Legacy and current routers/schemas were read.

- Both versions expose get-by-id, create, start, complete and cancel.
- Current implementation additionally forwards the authenticated user and enforces the technician/admin role.
- Current Application service records an audit entry on completion.
- Neither inspected router exposes a collection/list endpoint.
- Generic `get_all` and `archive` are not evidence that repair list/archive were business workflows.

**Status:** lifecycle behavior migrated and extended. List/archive remain unproven potential gaps, not confirmed losses.

### Diagnostic — preliminary comparison

Legacy and current routers/schemas were read.

- Both versions expose get-by-id, create, conclusion handling and recommendation handling (the conclusion action has a more explicit completion name in the current API).
- Current implementation adds authenticated user forwarding and role checks.
- Current Application service records an audit entry on conclusion completion.
- Neither inspected router exposes a collection/list endpoint.
- Generic `get_all` and `archive` do not prove diagnostic list/archive workflows existed.

**Status:** core inspected behavior migrated/refined. List/archive remain unproven potential gaps.

### Customer / Organization / Order — confirmed mismatch

Current code inspection established:
- Customer still has a required single `organization_id` through the domain/application/persistence flow.
- `CustomerOrganization` association persistence exists but is not yet the primary 0..N relationship in customer application/API/frontend flows.
- Order creation copies `customer.organization_id` into `Order.organization_id`.
- This conflicts with the approved business model: an Order belongs to a Customer; payer Organization is selected when invoicing.
- Preserve historical references until migration and data dependencies are inspected.
- Invoice implementation is outside this audit's scope unless separately designed and approved.

**Status:** incomplete migration confirmed. This is the first planned implementation slice after the audit of dependencies and migration constraints.

### Device

Current Instrument ORM, mapper and Device repository persist `device_status`.

**Status:** status persistence is migrated; do not classify the historical in-memory version as a current stub.

## Open work

Continue source comparison for:
- Customer / Organization / Order, including legacy frontend usage and migration/data dependencies.
- Verification: complete legacy workflow versus current lifecycle/methodology model.
- Repair / Diagnostic: frontend, domain rules, persistence, validation and callers.
- Warehouse / WarehouseStock / WarehouseMovement / Material: operational stock scenarios.
- PriceList / PriceListItem: editing, validity, selection and order-item pricing.
- Instrument / InstrumentType / Device / Site: identification and site relationships.

Search current code for placeholders, in-memory stores, no-op methods, hardcoded defaults, incomplete branches, skipped persistence and missing relationship validation.

## Work log

| Step | Completed result |
|---|---|
| 1 | Verified branch HEAD `e3fe4a6`; reviewed working protocol, project context and constitution |
| 2 | Inspected legacy CRUD removal commit `8be14a2` and parent `1dd08fc` |
| 3 | Compared legacy/current Repair and Diagnostic API routers and schemas |
| 4 | Recorded that generic `get_all`/`archive` do not establish lost business workflows |
| 5 | Reconfirmed Customer/Organization/Order mismatch and Device status persistence from source inspection |

## Next step

Compare Customer / Organization / Order legacy routes, schemas, frontend callers and migration history with current code. Record the evidence and data constraints before changing code or database contracts.


## Checkpoint 2 — Customer / Organization / Order comparison

**Compared revisions:** legacy parent `1dd08fc` and current branch at `f0d9ab9`.

### Customer legacy behavior

The legacy Customer API already exposed:
- list customers;
- get one customer;
- create;
- update;
- delete.

Legacy Customer schema and Domain entity both required a single `organization_id`. Therefore, the single-organization limitation predates DDD migration. It is a confirmed mismatch with the subsequently approved business model, but not a regression introduced by the CRUD-removal commit.

Current API retains list/get/create/update and an archive-based delete use case. The current Customer service and repository retain list behavior. This means customer listing was not lost during the migration.

### Customer organization association

Migration `1d3e5f7a9b20`:
- creates `customer_organizations` with a uniqueness constraint on `(customer_id, organization_id)`;
- backfills one association row from each existing `customers.organization_id`;
- leaves the original `customers.organization_id` column in place.

Current ORM has both the legacy single-organization field and the `customer_organizations` relationship. However:
- Customer Domain entity still contains only `organization_id: UUID`;
- CustomerMapper reads/writes only `model.organization_id`;
- Customer Application create/update commands do not manage association rows;
- Customer API schemas still accept/return one `organization_id`;
- Customer form requires one organization and disables submission if no organizations exist.

**Classification:** association-table migration is present, but the new 0..N relationship is not integrated into the Customer business use cases. **Incomplete migration confirmed.**

### Customer update contract

Both legacy and current `CustomerUpdate` schemas contain optional `organization_id`. In both inspected Application service implementations, update logic changes customer contact/details but does not apply `command.organization_id`.

**Classification:** stale/unused update field exists in both legacy and current versions; not a newly introduced regression. It should be resolved as part of the approved Customer–Organization relationship design, not patched as a one-off field update.

### Order organization dependency

Legacy Order API schema and Domain entity use `customer_id`; the legacy Order Domain entity inspected has no `organization_id`.

Migration `1d3e5f7a9b20` later:
- adds `orders.organization_id`;
- copies `customers.organization_id` into each order;
- makes the new column non-null;
- adds the Organization foreign key.

Current Order Domain entity and ORM model require `organization_id`. Current Order Application Service fetches Customer and copies `customer.organization_id` into the new Order. The current public Order create schema still asks only for Customer, so this dependency is implicit.

**Classification:** required Order→Organization dependency was introduced during the later schema evolution and is inconsistent with the approved business model. **Mismatch confirmed.** Historical values must be preserved while dependencies and production/site relationships are checked before any schema change.

### Checkpoint 2 work log

| Step | Completed result |
|---|---|
| 1 | Compared legacy/current Customer routes and schemas: customer list remains available |
| 2 | Compared legacy/current Customer service: current delete archives; list remains implemented |
| 3 | Read Customer–Organization migration: association table backfill exists, original single FK remains |
| 4 | Read current Customer Domain, ORM, mapper, repository and form: association table is not yet the active application contract |
| 5 | Compared legacy/current Order contracts and migration: Order organization FK was added later and populated from Customer |
| 6 | Found `CustomerUpdate.organization_id` accepted but unused in both legacy and current Application services |

### Next step

Inspect Organization ownership and the full dependency graph for `orders.organization_id`, `customers.organization_id`, and `customer_organizations`, including Site, production movements, repositories, tests, and frontend detail/edit flows. Do not change schema until the data and FK impact is understood.


## Checkpoint 3 — Organization / Site / Order dependency graph

Current source inspection at HEAD `59b5f5d`:

### Organization relationships

- Organization ORM retains the legacy one-to-many `customers` relationship through `Customer.organization_id`.
- Organization ORM also has a `customer_organizations` relationship.
- Organization Domain entity and mapper contain legal/business details only; they do not expose Customer associations.
- Organization Application service supports organization get/list/create/update, but no Customer–Organization association management.
- The repository tree contains the ORM association model and migration, but no dedicated CustomerOrganization Domain, Application, repository port, or Infrastructure repository.

**Finding:** association persistence exists, but association management is not implemented as an application use case. This confirms the incomplete integration identified in checkpoint 2.

### Site relationships

- Site ORM requires `organization_id`; Site Domain entity and mapper preserve that relationship.
- Site Application service supports get, list, list by organization, and create.
- Order ORM has optional `site_id`; Instrument ORM also has optional `site_id`.
- The approved model keeps Site distinct from Customer and payer Organization. Site ownership must not be repurposed as invoice payer selection.

**Finding:** Site is a separate organization-owned entity and has its own application flow. No Site behavior is changed by this audit.

### Order and production dependencies

- Order ORM currently requires both `customer_id` and `organization_id`; `site_id` is nullable.
- Order Domain and OrderMapper carry all three identifiers.
- Order Application create currently derives `organization_id` from Customer; the current public create schema accepts only Customer, number and order details.
- ProductionMovement references Order by `order_id`; it does not directly reference Organization or Customer in the inspected model.
- Order repository and mapper persist the organization and site identifiers as part of the aggregate.

**Finding:** the hidden Organization dependency is present across Order Domain, ORM, mapper, repository and Application create. The inspected production movement model depends on Order identity, so removing Order.organization_id does not imply changing ProductionMovement's direct FK. Full runtime/query and reporting dependencies still need review.

### Data migration implications

Migration `1d3e5f7a9b20` performs a one-time copy:
- Customer's existing Organization is copied into `customer_organizations`.
- The same Customer Organization is copied into `orders.organization_id`.
- Order's Organization FK is then made non-null.

The migration does not remove `customers.organization_id`; the current ORM still requires it. Therefore the join table is currently a parallel association representation, not the active source of truth.

No database data was queried during this GitHub-only audit. The number of existing rows, nullability in production, and whether any later records diverge between the legacy FK and association table remain unknown.

### Checkpoint 3 work log

| Step | Completed result |
|---|---|
| 1 | Inspected Organization ORM, Domain mapper, Application service and repository |
| 2 | Confirmed CustomerOrganization has persistence model/migration but no dedicated application/repository flow |
| 3 | Inspected Site ORM, Domain, mapper and Application service |
| 4 | Inspected Order ORM, Domain, mapper, repository and create flow |
| 5 | Inspected ProductionMovement relationship; it references Order directly |
| 6 | Recorded migration effects and explicitly marked production row state as unknown |

### Next step

Finish the Customer / Organization / Order dependency audit by inspecting all current references to the organization identifiers, frontend customer detail/edit flows, and database migration ancestry. Then define a safe staged transition that preserves historical values and keeps Site semantics intact. No schema or application code changes are authorized by this audit checkpoint alone.


## Checkpoint 4 — Customer / Organization frontend flows

Current frontend source inspected at HEAD `609593c`:

- Customer list loads and displays customer contact details.
- Customer detail displays name, contact person, phone, email, comment, discount and archive state; it does not display any related Organization.
- Customer create form exposes one required Organization selector.
- Customer create schema requires a UUID `organizationId`.
- Create submission is disabled when the Organization list is empty.
- The frontend Customer DTO and mapper expose one `organization_id`, not a collection.
- No Customer edit page or Customer update form appears in the inspected customer page/feature paths.
- Organization detail displays legal/contact fields but does not show associated Customers or Sites.
- Order creation frontend remains Customer-oriented; payer Organization is not requested by the Order form.

**Classification:** the current UI concretely enforces the one-organization-only model and prevents Customer creation without an Organization. It does not expose the approved 0..N relationship or display the associations. This is consistent with the backend contract mismatch; no separate legacy frontend comparison was possible at the pre-frontend revision inspected.

### Checkpoint 4 work log

| Step | Completed result |
|---|---|
| 1 | Inspected Customer list and detail pages |
| 2 | Inspected Customer API DTO, mapper, queries and create schema |
| 3 | Confirmed Customer form requires one Organization and blocks submit when none exist |
| 4 | Confirmed Customer detail does not display related Organizations |
| 5 | Inspected Organization detail; it does not display associated Customers/Sites |
| 6 | Confirmed Order create UI remains Customer-oriented |

### Next step

Complete the backend reference search and migration ancestry review, then consolidate the safe Customer–Organization–Order transition plan. Keep implementation changes separate from the audit.


## Checkpoint 5 — Alembic ancestry and migration semantics

Current migration source inspected at HEAD `e608f29`:

- Site persistence is introduced by `f1a2b3c4d5e6`, with required `sites.organization_id`.
- `0c9e8a7b6d5f` follows the Site migration and only adjusts timestamp defaults.
- `1d3e5f7a9b20` follows `0c9e8a7b6d5f`; it creates/backfills Customer–Organization links and adds/backfills the required Order Organization FK and optional Site links.
- `a7c9e2f4b610` is an explicit merge of `1d3e5f7a9b20` and `8d4f6a1b2c30`.

Several Alembic merge revisions contain empty `upgrade()`/`downgrade()` bodies. In the inspected files these are merge-only revisions whose purpose is to join migration graph heads, not runtime business operations. Their `pass` bodies must not be classified as forgotten application stubs.

The Customer migration `2b6f5480aadf` was also inspected; despite its filename, its upgrade body drops `verification_methods` and adds a customer-name index. It does not create the Customer table. The actual historical Customer table creation is earlier in the schema history and must be traced from the initial schema migration if column-level origin becomes relevant.

**Data limitation:** GitHub source reveals the intended migration statements, but does not reveal the current production row counts, actual applied Alembic revision, or whether production data has diverged. Those facts require local/database inspection before a destructive or nullability-changing migration.

### Checkpoint 5 work log

| Step | Completed result |
|---|---|
| 1 | Traced Site migration ancestry through `f1a2b3c4d5e6` and `0c9e8a7b6d5f` |
| 2 | Confirmed Customer/Order association migration `1d3e5f7a9b20` and merge revision `a7c9e2f4b610` |
| 3 | Distinguished intentional Alembic merge markers from application no-op stubs |
| 4 | Inspected `2b6f5480aadf` and recorded that its filename does not describe its actual operations |

### Next step

Inspect the original schema migration for Customer, Organization, Order, Site and their constraints; inspect the remaining application references and test coverage. Then publish a consolidated migration plan with explicit production checks required before implementation.


## Checkpoint 6 — Original database schema

The initial schema migration `72485e49cfd8_initial_schema.py` was inspected.

- Initial `customers` table already had a required `organization_id` FK to `organizations`.
- Initial `orders` table had a required `customer_id` FK to `customers`; it did not contain `organization_id`.
- Initial schema therefore confirms that Customer's one-Organization limitation existed from the first database schema, while Order's direct Organization dependency was introduced later by migration `1d3e5f7a9b20`.
- The initial schema also establishes Organization as a separate table and Order as directly owned by Customer.

This strengthens the earlier classification:
- Customer 0..N Organization is a later-approved business model change that requires an explicit migration from the original 1:1-ish required FK model.
- Order.organization_id is a later-added persistence dependency and is not part of the original Order ownership contract.

**No production database state was inspected.** The initial schema is historical evidence only and cannot establish the current production data state.

### Checkpoint 6 work log

| Step | Completed result |
|---|---|
| 1 | Inspected the initial schema migration `72485e49cfd8` |
| 2 | Confirmed original Customer had required Organization FK |
| 3 | Confirmed original Order had Customer FK but no Organization FK |
| 4 | Established chronology: Order Organization FK was added later in `1d3e5f7a9b20` |

### Next step

Complete a repository-wide reference inventory for Customer/Organization/Order IDs and review relevant architecture/business docs against the current implementation. Then prepare the smallest safe transition sequence, with production database checks clearly separated from GitHub-only validation.


## Checkpoint 7 — Order events and application wiring

Current source and tests inspected at HEAD `72d7740`:

- `Order.register()` emits `OrderRegistered`; the domain test confirms the event.
- `SqlAlchemyUnitOfWork.commit()` commits the transaction, collects registered aggregate events and dispatches them through `EventDispatcher`; infrastructure tests confirm dispatch and operation correlation.
- The Order Application service calls `register_aggregate()` for registration, so this event path is active.
- `OrderCreated` is defined as a domain event but no current Order creation path emits it.
- `OrderApplicationService` receives an `event_dispatcher` dependency but does not use it. Event dispatch is performed by the Unit of Work instead.
- The current source tree contains no production event-handler/subscriber modules. The event dispatcher is exercised by a unit test with an inline lambda; the Device event types also exist, but no production subscriber was found in the inspected tree.

**Classification:**
- OrderRegistered event production and dispatch — **Migrated / active infrastructure**.
- OrderCreated event — **Unused event type; potential unfinished scaffold**, not yet a confirmed missing business workflow.
- Unused event_dispatcher dependency on OrderApplicationService — **redundant wiring / cleanup candidate**, not a business capability.
- No production subscribers — **potential gap only** until business requirements establish which cross-module reactions must happen after registration or device connection.

No event behavior was changed.

### Checkpoint 7 work log

| Step | Completed result |
|---|---|
| 1 | Inspected AggregateRoot event collection and DomainEvent metadata |
| 2 | Inspected SQLAlchemy Unit of Work event dispatch after commit |
| 3 | Verified OrderRegistered event creation and dispatch in domain/infrastructure tests |
| 4 | Confirmed OrderCreated is not emitted by current Order creation flow |
| 5 | Confirmed OrderApplicationService's event_dispatcher argument is unused |
| 6 | Inspected current tree for production event subscribers; none found |

### Next step

Continue the audit beyond Customer/Order: compare Warehouse, Material and PriceList legacy workflows against current application/API/frontend. In parallel, retain the event findings as potential architecture cleanup until concrete business reactions are identified.


## Checkpoint 8 — Warehouse, Material and PriceList workflows

**Compared revisions:** legacy parent `1dd08fc` and current branch at HEAD `62b8381`; module design docs were also read.

### Warehouse — confirmed API/Application contract break

Legacy WarehouseApplicationService methods accepted only their command. The current service changed all write methods to require an authenticated `User` and enforce ADMIN/WAREHOUSE roles.

The current routers were not updated to pass that user:
- `create_warehouse` calls `service.create(command)`, while current signature is `create(command, user)`.
- `add_stock` calls `service.add_stock(command)`, while current signature is `add_stock(command, user)`.
- `create_movement` calls `service.create_movement(command)`, while current signature is `create_movement(command, user)`.

The app's global `require_password_change_completed` dependency authenticates the user, but does not pass the User object into endpoint functions or enforce the WAREHOUSE role. Therefore these three write routes reach a Python call with a missing required positional argument. The existing warehouse auth test only inspects authentication/CSRF dependencies on create; it does not invoke the endpoint or verify the Application service call. No Warehouse Application service test module exists in the current test tree.

**Classification:** **Confirmed API/Application integration defect** for warehouse creation, stock addition and movement creation. This is a current regression caused by adding Application-layer role checks without updating the API adapters. It is not merely an authorization policy question.

### Warehouse — documented stock-ledger invariant is not implemented

`docs/modules/warehouse.md` states: all changes to stock must happen through `WarehouseMovement`; direct quantity changes are forbidden; movements are the source of stock history.

Current code does not enforce that invariant:
- `add_stock()` creates or saves a WarehouseStock quantity directly and does not create a movement.
- `reserve()` and `release()` directly modify reserved quantity and save stock, without a movement record.
- `create_movement()` only saves a WarehouseMovement record; it does not update WarehouseStock.
- Movement types include RECEIPT, ISSUE, RESERVATION, RELEASE and ADJUSTMENT, but the movement service does not apply the corresponding stock effects.
- No Application-level tests for these Warehouse write workflows were found in the current test tree.

The legacy implementation already had these separate operations and the same lack of coupling, so this is **not proven to be a DDD migration regression**. It is a **confirmed gap between the documented business invariant and both inspected implementations**. Whether the original behavior was an intentional temporary stub or an accepted but incomplete first version requires product confirmation; the documentation makes the target invariant explicit.

### Warehouse — route coverage

Legacy and current routers both expose warehouse creation, stock addition, stock read, and movement creation. The current implementation adds the stock read endpoint's richer read model. Neither inspected version exposes reserve/release as API routes despite corresponding Application commands and methods.

**Classification:** reserve/release are internal Application use cases but not exposed HTTP workflows in either inspected revision; do not call this a migration loss without evidence of another caller.

### Material — CRUD migration and archive visibility

Legacy API exposed list/get/create/update/delete. Current API exposes list/get/create/update/archive/restore. The current service adds role checks and replaces physical delete with archive/restore, so the business capability is **replaced/refined**, not lost.

A repository/test-double mismatch was found:
- Current MaterialApplicationService tests use a FakeMaterialRepository whose `get_all()` excludes archived materials by default.
- Current SQLAlchemy MaterialRepository.get_all() queries all rows without filtering `archived`.
- The API list endpoint calls this repository method directly through the service.

Therefore the production list can include archived materials even though the Application test double models the default list as active-only. This is a **confirmed persistence adapter inconsistency**; it is not a legacy CRUD loss.

### PriceList — core management behavior

Legacy and current implementations both expose list/get/create/update PriceList and add/update/remove PriceListItem. Current model adds `price_list_type`, `currency`, `valid_from`, `valid_to`, stronger domain validation, and explicit active/deactivate behavior. The old and current PriceList Application service both include get-active and item operations.

Current API does not expose a dedicated `GET active` endpoint or a query to find a price by service code. Current Order Application/Domain/OrderItem code inspected has no PriceList dependency, service-code price lookup, or persisted order-line price snapshot.

The domain design `docs/domain/price-list.md` explicitly describes:
- `GetPriceByServiceCode` query;
- lookup of a price from an active PriceList;
- Order Application integration;
- calculation of an amount for an OrderItem.

The module document `docs/modules/price_list.md` also states that only an active PriceList is used for calculations and that the applied price must remain unchanged through the order lifecycle.

**Classification:** PriceList administration and item CRUD are migrated/extended. **Price calculation and Order price snapshot integration are missing relative to the documented domain design**, pending verification that the relevant document remains an approved baseline requirement and has not been superseded. No implementation is started.

### PriceList item error handling — potential defect

Current PriceList domain `remove_item()` silently filters the list and does not raise when the item ID does not exist. The current API expects `PriceListItemNotFoundApplicationError` for missing items, but the service does not check existence before calling the domain method. Thus deleting a nonexistent item may return success instead of 404.

Current domain `change_item_price()` and `change_item_description()` raise plain `ValueError` for missing items, while the current API catches only `PriceListItemNotFoundApplicationError`. This may result in an unhandled 500 instead of 404. Legacy API caught `ValueError` for these cases.

**Classification:** likely current API error-contract regression; verify with direct service/API tests before changing.

### Checkpoint 8 work log

| Step | Completed result |
|---|---|
| 1 | Compared legacy/current Warehouse service signatures and all three write routers |
| 2 | Read global authentication dependency and current Warehouse tests |
| 3 | Compared Warehouse service behavior with the stock-ledger invariant in `docs/modules/warehouse.md` |
| 4 | Compared Material legacy/current API and service behavior |
| 5 | Compared Material SQLAlchemy repository with its test fake; found archived-list mismatch |
| 6 | Compared PriceList legacy/current API/service/domain and current PriceList design documents |
| 7 | Compared Order Application/OrderItem against documented price calculation and immutable price snapshot requirements |
| 8 | Identified potential PriceList missing-item error mapping regression |

### Next step

Continue with Instrument / Device / Site and Verification lifecycle comparison. Before any Warehouse code fix, define the smallest coherent change for user forwarding and add route invocation tests. Treat stock ledger behavior and PriceList-to-Order calculation as separate business slices; do not mix them into the Customer/Organization migration.

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


## Checkpoint 9 — Device / InstrumentType / Site / Verification

**Compared revisions:** legacy parent `1dd08fc` and current branch at HEAD `8639210`; current instrument and verification architecture documents were reviewed.

### Device / Instrument

Legacy Device behavior:
- API exposed connect/disconnect only.
- Domain state changed between AVAILABLE, IN_WORK and COMPLETED.
- Legacy DeviceMapper always reconstructed status as AVAILABLE and did not persist status changes into the Instrument ORM. This was a real persistence gap in the legacy implementation.

Current behavior:
- Device is explicitly the card of one concrete measuring instrument; `InstrumentType` is a separate entity.
- Current Device API adds list/get/create/update and retains connect/disconnect.
- Current Device Application service validates InstrumentType existence on create and uses a Unit of Work for writes.
- Current ORM `Instrument.device_status`, mapper and repository persist the status; this closes the legacy status-persistence gap.
- Current DeviceMapper maps stored status to the enum, but catches an unknown status and silently substitutes `AVAILABLE`.

**Classification:**
- Device status persistence — **Migrated/fixed**; not a current in-memory stub.
- Device card create/list/update — **Expanded current capability**.
- Unknown persisted status silently becoming AVAILABLE — **Potential data-integrity defect**. It masks unexpected database values and can make an instrument appear available. No evidence yet that such values exist in production.
- Hardware/device connectivity is not established by these code paths: connect/disconnect update the domain status only. The current architecture document defines Device as the instrument card, so do not infer a missing physical hardware integration from these names.

### InstrumentType

Current InstrumentType has a distinct ORM, Domain entity, repository, Application service and API for create/list/get/update/archive/restore. Device creation validates that the referenced type exists.

This separation matches `docs/architecture/INSTRUMENT_CARD.md`: type-level properties remain on InstrumentType; instance name, modification and serial number remain on Device/Instrument. No confirmed migration loss was identified in this preliminary comparison. The current API's write endpoints authenticate/CSRF-protect requests; Application service itself does not enforce a role, which is a separate authorization-policy review item.

### Site

Site is not present in the inspected legacy module tree and was added later. Current Site:
- is owned by one Organization;
- supports get/list/list-by-organization/create;
- is independently mapped and persisted;
- is optionally linked to Order and Instrument.

The Site API passes the authenticated User into the Application service for create. This matches the current Customer/Organization/Site architecture decision. Site is a new model in the inspected history, not a migrated legacy Device feature.

### Verification — lifecycle migration

Legacy Verification behavior at parent revision:
- API exposed get-by-id and approve/reject actions.
- Application service exposed get/approve/reject.
- Domain represented the verification mainly by date, result, valid-until and unsuitable reason.
- There was no legacy create/start lifecycle in the inspected Verification Application/API.

Current Verification behavior:
- adds create in CREATED state and explicit start to IN_PROGRESS;
- preserves approve/reject as domain-specific final decisions, now only allowed from IN_PROGRESS;
- requires a real OrderItem and concrete Instrument at creation;
- persists verification type, created/start/decision timestamps and methodology string;
- writes audit records for create/start/approve/reject;
- tests cover role authorization, missing OrderItem/instrument, lifecycle transitions and audit records.

**Classification:** current lifecycle is **expanded and refined**, not a loss of legacy approve/reject behavior.

### Verification — full metrological process remains unimplemented

The approved architecture documents `VERIFICATION_DOMAIN_MODEL.md` and `VERIFICATION_AGGREGATE_MODEL.md` describe the intended subject process: method/version, conditions, operations, measurement points, actual measurements, calculations, metrological characteristics, acceptance evaluation and a decision grounded in those facts.

Current code stores a nullable `methodology` string and lifecycle/result fields; it does not yet store the execution facts, measurements, calculations or method version. The current `docs/modules/verification.md` explicitly acknowledges that methodology is currently a string and does not claim a universal method engine exists.

**Classification:** **Confirmed gap against the approved target domain model**, but not a regression introduced by the recent CRUD migration. It is a deliberately staged, unfinished domain capability. Do not solve it by adding generic measurement fields or a universal formula engine; follow the methodology-specific design.

### Verification persistence caveat

Current Application creation requires a concrete instrument, but the Verification ORM `instrument_id` remains nullable and the API read schema exposes it as optional. This is looser than the current creation invariant and the domain meaning of a verification of a concrete instrument. It may be retained for historical rows; production data and migration history must be checked before tightening the database constraint.

### Checkpoint 9 work log

| Step | Completed result |
|---|---|
| 1 | Compared legacy/current Device routers, services, entities, mapper and Instrument ORM |
| 2 | Confirmed legacy DeviceMapper did not persist/read status; current mapper/repository do |
| 3 | Identified current unknown-status fallback to AVAILABLE |
| 4 | Reviewed InstrumentType separation and current use cases |
| 5 | Reviewed Site API/Application/ORM and its optional Order/Instrument links |
| 6 | Compared legacy/current Verification API, Application, Domain, ORM, mapper and tests |
| 7 | Compared current Verification implementation with approved target aggregate/domain documents |
| 8 | Recorded nullable Verification.instrument_id as a historical-data-dependent contract mismatch |

### Next step

Continue the broad stub audit across Arshin/document workflows, repair/diagnostic validation and remaining integration boundaries. After that, consolidate the audit into a prioritized remediation plan. Keep all confirmed defects documented separately from business-model capabilities that require staged domain design.


## Checkpoint 10 — Repair / Diagnostic / Workflow / Document / Arshin

Current and legacy code plus current module documentation were inspected at HEAD `27185eb`.

### Repair and Diagnostic — core scenarios remain

Legacy and current API/Application contracts preserve the inspected business operations:
- Repair: get, create, start, complete, cancel.
- Diagnostic: get, create, update conclusion, set recommendation (current API names the conclusion action as completion).

Current code adds Application role checks and audit recording for Repair completion and Diagnostic completion. Existing current Application tests cover completion audit and unauthorized users. The earlier conclusion that these lifecycle operations were migrated remains valid.

### Repair and Diagnostic — missing relationship validation

Both current Application services create an aggregate using `order_item_id` without first checking that the OrderItem exists. Neither service depends on an OrderRepository. The database FK will reject an invalid ID at flush time, but the API does not translate that persistence failure into a domain/application 404 or 422.

This behavior also existed in the inspected legacy Application services, so it is **not a migration regression**. It is a **confirmed validation gap** relative to a clean application contract. Current tests construct arbitrary UUIDs for OrderItem and use fake repositories, so they do not exercise the database FK boundary.

### Repair lifecycle invariants

Current Repair Domain methods `start()`, `complete()` and `cancel()` directly assign status without checking the previous state. For example, the entity itself does not prevent completing a NEW repair or starting a completed/cancelled repair. The current Repair module document lists the lifecycle methods and statuses but does not provide a complete transition matrix.

**Classification:** missing transition guards are a **potential domain invariant gap**, not yet a confirmed business-rule violation. The permitted transitions must be agreed from actual repair workflow requirements before adding guards. Do not invent a state machine from status names alone.

### Workflow — current orchestration is separate but lightly guarded

Current Workflow Application service starts, advances and completes WorkflowInstance records through domain service and repositories. It is a newer workflow mechanism and is not present in the inspected legacy revision, so it is not a migrated legacy CRUD capability.

Current Workflow API write endpoints do not declare endpoint-level `get_current_user` or CSRF dependencies, and the Application service does not accept a User or enforce a role. The global `require_password_change_completed` dependency authenticates the session but does not provide role authorization or CSRF protection. This is a **confirmed security-contract gap** for state-changing Workflow endpoints, subject to checking any additional outer middleware not represented in the inspected FastAPI setup.

Workflow Application service also does not use an explicit UnitOfWork; repository save behavior and session dependency lifecycle need a separate transaction-boundary review before declaring persistence incomplete.

### Document — model-only persistence placeholder

Current source tree contains ORM models `Document` and `DocumentTemplate`, but no Document Domain, Application service, repository port/adapter, API router or file-storage adapter. The model stores optional `file_path`; no binary storage behavior or document generation workflow exists in the current application tree.

`docs/modules/document.md` explicitly records this as the confirmed current state and marks generation, attachment, storage abstraction, history and legal document reproduction as future design candidates.

**Classification:** model-only placeholder, **not a forgotten completed workflow** based on the inspected history. It is an intentionally incomplete module whose scope requires a separate document-domain design.

### Arshin — persistence model only

Current source tree contains `ArshinExport` ORM model and the Arshin module document, but no Arshin Domain, Application, repository, API router, XLSM template adapter or external integration implementation.

The module document describes validation, export-file generation, export history and controlled repeat-export behavior. None of these use cases is implemented in the current application tree.

**Classification:** **confirmed unimplemented module relative to its module design**, not a regression shown to have occurred during DDD migration. It must be treated as a separate business implementation stage, especially because it transfers legally significant verification results. Do not infer that the existence of the ORM table means export works.

### Checkpoint 10 work log

| Step | Completed result |
|---|---|
| 1 | Compared legacy/current Repair and Diagnostic routes and Application services |
| 2 | Inspected current Repair/Diagnostic entities, repositories and Application tests |
| 3 | Confirmed missing OrderItem existence checks in both services |
| 4 | Identified unguarded Repair lifecycle methods as a transition-rule question |
| 5 | Inspected Workflow API/Application and global FastAPI authentication dependency |
| 6 | Confirmed Document currently has ORM models only, matching its factual-state document |
| 7 | Confirmed Arshin currently has an ORM model only; no application/API/infrastructure workflow found |

### Next step

Complete a final cross-module search for placeholder code, incomplete route-to-service calls, missing CSRF/role enforcement and persistence transaction gaps. Then consolidate confirmed defects and unfinished business capabilities into a prioritized remediation roadmap. Do not begin implementation of Arshin, Document, Workflow or full metrological execution as part of this audit.


## Checkpoint 11 — Cross-module transaction and CSRF audit

Current source was checked at HEAD `10e5087`. The following files establish the transaction contract:
- `backend/app/db/database.py`: `SessionLocal` uses `autocommit=False`; `get_db()` closes the session without committing.
- `backend/app/core/dependencies/database.py`: `get_session()` also closes the session without committing.
- `backend/app/infrastructure/*/*repository.py`: repository write methods generally call `flush()`, which does not commit the transaction.
- `backend/app/core/dependencies/uow.py`: the explicit SQLAlchemy UnitOfWork commits on successful context exit.

A cross-check of Application services with persistence writes found three write services without a UnitOfWork or explicit commit:

### Material

- MaterialApplicationService has no UnitOfWork dependency.
- create/update/archive/restore call MaterialRepository.save().
- MaterialRepositorySQLAlchemy.save() only flushes.
- The repository is created with the request-scoped `get_session()`, which closes without committing.

**Classification:** **Confirmed transaction-boundary defect.** Material mutations can be returned by the API after flush but are rolled back when the uncommitted session is closed. Existing Application tests use an in-memory fake repository and do not exercise SQLAlchemy transaction commit.

### PriceList

- PriceListApplicationService has no UnitOfWork dependency or explicit commit.
- create/update/activate/add_item/remove_item/update_item call PriceListRepository.save().
- PriceListRepositorySQLAlchemy.save() only flushes.
- The repository is created with request-scoped `get_session()`, which closes without committing.
- Current PriceList tests use a fake repository and do not exercise database transaction persistence.

**Classification:** **Confirmed transaction-boundary defect** for PriceList and PriceListItem mutations.

### Workflow

- WorkflowApplicationService has no UnitOfWork dependency or explicit commit.
- start/move_next/complete call WorkflowInstanceRepository.save_instance().
- WorkflowInstanceRepositorySQLAlchemy.save_instance() only flushes.
- The repository is created with request-scoped `get_session()`, which closes without committing.
- Current Workflow Application tests use fake repositories and do not exercise database transaction persistence.

**Classification:** **Confirmed transaction-boundary defect** for WorkflowInstance writes.

### Transaction boundary cross-check

The following write services do have a UnitOfWork or explicit commit path in the inspected source: Customer, Organization, Order, Device, InstrumentType, Site, Verification, Repair, Diagnostic and Warehouse. This is a source-level wiring check, not a production database test.

### CSRF protection gaps

The authentication architecture states that state-changing cookie-authenticated requests require CSRF validation. Current write routes were checked:

- `POST /warehouse-stocks/` has no endpoint-level `require_csrf`.
- `POST /warehouse-movements/` has no endpoint-level `require_csrf`.
- Workflow `POST /start`, `POST /move-next`, and `POST /complete` have no endpoint-level `require_csrf`.

The global `require_password_change_completed` dependency authenticates the user but does not validate CSRF. Therefore these state-changing routes do not satisfy the documented CSRF contract.

The Workflow routes also do not pass a User into Application and WorkflowApplicationService has no role authorization. `AUTHORIZATION.md` does not currently define a Workflow role contract, so role policy should be designed separately; CSRF protection is already a documented requirement.

### Tests that failed to expose the transaction defects

- Material Application tests use `FakeMaterialRepository`.
- PriceList Application tests use `FakePriceListRepository`.
- Workflow Application tests use fake repositories.
- No corresponding SQLAlchemy integration test was found in the inspected paths to assert that a write survives session closure and a fresh session read.

This is a systemic testing gap: Application unit tests verify in-memory behavior but do not prove persistence integration.

### Checkpoint 11 work log

| Step | Completed result |
|---|---|
| 1 | Verified SessionLocal transaction configuration and request session teardown |
| 2 | Cross-checked Application write services against UnitOfWork/commit usage |
| 3 | Confirmed Material write path has no commit |
| 4 | Confirmed PriceList write path has no commit |
| 5 | Confirmed WorkflowInstance write path has no commit |
| 6 | Confirmed existing tests use fake repositories for these modules |
| 7 | Checked mutation routers against the documented CSRF contract; found Warehouse stock/movement and Workflow gaps |

### Remediation priority update

The highest-priority confirmed technical defects from the audit are now:

1. Material, PriceList and Workflow writes have no transaction commit boundary.
2. Warehouse create/add-stock/create-movement API adapters omit the required User argument after Application authorization was introduced.
3. Warehouse stock/movement and Workflow mutation routes omit CSRF validation.
4. Warehouse stock changes bypass the documented WarehouseMovement ledger invariant.
5. Customer/Organization/Order still implement the obsolete single-organization/direct-order-organization model.
6. Material SQLAlchemy list behavior differs from the active-only fake repository behavior.

These are separate repair slices. Do not combine them into a broad refactor. The next task is to finish the remaining repository scan and then select one bounded defect for implementation with regression tests.


## Checkpoint 12 — Frontend module coverage and audit consolidation

The current frontend source tree was inspected at HEAD `6b8b247`.

Feature folders exist for:
- Auth;
- Customers;
- Devices;
- Diagnostics;
- InstrumentType;
- Materials;
- Orders;
- Organizations;
- PriceLists;
- Repairs;
- Users;
- Verifications;
- WarehouseStock.

Page folders exist for:
- Auth;
- Customers;
- Devices;
- Diagnostics;
- InstrumentTypes;
- Materials;
- Orders;
- Organizations;
- PriceLists;
- Repairs;
- Users;
- Verifications;
- Warehouses.

No frontend feature/page was found for Site, Workflow, Document, Arshin or WarehouseMovement. The frontend tree has WarehouseStock but no corresponding WarehouseMovement feature. This is a source-tree inventory only; it does not establish that every existing page is complete or correctly integrated with its backend API.

### Consolidated audit status

The audit has compared the legacy revision `1dd08fc` with current source at successive documented checkpoints. The main confirmed findings are:

**Business model / incomplete migration**
- Customer's single required Organization is inherited from the original schema; the current approved 0..N association model is not integrated into Application/API/frontend.
- Order.organization_id was added after the initial schema and is still copied from Customer, contrary to the current approved Order business contract.
- CustomerOrganization association persistence and backfill exist but have no active Application/repository management flow.

**Confirmed runtime / persistence defects**
- Material, PriceList and Workflow write services lack a transaction commit boundary.
- Warehouse create/add-stock/create-movement API calls omit the User argument required by current Application signatures.
- Warehouse stock/movement and Workflow state-changing routes omit CSRF validation.
- Warehouse stock operations do not follow the documented WarehouseMovement ledger invariant.
- Material list repository returns archived materials while the test fake excludes them.

**Confirmed missing documented business capabilities**
- PriceList price lookup and Order price snapshot integration are absent relative to the domain design documents; verify that these requirements remain in the frozen baseline before implementation.
- Arshin export workflow is not implemented beyond its ORM model.
- Document workflow is not implemented beyond Document/DocumentTemplate ORM models.
- Verification's full metrological execution data (method version, operations, measurements, calculations, characteristics and acceptance evaluation) is not implemented; current module documentation explicitly describes this as a staged limitation.

**Potential defects / require explicit business rules**
- PriceList missing-item behavior may return success or an unhandled 500 rather than 404.
- DeviceMapper silently maps unknown stored status to AVAILABLE.
- Repair lifecycle transitions have no explicit state guards.
- Repair/Diagnostic do not validate OrderItem existence in Application before persistence.
- Verification.instrument_id remains nullable for historical compatibility despite current creation requiring a concrete instrument.
- Workflow transaction and CSRF issues are confirmed; its role policy and transition invariants require a separate business decision.

**Not classified as lost functionality**
- Generic CRUD `get_all`/`archive` methods without legacy API/UI callers.
- Device status persistence, which was absent in the legacy mapper but is now persisted.
- Site, which is a later-added entity rather than a removed legacy capability.
- Empty Alembic merge revisions, which are graph-merge markers rather than application no-op stubs.
- Repair/Diagnostic lifecycle actions that are present in both legacy and current API contracts.

### Audit completion boundary

This is a broad source-level audit, not a claim that every line of the repository or every production workflow has been runtime-tested. GitHub inspection cannot establish:
- current production database row counts or actual applied migration revision;
- whether historic records contain invalid enum values or missing foreign keys;
- actual browser behavior for every frontend module;
- external Arshin credentials, template files, service endpoints or acceptance workflow;
- actual warehouse movement practices used by the business.

These require local validation, database inspection and/or business confirmation. No destructive migration or production data change should be prepared from GitHub source alone.

### Recommended remediation order

1. Restore transaction boundaries for Material, PriceList and Workflow, with SQLAlchemy integration tests proving writes survive request session closure.
2. Repair Warehouse API/Application user forwarding and add route invocation tests; add CSRF dependencies to Warehouse stock/movement and Workflow mutation routes.
3. Align WarehouseMovement and WarehouseStock behavior with the documented movement-ledger invariant, after defining movement semantics and tests.
4. Complete Customer 0..N Organization integration and remove the hidden Order→Organization dependency in a staged, data-preserving migration.
5. Fix Material archived-list filtering and PriceList item not-found behavior.
6. Continue business-domain design for PriceList-to-Order price snapshots, Document, Arshin and full Verification execution as separate approved slices.

Each remediation item must have its own minimal change, focused tests, a separate commit and a local production-like validation checkpoint.

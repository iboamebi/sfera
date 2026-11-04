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

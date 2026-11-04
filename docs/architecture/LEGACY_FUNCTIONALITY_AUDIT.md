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

# Sfera Authorization

## Purpose

This document defines the current business authorization model for Sfera.

Authorization answers:

> What may the authenticated user do?

Authentication remains responsible only for establishing the identity of the user.

## Initial Roles

The initial role set is intentionally small and may be refined as business requirements become explicit:

- `admin` — full system administration;
- `operator` — customers, organizations, orders and related documents;
- `metrologist` — verification and related metrology operations;
- `technician` — diagnostics and repair;
- `warehouse` — materials and warehouse operations.

Roles are persisted on the User domain entity and in the existing `users` persistence model.

## Authorization Principle

Authorization is enforced server-side.

Frontend visibility is not a security boundary.

The implemented flow is:

```text
Authenticated User
        ↓
Application Authorization Policy
        ↓
Application Use Case
        ↓
Domain
```

API dependencies provide the authenticated user and transport-level authentication/CSRF enforcement. Business authorization is not implemented as scattered role checks in routers or React components.

## Initial Responsibility Boundaries

| Role | Primary responsibility |
|---|---|
| `admin` | Full system administration |
| `operator` | Customers, organizations, orders, documents |
| `metrologist` | Verification and metrology operations |
| `technician` | Diagnostics and repair |
| `warehouse` | Materials and warehouse operations |

The matrix above describes responsibilities rather than granting every individual endpoint. Exact permissions are introduced from concrete application use cases.

## Implemented Use-Case Authorization

### Order

The following Order application use cases require one of:

- `operator`;
- `admin`.

Implemented use cases:

- `create`;
- `add_item`;
- `update`;
- `register`.

Authorization is performed in the Application layer through the shared authorization contract. State-changing API routes authenticate the user and require CSRF protection, then pass the authenticated user to the Application use case.

### Customer

The following Customer application use cases require one of:

- `operator`;
- `admin`.

Implemented use cases:

- `create`;
- `update`;
- `delete` / archive.

`delete` performs a soft delete through the Customer domain `archive()` behavior. Physical deletion is not performed.

Authorization is performed in the Application layer. State-changing API routes authenticate the user and require CSRF protection, then pass the authenticated user to the Application use case.

### Organization

The following Organization application use cases require one of:

- `operator`;
- `admin`.

Implemented use cases:

- `create`;
- `update`.

Authorization is performed in the Application layer. State-changing API routes authenticate the user and require CSRF protection, then pass the authenticated user to the Application use case.

### Material

The following Material application use cases require one of:

- `warehouse`;
- `admin`.

Implemented use cases:

- `create`;
- `update`;
- `archive`;
- `restore`.

Authorization is performed in the Application layer. State-changing API routes pass the authenticated user to the Application use case and retain CSRF protection.

### Warehouse

Warehouse state-changing application use cases require one of:

- `warehouse`;
- `admin`.

The Warehouse authorization contract is implemented at the Application boundary for the currently migrated warehouse operations.

### Verification

The following Verification application use cases require one of:

- `metrologist`;
- `admin`.

Implemented use cases:

- `create`;
- `approve`;
- `reject`.

Authorization is performed in the Application layer. Verification creation and state-changing API routes authenticate the user, retain CSRF protection, and pass the authenticated user to the Application use case.

### Diagnostic

The following Diagnostic application use cases require one of:

- `technician`;
- `admin`.

Implemented use cases:

- `create`;
- `complete`;
- `set_recommendation`.

Authorization is performed in the Application layer. State-changing API routes authenticate the user and pass that user to the Application use case while retaining CSRF protection.

### Repair

The following Repair application use cases require one of:

- `technician`;
- `admin`.

Implemented use cases:

- `create`;
- `start`;
- `complete`;
- `cancel`.

Authorization is performed in the Application layer. State-changing API routes authenticate the user and pass that user to the Application use case while retaining CSRF protection.

## Authorization Contract

The shared Application authorization contract is responsible for expressing role requirements for concrete use cases.

Role checks belong in Application use cases, not in API routers or frontend components.

New permissions must be introduced from an explicit business use case and covered by Application and API regression tests.

No permissions are currently introduced for unrelated use cases merely because they are state-changing.

## Current Persistence

User roles are persisted as part of the existing `users` table.

No separate role or permission tables currently exist.

The role value object is part of the User domain model and is mapped by Infrastructure.

## Current Scope

Implemented:

- server-side authorization;
- User role value object;
- User role in the domain entity;
- User role persistence in the existing `users` table;
- authorization Application contract;
- authorization of Order creation, item addition, update and registration;
- authorization of Customer creation, update and deletion/archive;
- authorization of Organization creation and update;
- authorization of Material creation, update, archive and restore;
- authorization of Warehouse state-changing operations covered by the current application contract;
- authorization of Verification creation, approval and rejection;
- authorization of Diagnostic creation, completion and recommendation;
- authorization of Repair creation, start, completion and cancellation;
- API forwarding of authenticated users for implemented state-changing boundaries;
- API mapping of authorization failures to HTTP `403`;
- regression coverage for Application and API authorization boundaries.

Not yet introduced:

- database role tables;
- permission tables;
- per-endpoint permission registry;
- frontend authorization as a security mechanism;
- authorization rules for `Device`, `InstrumentType`, `PriceList` or `Workflow` without an explicit business requirement.

Authorization will continue to be introduced incrementally from concrete application use cases.

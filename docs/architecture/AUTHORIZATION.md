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

### Order registration

The `OrderApplicationService.register()` use case currently requires one of:

- `operator`;
- `admin`.

The authorization check is performed in the Application layer through the shared authorization contract.

```text
POST /orders/{order_id}/register
        ↓
Authenticated User
        ↓
OrderApplicationService.register(..., user)
        ↓
require_role(user, OPERATOR, ADMIN)
        ↓
Order.register()
```

Unauthorized users are rejected by the Application layer with an authorization error. The API boundary maps that error to HTTP `403 Forbidden`.

The API route also requires authentication and CSRF protection for this state-changing operation.

## Authorization Contract

The shared Application authorization contract is responsible for expressing role requirements for concrete use cases.

Role checks belong in Application use cases, not in API routers or frontend components.

New permissions must be introduced from an explicit business use case and covered by Application and API regression tests.

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
- authorization of order registration;
- API mapping of authorization failures to HTTP `403`;
- regression coverage for Application and API authorization boundaries.

Not yet introduced:

- database role tables;
- permission tables;
- per-endpoint permission registry;
- frontend authorization as a security mechanism;
- authorization rules for unrelated use cases without an explicit business requirement.

Authorization will continue to be introduced incrementally from concrete application use cases.

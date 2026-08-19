# Sfera Authorization

## Purpose

This document defines the initial business authorization model for Sfera.

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

These roles are a business starting point, not yet a database or API implementation contract.

## Authorization Principle

Authorization must be enforced server-side.

Frontend visibility is not a security boundary.

The target flow is:

```text
Authenticated User
        ↓
Authorization Policy
        ↓
Application Use Case
        ↓
Domain
```

API dependencies may provide the authenticated user and transport-level enforcement, but business authorization must not be implemented as scattered role checks in routers or React components.

## Initial Responsibility Boundaries

| Role | Primary responsibility |
|---|---|
| `admin` | Full system administration |
| `operator` | Customers, organizations, orders, documents |
| `metrologist` | Verification and metrology operations |
| `technician` | Diagnostics and repair |
| `warehouse` | Materials and warehouse operations |

The matrix above intentionally describes responsibilities rather than granting every individual endpoint. Exact permissions will be introduced from concrete application use cases.

## Current Scope

This is the initial authorization business contract.

It does not yet introduce:

- database role tables;
- user-role persistence;
- permission tables;
- JWT claims;
- frontend authorization logic;
- endpoint-specific permission checks.

Those changes require a concrete authorization use case and will be introduced incrementally.

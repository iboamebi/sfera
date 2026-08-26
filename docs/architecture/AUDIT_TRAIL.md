# Sfera Audit Trail

## Status

Architecture decision recorded. Implementation is not yet introduced.

## Date

2026-08-26

## Scope

This document records the audit requirements and architectural decisions established during the production-readiness audit of Verification and the comparison with the current Sfera architecture.

The document describes the required audit mechanism based on the current code. It does not treat future implementation as already existing.

---

## 1. Business Requirement

Sfera is used by multiple users. For every significant business change it must remain possible to determine:

- who performed the action;
- when it was performed;
- what changed;
- what the previous value was;
- what the new value became;
- why the change was made when a reason is required;
- which operation produced the change.

The historical chain must remain available after later changes to the business object.

The operational requirement is:

> It must always be possible to trace the responsible user at the end of a business-change chain.

---

## 2. Current Implementation Finding

The current code contains Domain Events and an EventDispatcher, but they are not a persistent audit journal.

Current event flow:

```text
Aggregate
    ↓
collect events
    ↓
UnitOfWork
    ↓
commit
    ↓
EventDispatcher
    ↓
Handlers
```

Domain event dispatch occurs after the database commit. Therefore a mandatory audit record must not depend exclusively on the current Domain Event dispatcher.

The current `UnitOfWork` provides the transactional boundary. Audit persistence must participate in that same transaction as the business mutation.

---

## 3. Architectural Decision: Audit Is a Transactional Persistence Concern

Business mutation and its mandatory audit record must be committed atomically.

Required flow:

```text
Application Use Case
        ↓
 business mutation
        ↓
 audit record
        ↓
 same UnitOfWork / transaction
        ↓
      COMMIT
```

On failure:

```text
business mutation + audit record
        ↓
      ROLLBACK
```

The current post-commit Domain Event dispatcher must not be treated as the sole persistence mechanism for mandatory audit records.

---

## 4. Actor Identity

The audit actor is the authenticated Sfera `User`.

The stable reference is:

```text
AuditRecord.actor_id → User.id
```

`username` is not the historical identity key.

The Application boundary already receives the authenticated `User` for protected business mutations. Verification approval and rejection are examples of this existing pattern.

Authentication/session details must not enter the Domain model merely to support audit.

The Domain remains independent from FastAPI, HTTP sessions and authentication infrastructure.

---

## 5. Audit-Worthy Operations

Audit is mandatory for operations that create, modify, archive, restore or otherwise change significant business state.

The minimum system rule is:

> Every significant business-state change or significant creation/archive operation must leave an immutable audit record.

Read-only operations are not included by default. Auditing data access is a separate future business/security requirement.

### Verification

The following operations are audit-worthy:

- create verification;
- approve verification;
- reject verification;
- archive verification;
- correction of erroneous or unreliable data.

`reject` requires a reason according to the Verification business rule.

Archive/correction actions must preserve the previous history rather than replacing it.

---

## 6. Verification History Rule

Verification history must never be physically deleted.

The current business rule is:

```text
Current relevant result
    = latest successfully completed verification
```

During an active set of current verifications, multiple verification records may exist. Until one successful verification is established as the applicable result, the competing records remain historical records. Once a later decision is established, the latest applicable decision has higher priority.

An older verification record is not deleted because a newer result becomes applicable.

Incorrect or unreliable data follows this flow:

```text
incorrect / unreliable data
        ↓
mark as invalid / archived
        ↓
record reason / basis
        ↓
retain original record
        ↓
create correction separately
```

The history must retain who, when and why.

---

## 7. Audit Record Format

The approved representation is **field-level changes**, not full-object snapshots for every mutation.

Conceptual record:

```text
AuditRecord
├── id
├── actor_id
├── occurred_at
├── action
├── entity_type
├── entity_id
├── changes
├── reason
└── operation_id
```

The `changes` payload records only business fields that actually changed.

Example:

```text
changes:
  status:
    old: "PENDING"
    new: "APPROVED"

  result:
    old: "..."
    new: "..."
```

For creation/archive/correction operations, the audit payload may contain the relevant field set necessary to reconstruct the operation. This does not imply that the complete ORM object should be serialized indiscriminately.

---

## 8. Immutability

Audit Trail is append-only.

Audit records must not be physically deleted or rewritten as part of ordinary application behavior.

The intended rule is:

```text
INSERT audit record
    ↓
never UPDATE
never DELETE
```

If an audit record itself is discovered to be incorrect, the correction must be represented by a new historical record rather than silently rewriting the original audit entry.

---

## 9. Operation Correlation

`operation_id` is required as the correlation identifier for one logical application operation that may produce multiple audit records.

This allows the history to answer both questions:

```text
Who changed this entity?
```

and:

```text
Which changes were part of the same operation?
```

The exact generation and propagation mechanism for `operation_id` remains an implementation decision.

---

## 10. Separation of Concerns

Audit Trail is not a replacement for business history.

The responsibilities are separate:

```text
Business entity/history
    ↓
current and domain-specific state

Audit Trail
    ↓
who / when / what / why / operation
```

Domain Events also remain a separate concern:

```text
Domain Event
    ↓
notify / coordinate application behavior

Audit Trail
    ↓
mandatory persistent historical trace
```

The existence of a Domain Event does not by itself satisfy the audit requirement.

---

## 11. Architectural Boundaries

The Audit implementation must follow the project Constitution:

```text
API
  ↓
Application
  ↓
Domain / shared contracts
  ↑
Infrastructure
  ↓
Database
```

The following are prohibited:

- FastAPI dependencies inside Audit domain logic;
- SQLAlchemy models inside Domain;
- direct database access from API routers;
- audit logic implemented as legacy CRUD;
- mandatory audit persistence only in a post-commit event handler.

The Application layer owns the use-case transaction boundary. Infrastructure owns persistence implementation.

---

## 12. Security and Integrity Requirements

The audit mechanism must preserve historical accountability even when a user is later archived or deactivated.

`actor_id` therefore references the stable User identity and must remain meaningful after the actor can no longer authenticate.

The audit journal itself must not become mutable merely because the referenced user is archived.

Authorization remains a separate concern. Existing business authorization determines whether a user may perform the operation; Audit Trail records which authenticated user actually performed it.

---

## 13. Current State vs Required State

### Already available in current code

- authenticated `User` identity;
- Application-level authenticated-user propagation for protected mutations;
- Application authorization for Verification approve/reject;
- Unit of Work transaction boundary;
- Domain Events infrastructure;
- logical `archived` state on the shared model base.

### Not yet implemented

- persistent Audit Record model;
- Audit Repository contract;
- Infrastructure audit persistence;
- transactional audit write integration;
- immutable database/application enforcement for audit records;
- operation correlation generation;
- field-level change generation;
- audit read/query contract;
- complete system-wide audit-worthy operation matrix.

---

## 14. Open Design Questions

The following remain deliberately open until the relevant current code is audited:

1. Exact Audit domain/shared contract and ownership.
2. Exact SQLAlchemy persistence model and migration.
3. How field-level changes are generated without duplicating business logic.
4. How `operation_id` is generated and propagated through nested application operations.
5. Whether audit persistence is exposed through a dedicated Repository Interface or another existing shared contract.
6. How database-level protection against UPDATE/DELETE is enforced in production.
7. Which additional modules and use cases are mandatory in the first audit rollout.
8. Whether audit read access requires a dedicated read model and authorization policy.
9. Retention, indexing and operational storage requirements for long-term history.

These questions must be answered from the current code and explicit business requirements before implementation.

---

## 15. Decision Summary

Approved decisions:

```text
1. Audit Trail is required system-wide for significant business changes.
2. Audit must identify the authenticated User by User.id.
3. Audit and business mutation must be atomic in the same transaction.
4. Current post-commit Domain Events are not the mandatory audit mechanism.
5. Audit uses field-level changes as the primary change representation.
6. Audit is append-only and historical records are never silently deleted or rewritten.
7. Verification history is never physically deleted.
8. Invalid/unreliable Verification data is archived/invalidated, with reason and actor/time history, and corrections are separate records.
9. operation_id correlates changes belonging to one logical operation.
10. Audit remains separate from Domain Event notification and business entity state.
```

Implementation must begin only after the remaining open design questions are resolved from the actual project contracts.
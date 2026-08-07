# Repository Architecture Audit

## Sfera Repository Layer Audit

Date:

2026-08-07

Status:

AUDIT COMPLETED

---

## Scope

Проверены:

- Domain Repository Interfaces
- Application Service dependencies
- Infrastructure Repository implementations
- Mapper usage
- Unit Of Work integration

---

# Current Repository Architecture


Application Service
|
v
Domain Repository Interface
|
v
Infrastructure Repository
|
v
Mapper
|
v
ORM Model
|
v
Database


---

# Validation Results

## Application Layer

Status:

COMPLIANT

Verified:

- Application depends only on repository interfaces.
- Application does not import Infrastructure.
- Business operations delegated to Domain entities.
- Transaction boundaries use UnitOfWork where required.

---

## Domain Repository Interfaces

Status:

PARTIALLY STANDARDIZED

Verified:

- Repository interfaces are located in Domain layer.
- Domain repositories do not depend on ORM.
- Infrastructure implementations are separated.

Found inconsistencies:

### Repository base abstraction

Current state:

Two approaches exist.

Direct ABC:

- CustomerRepository
- DeviceRepository
- DiagnosticRepository
- MaterialRepository
- OrderRepository
- OrganizationRepository
- PriceListRepository
- RepairRepository
- VerificationRepository

Generic base repository:

- WarehouseRepository
- WarehouseStockRepository
- WarehouseMovementRepository

Target:

All repository interfaces should use one common abstraction.

---

## Repository Method Contracts

Found inconsistencies:

### save()

Different return contracts:


save() -> Entity
save() -> None


Target:

Unified contract:


save(entity) -> Entity


Reason:

- consistent Application Service behaviour;
- easier testing;
- predictable repository API.

---

## Async / Sync Repository Style

Found:

PriceListRepository uses:


async def


Other repositories use:


def


Current infrastructure uses synchronous SQLAlchemy Session.

Target:

Use synchronous repository interfaces consistently.

---

# Infrastructure Repository Audit

Status:

COMPLIANT WITH TECHNICAL DEBT

Verified:

- ORM usage isolated in Infrastructure.
- Repository implementations depend on Domain interfaces.
- Mappers are located in Infrastructure.

---

# Technical Debt

## TD-001

MaterialRepository contains inline domain mapping.

Required:

Extract mapping into MaterialMapper.

---

## TD-002

Mapper invocation style is inconsistent.

Examples:

Instance style:


self.mapper.to_domain()


Static style:


Mapper.to_domain()


Required:

Single mapper usage convention.

---

## TD-003

VerificationRepository creates Mapper on every operation.

Current:


VerificationMapper().to_domain()


Required:

Store mapper instance during repository initialization.

---

# Standardization Plan

Order of changes:

1. Normalize repository interfaces.
2. Normalize repository method contracts.
3. Remove inline mappings.
4. Normalize mapper usage.
5. Run architecture validation.
6. Update migration documentation.

---

# Audit Result

DDD/Clean Architecture dependency rules:

PASSED

Remaining work:

Repository layer standardization only.

No architectural migration required.

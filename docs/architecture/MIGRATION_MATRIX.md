# Sfera Migration Matrix

| Module | CRUD | Domain | Application Service | Repository | API | Status |
|--------|------|--------|---------------------|------------|-----|--------|
| PriceList | archived | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| Customer | legacy | | | | | NEXT |
| Order | legacy | | | | | PLANNED |
| Material | legacy | | | | | PLANNED |
| Warehouse | legacy | | | | | PLANNED |
| Verification | legacy | | | | | PLANNED |
| Repair | legacy | | | | | PLANNED |
| Diagnostic | legacy | | | | | PLANNED |

---

## Migration flow

Каждый модуль переводится по схеме:

Domain
↓
Application Service
↓
Repository Interface
↓
Infrastructure Repository
↓
API

---

## Completed migrations

### PriceList

Completed:

- Domain entity
- Repository interface
- Infrastructure repository
- Application Service
- Dependency Injection
- API migration
- Legacy implementation archived

Archive:

`docs/archive/legacy_price_list/`

PriceList используется как эталон миграции CRUD → DDD/Clean Architecture.

---

## Architecture checkpoints

### Application Exceptions Isolation

Status:

COMPLETED

Completed:

- Application layer exceptions introduced
- Generic ValueError replaced in Application Services
- API routers migrated to application exceptions
- Exception boundaries isolated between API and Application layers

Modules:

- Order
- Material
- Diagnostic
- PriceList
- PriceListItem
- Repair
- Verification
- Warehouse

Validation:

- No `except ValueError` in `app/api`
- No application use cases raising generic `ValueError`
- pytest: 16 passed

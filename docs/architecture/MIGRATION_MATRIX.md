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

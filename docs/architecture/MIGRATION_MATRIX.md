# Sfera Migration Matrix

| Module | Legacy | Domain | Application Service | Repository | Infrastructure | API | Exceptions | Status |
|--------|--------|--------|---------------------|------------|----------------|-----|------------|--------|
| Organization | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| Customer | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| Order | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| Material | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| Warehouse | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| Verification | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| Repair | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| Diagnostic | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| PriceList | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| PriceListItem | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| Device | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| Workflow | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |

---

# Current Architecture

```
API
↓
Application Service
↓
Domain
↓
Repository Interface
↑
Infrastructure Repository
↓
Database
```

---

# Migration Standard

Каждый новый функционал реализуется исключительно по цепочке:

```
Application Service
        ↓
Repository Interface
        ↓
Infrastructure Repository
        ↓
Database
```

Правила:

- Domain не зависит от внешних слоев.
- Application не зависит от Infrastructure.
- API не содержит бизнес-логику.
- SQLAlchemy используется только в Infrastructure.
- Legacy CRUD запрещён.
- Новые use cases создаются только через Application Services.

---

# Completed Architecture Checkpoints

## DDD/Clean Architecture

Status:

COMPLETED

Completed:

- Domain isolation
- Application isolation
- Infrastructure isolation
- API migration
- Repository abstraction
- Legacy CRUD removal
- Device
- Workflow

---

## Application Exceptions Isolation

Status:

COMPLETED

Completed:

- Specialized application exceptions
- Generic ValueError removed
- API exception boundaries isolated

Modules:

- Order
- Material
- Diagnostic
- PriceList
- PriceListItem
- Repair
- Verification
- Warehouse
- Device
- Workflow

Validation:

- API imports only Application layer
- Application imports no Infrastructure
- Domain imports no external layers
- SQLAlchemy isolated in Infrastructure
- pytest: 16 passed

---

## Domain Exceptions Isolation

Status:

COMPLETED

Completed:

- Specialized domain exceptions
- Generic ValueError removed from migrated domain logic
- Domain validation boundaries isolated

Modules:

- Device
- Order
- Verification
- Warehouse

Validation:

- Domain has no ORM dependencies
- Domain has no Infrastructure dependencies
- pytest: 16 passed

---

## Architecture Dependency Audit

Status:

COMPLETED

Completed:

- Clean Architecture dependency verification
- API layer isolation verification
- Application layer isolation verification
- Domain layer isolation verification
- Repository interface boundary verification
- Infrastructure dependency direction verification

Validation:

- API contains no repository dependencies
- Application contains no Infrastructure dependencies
- Domain contains no ORM dependencies
- Infrastructure contains no API/Application dependencies
- pytest: 16 passed

---

# Next Architecture Audit

Следующий этап развития архитектуры:

- аудит полноты DDD-миграции всех модулей;
- поиск оставшихся нарушений зависимостей;
- проверка единообразия Application Services;
- проверка единообразия Repository Interfaces;
- проверка единообразия Infrastructure Repositories;
- актуализация архитектурной документации после аудита.

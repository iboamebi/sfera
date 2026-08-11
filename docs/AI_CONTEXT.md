# Sfera Project AI Context

## Назначение проекта

Сфера — информационная система сервисного центра и метрологической лаборатории.

Основное направление:

- учёт средств измерений (СИ);
- поверка средств измерений;
- ремонт;
- диагностика;
- документы;
- склад;
- финансы;
- интеграция с ФГИС Аршин.

Основная бизнес-ценность системы:

- управление жизненным циклом средств измерений;
- проведение поверок;
- фиксация результатов;
- подготовка документов;
- экспорт данных в ФГИС Аршин.

---

# Ключевой бизнес-процесс

Текущий реализованный процесс не использует `Case` или `Technological Card` как обязательные архитектурные сущности.

```text
Order
  ↓
OrderItem
  ↓
Workflow
  ↓
Verification / Repair / Diagnostic
```

Конкретный сценарий может использовать связанные складские и документальные операции.

### Реализованные доменные объекты

- Organization
- Customer
- Device
- Order
- Material
- Warehouse
- Workflow
- Verification
- Repair
- Diagnostic
- PriceList

`Case` и `Technological Card` не являются текущими реализованными доменными объектами и не должны описываться как обязательная часть текущей архитектуры.

Статус backend migration:

```text
DDD/CLEAN ARCHITECTURE MIGRATION COMPLETE
```

---

# Технологический стек

## Backend

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Docker / Docker Compose

## Инструменты качества

- pytest
- ruff
- pre-commit

## Frontend baseline

- React
- TypeScript
- Vite
- React Router
- TanStack Query
- Axios
- Material UI
- React Hook Form
- Zod

---

# Репозиторий

GitHub:

```text
iboamebi/sfera
```

Основная рабочая ветка:

```text
develop
```

---

# Структура проекта

Основной backend:

```text
backend/app/
```

```text
api/
application/
domains/
infrastructure/
models/
schemas/
shared/
```

### Назначение слоёв

| Слой | Назначение |
|------|------------|
| API | HTTP adapter |
| Application | Use Cases и orchestration |
| Domain | Бизнес-правила и domain model |
| Infrastructure | Persistence и внешние интеграции |
| Models | SQLAlchemy ORM models |
| Schemas | Pydantic API contracts |
| Shared | Общие архитектурные компоненты |

---

# Архитектура

Проект использует:

```text
DDD + Clean Architecture
```

Текущая структура зависимостей:

```text
API
  ↓
Application
  ↓
Domain
  ↓
Repository Interface
  ↑
Infrastructure Repository
  ↓
Database
```

Repository Interface является границей между use cases/domain и persistence implementation.

---

# Архитектурные правила

## Domain

Domain содержит:

- Entities;
- Aggregate Roots;
- Value Objects;
- Domain Services;
- Domain Exceptions;
- Domain Factories;
- Repository Interfaces;
- Domain Events, где они необходимы.

Разрешено:

- бизнес-правила;
- изменение состояния сущностей;
- доменная валидация;
- создание domain structures через factories.

Запрещено:

- SQLAlchemy;
- ORM;
- Session;
- Infrastructure;
- API.

---

## Application

Application содержит:

- Use Cases;
- Application Services;
- Commands;
- Application Exceptions;
- orchestration logic.

Application:

- управляет сценариями использования;
- загружает и сохраняет агрегаты через Repository Interfaces;
- вызывает domain behavior;
- определяет transaction boundary через Unit of Work.

Application не содержит бизнес-правила, которые должны находиться в Domain.

Запрещено:

- SQLAlchemy;
- ORM;
- Session;
- Infrastructure Repository implementations;
- API routers.

---

## Infrastructure

Infrastructure содержит:

- реализации Repository Interfaces;
- SQLAlchemy;
- ORM mapping;
- работу с базой данных;
- mappers;
- внешние интеграции.

Infrastructure не зависит от API/Application layers.

---

## API

API содержит:

- FastAPI routers;
- Request/Response Schemas;
- Dependency Injection;
- mapping Application Exceptions → HTTP responses.

API:

- принимает HTTP-запрос;
- формирует Application Command;
- вызывает Application Service;
- возвращает результат через response schema.

Запрещено:

- бизнес-логика;
- Repository-вызовы;
- SQLAlchemy;
- прямой доступ к БД;
- генерация domain identifiers.

---

# Identifier Generation Policy

Текущая политика:

- API routers не генерируют domain identifiers.
- Application Services генерируют identifiers для простых entity creation flows.
- Domain factories могут генерировать identifiers, когда это является частью создания полной domain structure.
- Domain `create()` methods получают identifier явно, если генерация identifier не является domain business rule.

Эта политика проверена в рамках Identifier Generation Audit — 2026-08-11.

Known technical debt:

- PriceList и PriceListItem имеют несогласованный creation contract относительно обязательного `Entity.id`.
- Это отдельная cleanup/migration задача и не относится к завершённому API identifier refactoring.

---

# Repository Boundary

## Domain Repository

Расположение:

```text
app/domains/*/repositories/
```

Назначение:

- интерфейсы хранения;
- абстракции доступа к данным.

Запрещено:

- SQLAlchemy;
- Session;
- ORM.

---

## Infrastructure Repository

Расположение зависит от bounded context и текущей инфраструктурной структуры:

```text
app/infrastructure/*/
```

Назначение:

- реализация Repository Interface;
- работа с SQLAlchemy;
- преобразование ORM ↔ Domain через Mapper.

Infrastructure implementations подключаются через Dependency Injection.

---

# Unit of Work

Unit of Work определяет transaction boundary для application use cases, изменяющих persistent state.

Application Services используют Unit of Work abstraction.

Infrastructure предоставляет concrete implementation.

Domain entities не управляют database transactions.

---

# Текущее состояние проекта

Полностью завершена миграция на DDD/Clean Architecture для модулей:

- Organization
- Customer
- Device
- Order
- Material
- Warehouse
- PriceList
- Workflow
- Verification
- Repair
- Diagnostic

Для Workflow завершены:

- Domain entities;
- Repository interfaces;
- SQLAlchemy repositories;
- WorkflowMapper;
- WorkflowStageMapper;
- WorkflowInstanceMapper;
- WorkflowApplicationService;
- команды Start / Move / Complete;
- Dependency Injection;
- API migration;
- unit и architecture tests.

## Architecture Baseline

Status:

```text
DDD + Clean Architecture migration completed
```

Current state:

- Domain layer isolated.
- Application layer independent from ORM and Infrastructure implementations.
- API contains no business logic or persistence access.
- Infrastructure uses dedicated mappers and repository implementations.
- Legacy CRUD layers removed.
- Architecture dependency rules validated.

Validation:

- pytest: 26 passed
- ruff check: passed
- ruff format --check: passed

---

# Архитектурные checkpoints

### Application Services Audit — 2026-08-10

Статус:

```text
COMPLETE
```

Проверены Application Services:

- Customer
- Device
- Diagnostic
- Material
- Order
- Organization
- PriceList
- Repair
- Verification
- Warehouse
- Workflow

Проверено:

- отсутствие CRUD-style proxy methods;
- делегирование business state changes в Domain;
- корректные Repository Interface boundaries;
- корректные Unit of Work transaction boundaries;
- отсутствие Infrastructure/ORM dependencies.

### API Layer Audit — 2026-08-10

Статус:

```text
COMPLETE
```

Проверены API routers и dependency boundaries.

Результат:

- API → Application boundary соблюдается;
- Repository/ORM/Session dependencies отсутствуют в API;
- business logic отсутствует в routers;
- UUID generation removed from create routers.

### Identifier Generation Audit — 2026-08-11

Статус:

```text
COMPLETE
```

Проверены API routers, Application Services, Domain entities, Domain factories и Domain `create()` methods.

Результат:

- API identifier generation removed;
- Application identifier generation aligned with current policy;
- Domain factories retain legitimate domain creation responsibilities;
- Order creation flow aligned;
- application tests: 26 passed.

---

# Legacy Layers

Legacy CRUD architecture has been removed.

Удалены/выведены из active architecture:

- `app/crud`
- `app/services/price_list_service.py`
- `app/api/base_router.py`

Новые features не должны добавляться в legacy CRUD style.

---

# Технический долг

## PriceList creation contract

`PriceList` и `PriceListItem` имеют creation paths, которые не предоставляют обязательный `Entity.id` согласованно.

Required follow-up:

1. Add dedicated PriceList application tests.
2. Define intended identifier creation contract.
3. Update Domain/Application contracts consistently.
4. Validate repository and mapper behavior.
5. Keep cleanup isolated from unrelated feature work.

## Existing API contract debt

Отдельно отслеживаются:

- PriceListItem update contract semantic inconsistencies;
- Device connect/disconnect response schemas;
- Material `PUT` endpoint with partial-update semantics.

Эти задачи не являются blockers для завершённой architecture migration.

---

# Frontend Direction

Backend Domain/Application layers являются source of truth для business rules.

Frontend не дублирует backend business logic.

Frontend development follows:

```text
Frontend Architecture
  ↓
Application Shell
  ↓
Backend API Integration
  ↓
One User Scenario
  ↓
Validate
  ↓
Next Scenario
```

Архитектурный baseline frontend описан в:

```text
 docs/FRONTEND_ARCHITECTURE.md
```

---

# Documentation Governance

Документы должны отражать фактическое состояние repository.

Основные документы:

- `docs/AI_CONTEXT.md` — контекст для восстановления сессии;
- `docs/MIGRATION_STATUS.md` — migration/checkpoint status;
- `docs/ARCHITECTURE.md` — архитектурное описание;
- `docs/architecture/MIGRATION_MATRIX.md` — migration matrix;
- `docs/architecture/PROJECT_CONSTITUTION.md` — архитектурные правила;
- `docs/FRONTEND_ARCHITECTURE.md` — frontend baseline.

При архитектурных изменениях сначала проверяется фактический код, затем синхронизируется соответствующая документация.

---

# Current Development Phase

As of 2026-08-11:

```text
Backend DDD/Clean Architecture migration: COMPLETE
Architecture audits: COMPLETE
Current phase: incremental technical-debt cleanup and frontend preparation
```

Работа продолжается по правилу:

```text
analyze → one file → y → next
```

Feature migration и architectural cleanup не смешиваются.

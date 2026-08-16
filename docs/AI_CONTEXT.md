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

## Ключевой бизнес-процесс

```text
Order
  ↓
OrderItem
  ↓
Workflow
  ↓
Verification / Repair / Diagnostic
```

`Case` и `Technological Card` не являются текущими обязательными доменными объектами.

Реализованные доменные объекты:

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

---

# Архитектура

Проект использует:

```text
DDD + Clean Architecture
```

Слои:

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

### Domain

Содержит Entities, Aggregate Roots, Value Objects, Domain Services, Domain Exceptions, Domain Factories и Repository Interfaces.

Не зависит от SQLAlchemy, ORM, Session, Infrastructure или API.

### Application

Содержит Use Cases, Application Services, Commands и Application Exceptions.

Application координирует use cases, работает через Repository Interfaces, вызывает Domain behavior и определяет transaction boundary через Unit of Work.

Не зависит от ORM или Infrastructure implementations.

### Infrastructure

Содержит SQLAlchemy repositories, ORM mapping, mappers, database access и внешние интеграции.

### API

Содержит FastAPI routers, request/response schemas, DI и mapping Application Exceptions → HTTP responses.

API не содержит business logic, Repository/ORM access или прямой доступ к БД.

---

# Unit of Work

Unit of Work определяет transaction boundary application use cases, изменяющих persistent state.

Application Services используют `UnitOfWork` abstraction. Infrastructure предоставляет concrete implementation.

Domain entities не управляют database transactions.

---

# Identifier Generation Policy

- API routers не генерируют domain identifiers.
- Application Services генерируют identifiers для простых entity creation flows.
- Domain factories могут генерировать identifiers, когда это является частью создания полной domain structure.
- Domain `create()` methods получают identifier явно, если генерация identifier не является domain business rule.

Identifier Generation Audit завершён 2026-08-11.

Known technical debt:

- PriceList / PriceListItem creation contract не согласован с обязательным `Entity.id`.
- Dedicated PriceList application tests отсутствуют.

---

# Device Current Checkpoint

Device migration находится в состоянии:

```text
COMPLETED
```

Реализовано:

- Device domain entity;
- DeviceFactory;
- DeviceRepository interface;
- SQLAlchemy repository;
- DeviceMapper;
- Create / Connect / Disconnect commands;
- DeviceApplicationService;
- Dependency Injection;
- Device API router;
- validation referenced `InstrumentType` during creation;
- `InstrumentTypeNotFoundApplicationError` → HTTP 404;
- Unit of Work transaction boundary for `create`, `connect`, `disconnect`.

`DeviceApplicationService.create()` сначала загружает `InstrumentType`. Если тип отсутствует, application service выбрасывает `InstrumentTypeNotFoundApplicationError`, транзакция откатывается, Device не создаётся.

Успешные `create`, `connect` и `disconnect` выполняются внутри `with self._uow:` и завершаются commit. Исключения приводят к rollback через `UnitOfWork.__exit__`.

Последний commit:

```text
b69b551 refactor: add unit of work to device service
```

---

# Текущее состояние backend

DDD/Clean Architecture migration:

```text
COMPLETE
```

Architecture audits:

```text
COMPLETE
```

Legacy CRUD:

```text
REMOVED
```

Последняя полная validation:

```text
pytest -q
33 passed

ruff check .
All checks passed

ruff format --check .
352 files already formatted

git diff --check
passed
```

Текущая ветка:

```text
develop
```

Последний синхронизированный backend commit:

```text
b69b551
```

---

# Технический долг

## PriceList

`PriceList` и `PriceListItem` имеют несогласованный creation contract относительно обязательного `Entity.id`.

Required follow-up:

1. Add dedicated PriceList application tests.
2. Define intended identifier creation contract.
3. Update Domain/Application contracts consistently.
4. Validate repository and mapper behavior.
5. Keep cleanup isolated from unrelated feature work.

## Existing API contract debt

- PriceListItem update contract semantic inconsistencies;
- Device connect/disconnect response schemas;
- Material `PUT` endpoint with partial-update semantics.

Эти пункты не блокируют завершённую architecture migration.

---

# Frontend Direction

Backend Domain/Application layers являются source of truth для business rules.

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

Baseline: `docs/FRONTEND_ARCHITECTURE.md`.

---

# Documentation Governance

Основные документы:

- `docs/AI_CONTEXT.md` — контекст восстановления;
- `docs/MIGRATION_STATUS.md` — migration/checkpoint status;
- `docs/ARCHITECTURE.md` — архитектурное описание;
- `docs/architecture/MIGRATION_MATRIX.md` — migration matrix;
- `docs/architecture/PROJECT_CONSTITUTION.md` — нормативные правила;
- `docs/FRONTEND_ARCHITECTURE.md` — frontend baseline.

Документация должна отражать фактический repository state.

---

# Следующий этап

Следующий логичный backend шаг — интеграционные тесты Device API с FastAPI `TestClient` и dependency overrides.

Проверить:

1. `POST /devices/` с существующим `InstrumentType`;
2. `POST /devices/` с отсутствующим `InstrumentType` → HTTP 404;
3. DI `get_device_service`;
4. API → Application → Repository/UoW boundary;
5. отсутствие business logic в router.

Работа продолжается по правилу:

```text
analyze → one file → y → next
```

Feature migration и architectural cleanup не смешиваются.

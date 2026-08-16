# Sfera Migration Status

## Текущая задача

Переход от CRUD-архитектуры к DDD/Clean Architecture завершён.

Текущий этап — изолированная архитектурная и техническая валидация без смешивания feature migration и cleanup.

## Текущая схема

```text
API
→ Application Service
→ Domain
→ Repository Interface
↑
Infrastructure Repository
→ Database
```

---

## Статус миграции модулей

Следующие модули имеют завершённый DDD/Clean Architecture flow:

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

Для модулей завершены соответствующие Domain/Application/Infrastructure/API этапы, включая Dependency Injection и релевантные тесты.

### Device

Статус:

```text
COMPLETED
```

Выполнено:

- Domain entity `Device`;
- Device value objects and domain state transitions;
- `DeviceFactory`;
- `DeviceRepository` interface;
- SQLAlchemy repository;
- `DeviceMapper`;
- `CreateDeviceCommand`, `ConnectDeviceCommand`, `DisconnectDeviceCommand`;
- `DeviceApplicationService`;
- Dependency Injection;
- API router;
- validation of referenced `InstrumentType` during creation;
- Application error → HTTP 404 mapping for missing `InstrumentType`;
- Unit of Work transaction boundary for `create`, `connect` and `disconnect`.

Последний Device checkpoint:

```text
b69b551 refactor: add unit of work to device service
```

Текущий Application flow:

```text
API
→ DeviceApplicationService
→ DeviceRepository / InstrumentTypeRepository
→ Domain
→ UnitOfWork
→ Infrastructure
```

`DeviceApplicationService.create()` проверяет существование `InstrumentType` до создания Device. При отсутствии типа выбрасывается `InstrumentTypeNotFoundApplicationError`.

`DeviceApplicationService.create()`, `connect()` и `disconnect()` выполняются внутри Unit of Work. Успешный use case приводит к commit; исключение приводит к rollback через `UnitOfWork.__exit__`.

---

## Infrastructure Audit

Статус:

```text
COMPLETED
```

Проверено:

- Repository implementations;
- mapper alignment;
- Unit of Work transaction boundaries;
- dependency direction;
- отсутствие CRUD dependencies.

Infrastructure repositories используют Repository Interfaces и SQLAlchemy только в Infrastructure layer.

---

## Infrastructure Mapper Alignment

Статус:

```text
COMPLETED
```

Стандартизирован контракт mapper:

```text
to_domain(self, model)
to_model(self, entity, model)
```

`DeviceMapper` преобразует `Instrument` ↔ `Device`, включая `device_status`.

---

## Legacy Layers

Статус:

```text
REMOVED
```

Удалены/выведены из active architecture:

- `app/crud`
- `app/services/price_list_service.py`
- `app/api/base_router.py`

Новые features не должны использовать legacy CRUD style.

---

## Domain Layer Isolation

Статус:

```text
COMPLETED
```

Проверено:

- Domain не импортирует ORM models;
- Domain не импортирует Infrastructure;
- Domain factories создают domain entities;
- ORM mapping находится в Infrastructure.

---

## Architecture Audit

Статус:

```text
COMPLETED
```

Проверены:

- dependency direction;
- Domain isolation;
- Application isolation;
- API isolation;
- Repository boundaries;
- mapper consistency;
- legacy dependencies.

Результат:

- Domain не зависит от ORM/Infrastructure;
- Application не зависит от ORM/Infrastructure implementations;
- API не зависит напрямую от Repository/Session;
- Infrastructure не зависит от API/Application;
- legacy CRUD dependencies отсутствуют.

---

## Application Services Audit

### Checkpoint — 2026-08-10

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

---

## API Layer Audit

### Checkpoint — 2026-08-10

Статус:

```text
COMPLETE
```

Проверены API routers и dependency boundaries.

Результат:

- API → Application boundary соблюдается;
- Repository/ORM/Session dependencies отсутствуют в API layer;
- business logic отсутствует в routers;
- UUID generation removed from create routers;
- Application exceptions mapped to HTTP responses where contracts exist.

Known API technical debt:

- Device connect/disconnect endpoints пока используют структурированный payload без отдельной явной response schema;
- PriceListItem update contract имеет semantic inconsistencies;
- Material `PUT` использует partial-update semantics.

---

## Identifier Generation Audit

### Checkpoint — 2026-08-11

Статус:

```text
COMPLETE
```

Результат:

- API identifier generation removed;
- Application layer owns identifier generation for simple entity creation;
- Domain factories retain legitimate domain creation responsibilities;
- Domain `create()` methods receive identifiers explicitly where appropriate.

Known technical debt:

- PriceList / PriceListItem creation contracts are inconsistent with mandatory `Entity.id`;
- dedicated PriceList application tests are absent.

---

## Current Validation

Последняя полная backend validation:

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

---

## Current Checkpoint — 2026-08-16

```text
Backend DDD/Clean Architecture migration: COMPLETE
Architecture audits: COMPLETE
Device validation: COMPLETE
Device UnitOfWork integration: COMPLETE
```

Последний синхронизированный backend commit:

```text
b69b551 refactor: add unit of work to device service
```

Ветка:

```text
develop
```

Working tree был чистым после последнего push.

---

## Следующий этап

Следующий логичный шаг — интеграционные тесты Device API с FastAPI `TestClient` и dependency overrides.

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

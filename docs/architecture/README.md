# Sfera Architecture Documentation

## Назначение

Каталог содержит архитектурную документацию проекта «Сфера».

Документация используется для:

- проектирования новых модулей;
- контроля архитектурных решений;
- поддержки разработки;
- сохранения истории изменений.

---

# Architecture Baseline

Текущая архитектурная модель:

```text
DDD + Clean Architecture
```

Основные принципы:

- Domain Driven Design;
- Clean Architecture;
- Application Service Pattern;
- Repository Pattern;
- Unit of Work;
- Domain Events;
- Dependency Injection;
- явные границы бизнес-контекстов.

---

# Documentation Structure

```text
docs/
├── adr/
├── architecture/
├── domain/
├── api/
└── engines/
```

`architecture/` содержит нормативные архитектурные документы, стандарты и отдельные архитектурные аудиты.

---

# Architecture Layers

## API Layer

Назначение:

- HTTP интерфейс;
- валидация запросов;
- преобразование DTO;
- Dependency Injection;
- вызов Application Services/use cases;
- преобразование Application errors в HTTP responses.

Расположение:

```text
backend/app/api/
```

API не содержит бизнес-логики, не обращается к Repository напрямую и не работает с БД напрямую.

---

## Application Layer

Назначение:

- выполнение бизнес-сценариев;
- координация действий;
- Commands и Use Cases;
- управление границами Unit of Work;
- вызов Domain behavior;
- взаимодействие с Repository Interfaces;
- передача контекста выполнения операции;
- координация Domain Events в соответствии с Application flow.

Расположение:

```text
backend/app/application/
```

Application не зависит от Infrastructure implementations и не содержит persistence implementation.

---

## Domain Layer

Назначение:

- бизнес-правила;
- агрегаты;
- сущности;
- Value Objects;
- Domain Services;
- Domain Events;
- Repository Interfaces.

Расположение:

```text
backend/app/domains/
```

Domain не зависит от HTTP, FastAPI, SQLAlchemy, ORM, Session или Infrastructure.

---

## Infrastructure Layer

Назначение:

- SQLAlchemy Repository implementations;
- ORM Models;
- Mappers;
- работа с БД;
- внешние интеграции;
- технические реализации Application/Domain портов.

Расположение:

```text
backend/app/infrastructure/
```

Infrastructure не содержит бизнес-правил.

---

# Production Business Flow

Основной реализованный поток:

```text
Order
    ↓
OrderItem
    ↓
Workflow
    ↓
Verification / Repair / Diagnostic
```

---

# Domain Contexts

Текущие backend application/domain контексты:

```text
Auth
Customer
Device
Diagnostic
InstrumentType
Material
Order
Organization
PriceList
Repair
Verification
Warehouse
Workflow
```

Каждый контекст имеет собственную границу ответственности и соответствующие Commands, Application Services, Domain модели и Repository Interfaces там, где они требуются текущим сценарием.

---

# Instrument Card Context

Конкретный экземпляр средства измерений (`Device` / `Instrument`) отделён от типа средства измерений (`InstrumentType`).

Семантика карты СИ зафиксирована в:

```text
docs/architecture/INSTRUMENT_CARD.md
```

Основной контракт:

```text
Наименование СИ → Device.name
Тип СИ          → InstrumentType.name
Модель СИ       → Device.modification
```

Изменение карты СИ не изменяет `InstrumentType`, поскольку один тип может использоваться несколькими экземплярами.

---

# Operation Audit Context

Для многопользовательской работы система должна уметь определить происхождение значимой операции.

Архитектурное решение зафиксировано в:

```text
docs/architecture/AUDIT_ARCHITECTURE.md
```

Модель:

```text
OperationContext
├── operation_id: UUID
└── actor_id: UUID | None
```

Правила:

- `operation_id` идентифицирует одну логическую Application Operation;
- `actor_id` идентифицирует пользователя, инициировавшего операцию;
- для фоновых/system operations `actor_id` может быть `None`;
- `event_id` остаётся самостоятельным идентификатором Domain Event;
- несколько событий одной операции связываются через `operation_id`;
- mutation и audit persistence при необходимости используют одну границу Unit of Work;
- Domain не получает зависимость от HTTP, authentication/session infrastructure или audit implementation.

Текущий статус: **OperationContext реализован в Application layer и используется Order registration flow. Operation-to-event correlation реализован через UnitOfWork. Persistent Audit Trail ещё не реализован.**

---

# Development Process

Новые изменения выполняются по схеме:

```text
Analyze
    ↓
Read current code
    ↓
Minimal change
    ↓
Validate
    ↓
Commit / Push
    ↓
Local validation
    ↓
Next stage
```

Архитектурные изменения должны опираться на фактический код репозитория, а не на предположения о структуре проекта.

---

# Migration Rules

Миграция существующего функционала выполняется поэтапно:

```text
Analyze
    ↓
Domain
    ↓
Application
    ↓
Repository Interface
    ↓
Infrastructure Repository
    ↓
API
    ↓
Tests
    ↓
Legacy removal / archive
    ↓
Documentation
    ↓
Checkpoint
```

Правила:

- миграция начинается с аудита фактического кода;
- новый use case реализуется через Application Service/use case и Repository abstraction;
- бизнес-правила переносятся в Domain;
- SQLAlchemy и ORM остаются в Infrastructure;
- API не получает прямой доступ к Repository или Database;
- Legacy CRUD не используется как архитектурный слой нового use case;
- legacy удаляется или архивируется только после переноса логики и валидации;
- feature migration и architectural cleanup не смешиваются без необходимости для корректности.

Контроль статуса миграции по модулям ведётся в:

```text
docs/architecture/MIGRATION_MATRIX.md
```

---

# Architecture Rules

## Rule 1 — Dependency Direction

```text
API
 ↓
Application
 ↓
Domain
```

Infrastructure реализует необходимые интерфейсы и подключается через Dependency Injection.

Запрещено:

```text
Domain
 ↓
Infrastructure
```

```text
Application
 ↓
Infrastructure
```

```text
Application
 ↓
CRUD
```

```text
Router
 ↓
Repository
```

```text
Router
 ↓
Database
```

---

## Rule 2 — Business Logic

Бизнес-правила находятся в Domain. Application координирует use cases. API отвечает за транспорт.

---

## Rule 3 — Repository Boundary

Repository Interface является контрактом доступа Application к данным и определяется в Domain/соответствующем domain contract boundary.

SQLAlchemy Repository implementation находится в Infrastructure.

Repository не изменяет бизнес-правила и не принимает бизнес-решения.

---

## Rule 4 — Unit of Work

Application Service определяет транзакционную границу use case и координирует Unit of Work.

Изменения, требующие транзакционной целостности, выполняются в рамках одной транзакционной границы.

Unit of Work отвечает за управление транзакцией и persistence coordination, но не содержит бизнес-правила.

---

## Rule 5 — Audit Boundary

Audit operation context является Application concern и не становится Domain Entity или бизнес-правилом.

`operation_id` используется для корреляции операций и связанных Domain Events.

---

## Rule 6 — DTO and ORM Boundary

API DTO не являются Domain entities или ORM models.

Правила:

- API преобразует HTTP DTO в Application Commands/queries;
- Application работает с Application/Domain contracts;
- Infrastructure выполняет mapping между ORM models и Domain entities;
- ORM models не импортируются в Domain;
- SQLAlchemy не импортируется в Domain или Application.

---

## Rule 7 — Legacy Boundary

Legacy CRUD не является частью новой архитектуры.

Новые use cases не должны зависеть от legacy CRUD или возвращать legacy CRUD abstractions.

Legacy код может использоваться только как источник информации при миграции существующего функционала.

---

## Rule 8 — History

Для значимой бизнес-истории не следует заменять исторические изменения одним destructive update. Исправления должны оставлять необходимую трассируемость.

Для соответствующих сущностей используется логическое архивирование в соответствии с бизнес-требованиями.

---

# Current Architectural Status

```text
Backend DDD / Clean Architecture      COMPLETE
Legacy CRUD migration                 COMPLETE
Main backend architecture audits      COMPLETE
Operation audit architecture          DEFINED
OperationContext implementation       COMPLETE
Order operation-to-event correlation  COMPLETE
Persistent Audit Trail                NEXT
Frontend architecture                 IN PROGRESS
```

Статус миграции отдельных модулей является частью `MIGRATION_MATRIX.md` и не дублируется здесь.

---

# Related Documents

Нормативные и архитектурные документы:

```text
docs/architecture/PROJECT_CONSTITUTION.md
docs/architecture/PROJECT_ARCHITECTURE_STANDARD.md
docs/architecture/PROJECT_STRUCTURE.md
docs/architecture/INSTRUMENT_CARD.md
docs/architecture/AUDIT_ARCHITECTURE.md
docs/architecture/AUDIT_TRAIL.md
docs/architecture/AUTHENTICATION.md
docs/architecture/AUTHORIZATION.md
docs/architecture/MIGRATION_MATRIX.md
docs/architecture/ORDER_LIFECYCLE_AUDIT.md
docs/architecture/REPOSITORY_AUDIT.md
docs/architecture/README.md
```

Нормативным документом остаётся `PROJECT_CONSTITUTION.md`. `AUDIT_ARCHITECTURE.md` фиксирует архитектуру operation context и корреляции событий; `AUDIT_TRAIL.md` фиксирует требования к будущему persistent audit mechanism.

# Rule

Архитектурная документация является частью исходного кода и должна отражать фактическое состояние системы.

Любое существенное архитектурное изменение должно сопровождаться:

- изменением соответствующей документации;
- проверкой влияния на связанные документы;
- Git commit;
- валидацией после синхронизации.

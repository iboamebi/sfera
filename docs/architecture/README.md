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
- вызов Application Services.

Расположение:

```text
backend/app/api/
```

API не содержит бизнес-логики и не работает с БД напрямую.

---

## Application Layer

Назначение:

- выполнение бизнес-сценариев;
- координация действий;
- Commands и Use Cases;
- управление Unit of Work;
- передача контекста выполнения операции.

Расположение:

```text
backend/app/application/
```

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

Текущий статус: **архитектура определена, реализация OperationContext ещё не введена в код**.

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

## Rule 2 — Business Logic

Бизнес-правила находятся в Domain. Application координирует use cases. API отвечает за транспорт.

## Rule 3 — Repository Boundary

Repository Interface находится в Domain/Application boundary согласно конкретному use case; SQLAlchemy implementation находится в Infrastructure.

## Rule 4 — Audit Boundary

Audit operation context является Application concern и не становится Domain Entity или бизнес-правилом.

## Rule 5 — History

Для значимой бизнес-истории не следует заменять исторические изменения одним destructive update. Исправления должны оставлять необходимую трассируемость.

---

# Current Architectural Status

```text
Backend DDD / Clean Architecture      COMPLETE
Legacy CRUD migration                 COMPLETE
Main backend architecture audits      COMPLETE
Operation audit architecture          DEFINED
OperationContext implementation       NEXT
Frontend architecture                 IN PROGRESS
```

---

# Related Documents

Нормативные и архитектурные документы:

```text
docs/architecture/PROJECT_CONSTITUTION.md
docs/architecture/PROJECT_ARCHITECTURE_STANDARD.md
docs/architecture/PROJECT_STRUCTURE.md
docs/architecture/AUDIT_ARCHITECTURE.md
docs/architecture/AUDIT_TRAIL.md
docs/architecture/AUTHENTICATION.md
docs/architecture/AUTHORIZATION.md
docs/architecture/MIGRATION_MATRIX.md
docs/architecture/ORDER_LIFECYCLE_AUDIT.md
docs/architecture/REPOSITORY_AUDIT.md
docs/architecture/README.md
```

---

# Rule

Архитектурная документация является частью исходного кода и должна отражать фактическое состояние системы.

Любое существенное архитектурное изменение должно сопровождаться:

- изменением соответствующей документации;
- проверкой влияния на связанные документы;
- Git commit;
- валидацией после синхронизации.

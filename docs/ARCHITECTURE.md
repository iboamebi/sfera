# Sfera Architecture

## Общие принципы

Проект развивается по архитектуре:

```text
DDD + Clean Architecture
```

Главный принцип:

> Бизнес-правила не должны зависеть от инфраструктуры.

---

# Архитектурные слои

## Domain

Содержит:

- Entities;
- Aggregate Roots;
- Value Objects;
- Domain Services;
- Domain Exceptions;
- Repository Interfaces;
- Domain Factories where creation of a complete domain structure requires them.

Разрешено:

- бизнес-правила;
- изменение состояния сущностей;
- доменная валидация;
- создание доменных структур через entities/factories.

Запрещено:

- FastAPI;
- SQLAlchemy;
- ORM;
- Session;
- Infrastructure;
- API.

---

## Application

Содержит:

- Application Services;
- Use Cases;
- Commands;
- Application Exceptions.

Отвечает за:

- координацию сценариев;
- работу через Repository Interfaces;
- управление Unit of Work;
- генерацию технических identifiers для простого создания entities, когда это не является domain business rule.

Запрещено:

- SQLAlchemy;
- ORM;
- Database Session;
- прямые обращения к Infrastructure.

---

## Infrastructure

Содержит:

- SQLAlchemy Repository implementations;
- ORM Models;
- Mappers;
- работу с базой данных;
- внешние интеграции.

Infrastructure реализует интерфейсы Domain/Application и не содержит бизнес-правил.

---

## API

Содержит:

- FastAPI Routers;
- Request/Response Schemas;
- Dependency Injection;
- преобразование Application Exceptions → HTTP.

API отвечает только за транспортный слой.

Запрещено:

- бизнес-логика;
- SQLAlchemy;
- Repository-вызовы;
- работа с БД;
- генерация domain identifiers.

---

# Поток выполнения

Все новые сценарии строятся по одной схеме:

```text
HTTP Request
      ↓
API Router
      ↓
Application Service
      ↓
Domain Model
      ↓
Repository Interface
      ↑
Infrastructure Repository
      ↓
Database
```

---

# Репозитории

## Domain Repository

Расположение:

```text
app/domains/*/repositories/
```

Содержит только интерфейсы.

Не зависит от SQLAlchemy.

---

## Infrastructure Repository

Расположение:

```text
app/infrastructure/*/
```

Содержит:

- SQLAlchemy;
- ORM;
- преобразование ORM ↔ Domain через Mapper;
- реализацию Repository Interface.

---

# Производственный процесс

Основной реализованный бизнес-поток в текущей backend architecture:

```text
Order
    ↓
OrderItem
    ↓
Workflow
    ↓
Verification / Repair / Diagnostic
```

Текущий статус:

- Order migrated to DDD/Clean Architecture.
- Workflow migrated to DDD/Clean Architecture.
- Verification, Repair and Diagnostic migrated to DDD/Clean Architecture.
- Case and Technological Card are not current migration checkpoints and are not treated as implemented architectural layers unless their domain modules are introduced explicitly.

---

# Legacy Migration

Историческая схема:

```text
API
    ↓
CRUD
    ↓
Model
```

Целевая схема:

```text
API
    ↓
Application Service
    ↓
Repository Interface
    ↑
Infrastructure Repository
    ↓
Database
```

Legacy удаляется только после:

- полного переноса функциональности;
- прохождения тестов;
- проверки импортов;
- подтверждения отсутствия зависимостей.

Migration workflow:

```text
new → integrate → validate → remove legacy
```

---

# Правила разработки

Перед каждым изменением:

1. Прочитать актуальный код.
2. Проверить зависимости.
3. Анализировать существующую архитектуру.
4. Не делать предположений о структуре проекта.

Во время разработки:

- изменять один файл за раз;
- после каждого файла ожидать подтверждение `y`;
- не смешивать функциональные изменения и архитектурную очистку;
- соблюдать направление зависимостей DDD.

После завершения логического этапа:

1. Проверить `git status`.
2. Выполнить tests и linting.
3. Выполнить commit.
4. Выполнить push.
5. Только после синхронизации переходить к следующему этапу.

---

# Технический долг

Архитектурные упрощения выполняются отдельно от функциональных миграций.

Текущий технический долг:

- `PriceList` and `PriceListItem` creation contracts do not consistently provide the mandatory `Entity.id`;
- dedicated PriceList application tests are absent;
- PriceListItem API update contract has schema/command semantic inconsistencies;
- Device connect/disconnect endpoints lack explicit response schemas;
- Material update uses `PUT` with partial-update semantics.

These items are tracked separately and must be resolved incrementally. They do not reopen completed module migrations.

---

# Тестирование

Каждая миграция должна сопровождаться соответствующими:

- unit tests;
- architecture tests;
- API tests where applicable;
- migration/database checks where applicable;
- проверками основных бизнес-сценариев.

Текущий backend checkpoint:

- pytest: 26 passed;
- ruff check: passed;
- ruff format --check: passed.

Новая функциональность считается завершённой только после успешного прохождения релевантных проверок.

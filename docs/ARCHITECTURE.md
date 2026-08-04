# Sfera Architecture

## Общие принципы

Проект развивается по архитектуре:

```
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
- Repository Interfaces.

Разрешено:

- бизнес-правила;
- изменение состояния сущностей;
- доменная валидация.

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
- управление Unit of Work (при необходимости).

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

Infrastructure реализует интерфейсы Domain и не содержит бизнес-правил.

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
- работа с БД.

---

# Поток выполнения

Все новые сценарии строятся по одной схеме:

```
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

```
app/domains/*/repositories/
```

Содержит только интерфейсы.

Не зависит от SQLAlchemy.

---

## Infrastructure Repository

Расположение:

```
app/infrastructure/*/
```

Содержит:

- SQLAlchemy;
- ORM;
- преобразование ORM ↔ Domain через Mapper;
- реализацию Repository Interface.

---

# Производственный процесс

Основной бизнес-процесс:

```
Order
    ↓
Case
    ↓
Workflow
    ↓
Technological Card
    ↓
Verification / Repair / Diagnostic
```

Текущий статус:

- Workflow полностью переведён на DDD/Clean Architecture.
- Case и Technological Card остаются следующими ключевыми доменными объектами.

---

# Legacy Migration

Историческая схема:

```
API
    ↓
CRUD
    ↓
Model
```

Целевая схема:

```
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
2. Выполнить commit.
3. Выполнить push.
4. Только после синхронизации переходить к следующему этапу.

---

# Технический долг

Архитектурные упрощения выполняются только после завершения функциональных миграций.

Текущий запланированный рефакторинг:

- удалить `app/domains/workflow/services/workflow_service.py`, если он останется простой обёрткой над методами `WorkflowInstance`;
- удалить связанные неиспользуемые экспорты и импорты;
- сохранить чистую границу между Domain и Application.

---

# Тестирование

Каждая миграция должна сопровождаться:

- unit tests;
- architecture tests;
- проверкой API;
- проверкой миграций БД;
- проверкой основных бизнес-сценариев.

Новая функциональность считается завершённой только после успешного прохождения всех проверок.

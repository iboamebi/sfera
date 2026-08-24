# PROJECT_CONSTITUTION.md

# Конституция проекта «Сфера»

**Версия:** 1.1
**Статус:** LOCKED
**Дата принятия:** 19.07.2026

---

# 1. Назначение документа

Настоящая Конституция определяет обязательные архитектурные, технические и организационные правила разработки проекта «Сфера».

Документ является основным нормативным документом проекта.

Все архитектурные решения принимаются посредством Architecture Decision Record (ADR).

Настоящая редакция заменяет все предыдущие архитектурные соглашения.

---

# 2. Миссия проекта

«Сфера» — информационная система сервисного центра и метрологической лаборатории.

Основные направления:

- регистрация заказов;
- учет средств измерений;
- ремонт;
- диагностика;
- поверка;
- калибровка;
- складской учет;
- документооборот;
- интеграция с ФГИС «Аршин»;
- отчетность.

---

# 3. Цели архитектуры

Архитектура проекта должна обеспечивать:

- долгосрочную сопровождаемость;
- масштабируемость;
- минимальную связанность модулей;
- независимость бизнес-логики;
- тестируемость;
- повторное использование компонентов;
- возможность развития без переписывания системы.

---

# 4. Основные принципы

Проект основывается на:

- Domain-Driven Design (DDD);
- Clean Architecture;
- SOLID;
- DRY;
- KISS;
- Repository Pattern;
- Unit of Work;
- Dependency Injection.

---

# 5. Архитектурные принципы

## 5.1 Domain — единственный источник бизнес-логики

Все правила предметной области реализуются исключительно внутри Domain.

Запрещается размещать бизнес-логику:

- в API;
- в Application;
- в Repository;
- в Persistence Layer;
- в SQLAlchemy Model.

---

## 5.2 Application

Application реализует сценарии использования (Use Cases).

Допустимо:

- координация работы сервисов;
- управление транзакциями;
- вызов Domain;
- публикация событий.

Недопустимо:

- SQL;
- бизнес-правила;
- прямое изменение ORM-моделей.

---

## 5.3 Infrastructure

Infrastructure содержит технические реализации:

- Repository;
- внешние сервисы;
- файловые адаптеры;
- интеграции;
- драйверы оборудования;
- почту;
- очереди сообщений.

Infrastructure не содержит бизнес-логики.

---

## 5.4 API

API является исключительно транспортным слоем.

Допустимо:

- REST;
- HTTP;
- OpenAPI;
- DTO;
- авторизация;
- аутентификация;
- сериализация;
- валидация.

Недопустимо:

- SQL;
- вычисления;
- бизнес-правила;
- изменение Domain.

---

# 6. Архитектура системы

```
                API
                 │
         BaseRouter / HTTP
                 │
────────────────────────────────
          Application
      Services / Use Cases
                 │
────────────────────────────────
             Domain
                 │
────────────────────────────────
     Repository Interfaces
                 │
────────────────────────────────
         Infrastructure
      Repository Adapters
                 │
────────────────────────────────
        Persistence Layer
        ├── BaseCRUD
        ├── Generic CRUD
        └── SQLAlchemy Helpers
                 │
────────────────────────────────
          SQLAlchemy ORM
                 │
────────────────────────────────
           PostgreSQL
```

Persistence Layer является техническим механизмом хранения данных.

В состав Persistence Layer входят:

- BaseCRUD;
- Generic CRUD;
- SQLAlchemy Helpers;
- общие операции хранения данных.

Persistence Layer не содержит бизнес-логики и используется только через Repository.

---

# 7. Правило зависимостей

Допустимые зависимости:

```
API
 ↓
Application
 ↓
Domain
 ↓
Repository Interface
 ↓
Infrastructure
 ↓
Persistence Layer
 ↓
SQLAlchemy
 ↓
Database
```

Запрещённые зависимости:

```
Domain → Persistence Layer

Domain → SQLAlchemy

Domain → Infrastructure

Application → Persistence Layer

Application → SQLAlchemy

API → Persistence Layer

API → SQLAlchemy

Infrastructure → API
```
Разрешённые зависимости:

```
API
 ↓
Application
 ↓
Domain
 ↓
Repository Interface
 ↓
Infrastructure
 ↓
CRUD
 ↓
SQLAlchemy
 ↓
Database
```

---

Запрещённые зависимости:

```
Domain → SQLAlchemy

Domain → CRUD

Domain → Infrastructure

Application → CRUD

Application → SQLAlchemy

API → CRUD

API → SQLAlchemy

API → Repository

Infrastructure → API
```

---

# 8. Domain-Driven Design

Domain является центром системы.

Domain не знает:

- SQLAlchemy;
- FastAPI;
- PostgreSQL;
- HTTP;
- CRUD;
- Infrastructure.

Domain содержит исключительно предметную область.

---

## Domain включает

### Aggregate

Корневой объект предметной области.

Примеры:

- Order
- Device
- Verification

---

### Entity

Идентифицируемый объект.

---

### Value Object

Не имеет идентичности.

Например:

- SerialNumber
- VerificationInterval
- DeviceStatus

---

### Domain Service

Используется, если операция не принадлежит одной Entity.

---

### Policy

Правила предметной области.

---

### Specification

Проверка условий.

---

### Domain Event

Описание произошедшего события.

Например:

```
VerificationCompleted

RepairFinished

DeviceConnected

OrderClosed
```

---

# 9. Clean Architecture

Каждый слой знает только внутренний слой.

```
API
 ↓
Application
 ↓
Domain
```

Infrastructure является внешним адаптером.

---

# 10. Application Layer

Application реализует Use Cases.

Каждый сервис должен описывать завершённый пользовательский сценарий.

Например:

```
CreateOrder

PerformVerification

CloseOrder

ExportArshin

RegisterRepair
```

Application может:

- обращаться к нескольким Repository;
- публиковать события;
- открывать транзакции.

Application не может:

- выполнять SQL;
- изменять модели SQLAlchemy напрямую;
- реализовывать бизнес-правила.

---

# 11. Infrastructure Layer

Infrastructure содержит:

- Repository;
- интеграции;
- файловые сервисы;
- внешние API;
- SMTP;
- очереди;
- драйверы оборудования.

Infrastructure является техническим адаптером.

---

# 12. Generic CRUD

Generic CRUD является техническим слоем хранения данных.

Он существует исключительно для сокращения повторяющегося кода.

CRUD не является частью Domain.

CRUD не является частью бизнес-логики.

CRUD не знает предметную область.

---

Допустимые методы CRUD

```
get()

get_all()

create()

update()

archive()

filter()

paginate()

exists()
```

Любые вычисления запрещены.

Любые проверки предметной области запрещены.

---

# 13. Repository

Repository является адаптером между Domain и Generic CRUD.

Repository реализует интерфейс Domain.

Repository может:

- использовать CRUD;
- использовать SQLAlchemy;
- выполнять сложные запросы;
- использовать JOIN;
- использовать агрегатные функции.

Repository не может содержать бизнес-правила.

---

Каждый Repository обязан наследоваться от BaseRepository.

```
class CustomerRepositorySQLAlchemy(BaseRepository):
    ...
```

---

Специализированные методы разрешены.

Например:

```
find_by_email()

find_active()

find_last()

find_expired_verifications()
```

---

# 14. BaseRepository

Каждый Repository обязан наследоваться от BaseRepository.

BaseRepository предоставляет стандартные операции:

```python
get()

get_all()

create()

update()

archive()
```

Допускается расширение специализированными методами.

Запрещается изменять контракт BaseRepository без утверждения ADR.

---

# 15. BaseApplicationService

Все Application Services наследуются от BaseApplicationService.

Стандартный интерфейс:

```python
get()

get_all()

create()

update()

archive()
```

Специализированные сервисы могут добавлять собственные методы.

Например:

```python
perform_verification()

calculate_valid_until()

export_to_arshin()

connect_device()
```

---

# 16. API Layer

API строится на BaseRouter.

Router отвечает только за:

- получение HTTP-запроса;
- валидацию DTO;
- вызов Application Service;
- возврат результата.

Router не содержит:

- SQL;
- бизнес-логики;
- вычислений;
- изменения Domain.

---

# 17. DTO (Schemas)

Pydantic Schema используется исключительно как транспортный объект.

Разделение обязательно:

```text
Create

Read

Update

Response
```

DTO не является Domain Entity.

---

# 18. SQLAlchemy Models

SQLAlchemy Model является исключительно моделью хранения.

Model не содержит:

- бизнес-логики;
- вычислений;
- сложных методов.

Допустимо:

- relationships;
- constraints;
- indexes;
- ORM mapping.

---

# 19. Структура нового модуля

Каждый новый модуль обязан иметь следующую структуру.

```text
module/

├── api/
│
├── application/
│
├── domain/
│
├── infrastructure/
│
├── crud/
│
├── schemas/
│
└── tests/
```

При необходимости:

```text
commands/

queries/

events/

factories/

services/

repositories/

value_objects/

specifications/

policies/
```

---

# 20. Правила именования

Repository

```
CustomerRepository

VerificationRepository
```

Infrastructure

```
CustomerRepositorySQLAlchemy

VerificationRepositorySQLAlchemy
```

Service

```
CustomerService

WarehouseService

RepairService
```

CRUD

```
customer_crud

repair_crud

verification_crud
```

Router

```
customer.py

verification.py

warehouse.py
```

---

# 21. Dependency Injection

Все зависимости передаются через конструктор.

Запрещено:

```python
service = CustomerService()
```

Допустимо:

```python
service = CustomerService(repository)
```

---

# 22. Unit of Work

Все изменения нескольких Aggregate должны выполняться внутри UnitOfWork.

Application Service открывает транзакцию.

Repository не управляет транзакциями самостоятельно.

---

# 23. Domain Events

Каждое значимое событие предметной области оформляется как Domain Event.

Примеры:

```text
OrderCreated

OrderClosed

VerificationCompleted

RepairCompleted

DeviceConnected

DeviceDisconnected

WarehouseMovementCreated
```

Infrastructure отвечает за доставку событий.

Domain отвечает только за их создание.

---

# 24. Интеграции

Любая внешняя система подключается только через Infrastructure.

Примеры:

```text
ФГИС Аршин

SMTP

Telegram

ZeroTier

Файловое хранилище

PDF

Excel

REST API

SOAP
```

Domain не должен знать о существовании внешних систем.

---

# 25. Работа с оборудованием

Драйверы оборудования относятся к Infrastructure.

Application использует только абстракции.

Domain ничего не знает о физических устройствах.

---

# 26. Работа с файлами

Все файлы сохраняются через File Storage Adapter.

Запрещается записывать файлы напрямую из Domain.

---

# 27. Работа с БД

Все обращения к PostgreSQL выполняются только через:

```
Repository

↓

CRUD

↓

SQLAlchemy
```

Прямые SQL-запросы из API запрещены.

---

# 28. Работа с миграциями

Используется Alembic.

Любое изменение структуры базы данных сопровождается новой миграцией.

Изменение существующих миграций после публикации запрещено.

---

# 29. Документирование

Каждый модуль обязан содержать:

- описание назначения;
- зависимости;
- используемые события;
- основные Use Cases.

---

# 30. Тестирование

Минимальный набор тестов для каждого модуля:

- Unit Tests Domain;
- Repository Tests;
- API Tests.

Для сложной бизнес-логики обязательны интеграционные тесты.

---

# 31. Производительность

Оптимизация допустима только после подтверждения проблемы измерениями.

Запрещается усложнять архитектуру ради предполагаемой производительности.

---

# 32. Расширяемость

Новые функции должны добавляться через новые модули или расширение существующих слоёв.

Запрещается нарушать направление зависимостей для ускорения разработки.

---

# 33. Совместимость

Все новые компоненты обязаны быть совместимыми с:

- BaseRouter;
- BaseApplicationService;
- BaseRepository;
- BaseCRUD.

---

# 34. Обратная совместимость

Изменение публичных контрактов допускается только:

- при повышении версии Конституции;
- после принятия соответствующего ADR.

---

# 35. Правила рефакторинга

Разрешается:

- упрощать код;
- уменьшать дублирование;
- переносить техническую логику.

Запрещается:

- изменять бизнес-поведение без отдельного решения;
- нарушать архитектурные границы.

---

# 36. Код-ревью

При проверке изменений обязательно оцениваются:

- соответствие Конституции;
- соблюдение DDD;
- соблюдение Clean Architecture;
- отсутствие бизнес-логики вне Domain;
- отсутствие нарушения зависимостей.

Архитектурные нарушения являются критическими замечаниями.

---

# 37. Исключения

Любое исключение из Конституции оформляется отдельным ADR.

Временные решения должны иметь:

- обоснование;
- срок действия;
- план устранения.

Без ADR отклонения запрещены.

---

# 38. Architecture Decision Records (ADR)

Архитектурные решения фиксируются в каталоге:

```text
docs/adr/
```

Каждый ADR имеет статус:

- Proposed
- Accepted
- Deprecated
- Superseded

После получения статуса **Accepted** решение становится обязательным.

---

# ADR-001

## Название

Architecture v1.1

---

## Статус

Accepted

---

## Контекст

Проект достиг стадии, когда смешение CRUD, DDD и REST приводило к дублированию логики и усложнению сопровождения.

Требовалась единая архитектурная модель.

---

## Решение

Принять архитектуру:

```
API
↓
Application
↓
Domain
↓
Repository Interface
↓
Infrastructure
↓
Generic CRUD
↓
SQLAlchemy
↓
PostgreSQL
```

---

## Последствия

Положительные:

- единый стандарт разработки;
- минимизация дублирования;
- упрощение сопровождения;
- масштабируемость.

---

# ADR-002

## Название

Generic CRUD Preservation

---

## Статус

Accepted

---

## Контекст

Рассматривалась возможность полного удаления слоя CRUD.

После анализа установлено, что Generic CRUD представляет собой технический механизм доступа к данным и не нарушает DDD при условии правильного расположения.

---

## Решение

Generic CRUD сохраняется.

Использование допускается только через Repository.

Domain и Application не должны знать о существовании CRUD.

---

## Последствия

- уменьшение объёма повторяющегося кода;
- сохранение единой реализации CRUD;
- упрощение разработки новых модулей.

---

# ADR-003

## Название

Base Components

---

## Статус

Accepted

---

## Решение

В проекте обязательны следующие базовые компоненты:

```text
BaseRouter

BaseApplicationService

BaseRepository

BaseCRUD
```

Все новые модули обязаны использовать данные компоненты как основу.

---

## Последствия

- единообразная структура проекта;
- минимальное количество шаблонного кода;
- ускорение разработки новых модулей.

---

# ADR-004

## Название

Business Logic Isolation

---

## Статус

Accepted

---

## Решение

Бизнес-логика допускается исключительно в Domain.

Запрещено размещать бизнес-правила:

- в API;
- в Infrastructure;
- в Repository;
- в CRUD;
- в SQLAlchemy Model.

---

## Последствия

Domain становится единственным источником истины предметной области.

---

# 39. Контроль соответствия Конституции

Каждый Pull Request должен проверяться на соответствие настоящей Конституции.

Проверяются:

- направление зависимостей;
- отсутствие бизнес-логики вне Domain;
- использование базовых компонентов;
- соблюдение структуры модулей;
- наличие тестов;
- отсутствие архитектурных нарушений.

Несоответствие Конституции является основанием для отклонения изменений.

---

# 40. Заключительные положения

Настоящая Конституция вступает в силу с момента утверждения.

Все новые изменения проекта выполняются исключительно в соответствии с настоящим документом.

Изменение настоящей Конституции допускается только посредством нового Architecture Decision Record (ADR).

---

# Статус документа

**Версия:** 1.1

**Статус:** LOCKED

**Дата принятия:** 19 июля 2026 года.

Настоящий документ является основным архитектурным нормативом проекта «Сфера» и имеет приоритет над локальными соглашениями, комментариями и устными договорённостями.

---

# Приложение A. Эталонная структура проекта

```text
app/
├── api/
│   ├── base_router.py
│   └── routers/
│
├── application/
│   ├── base_service.py
│   └── <module>/
│       ├── commands/
│       ├── queries/
│       └── services/
│
├── domains/
│   └── <module>/
│       ├── entities/
│       ├── events/
│       ├── exceptions/
│       ├── factories/
│       ├── policies/
│       ├── repositories/
│       ├── services/
│       ├── specifications/
│       └── value_objects/
│
├── infrastructure/
│   ├── base_repository.py
│   └── <module>/
│
├── crud/
│
├── models/
│
├── schemas/
│
├── shared/
│
└── tests/
```

---

# Приложение B. Правила создания нового модуля

При создании нового функционального модуля разработчик выполняет следующие шаги:

1. Создать Domain.
2. Создать Repository Interface.
3. Реализовать Repository Adapter.
4. Создать Application Service.
5. Создать Router.
6. Создать Schemas.
7. Создать CRUD.
8. Написать тесты.
9. Обновить документацию.

---

# Приложение C. Контрольный список (Checklist)

Перед слиянием изменений необходимо убедиться, что:

- [ ] Бизнес-логика находится только в Domain.
- [ ] Repository наследуется от `BaseRepository`.
- [ ] Service наследуется от `BaseApplicationService`.
- [ ] Router использует `BaseRouter`.
- [ ] CRUD не содержит бизнес-логики.
- [ ] SQLAlchemy используется только в Infrastructure/CRUD.
- [ ] Добавлены или обновлены тесты.
- [ ] При необходимости создан новый ADR.
- [ ] Документация актуализирована.

---

# Приложение D. Поток выполнения запроса

Настоящая схема определяет обязательный путь прохождения любого пользовательского запроса через систему.

```text
                HTTP Request
                      │
                      ▼
               FastAPI Router
                      │
                      ▼
          Application Service
                      │
                      ▼
             Domain Model
                      │
                      ▼
         Repository Interface
                      │
                      ▼
     RepositorySQLAlchemy
                      │
                      ▼
          Persistence Layer
        (BaseCRUD / CRUD)
                      │
                      ▼
              SQLAlchemy ORM
                      │
                      ▼
               PostgreSQL
                      │
                      ▲
               HTTP Response
```

## Правила

- Router не обращается к Repository напрямую.
- Router не обращается к Persistence Layer.
- Application использует только Repository Interface.
- Domain не зависит от Infrastructure.
- Persistence Layer используется исключительно Repository.

---

# Приложение E. Правила размещения кода

| Что | Где размещается |
|------|-----------------|
| Entity | Domain |
| Aggregate | Domain |
| Value Object | Domain |
| Domain Event | Domain |
| Policy | Domain |
| Specification | Domain |
| Бизнес-правила | Domain |
| Расчёт срока поверки | Domain |
| Проверка возможности ремонта | Domain |
| Use Case | Application |
| Commands | Application |
| Queries | Application |
| Координация нескольких Repository | Application |
| Repository Interface | Domain |
| RepositorySQLAlchemy | Infrastructure |
| SQLAlchemy | Infrastructure / Persistence Layer |
| CRUD | Persistence Layer |
| SQL-запросы | Persistence Layer / Repository |
| REST API | API |
| Swagger | API |
| DTO / Schemas | API |
| Авторизация | API |
| Аутентификация | API |
| Интеграция с Аршин | Infrastructure |
| Работа с оборудованием | Infrastructure |
| Работа с PDF | Infrastructure |
| Работа с Excel | Infrastructure |
| SMTP | Infrastructure |
| Внешние REST API | Infrastructure |

---

# Приложение F. Запрещённые практики

Следующие зависимости и действия запрещены.

## Запрещённые зависимости

```text
Router → SQLAlchemy

Router → Persistence Layer

Router → RepositorySQLAlchemy

Application → SQLAlchemy

Application → Persistence Layer

Domain → SQLAlchemy

Domain → Persistence Layer

Domain → FastAPI

Infrastructure → API
```

## Запрещённые практики

- SQL внутри Router.
- SQL внутри Application.
- SQLAlchemy внутри Domain.
- Бизнес-логика внутри CRUD.
- Бизнес-логика внутри Repository.
- Бизнес-логика внутри Router.
- Использование ORM-моделей в Domain.
- Использование FastAPI внутри Domain.
- Изменение состояния Aggregate вне Domain.
- Обход Repository при работе с данными.

---

# Приложение G. Принципы развития проекта

Любое изменение архитектуры оценивается по следующим критериям.

## Архитектурные вопросы

Перед реализацией необходимо ответить:

1. Не нарушает ли изменение направление зависимостей?
2. Не переносится ли бизнес-логика из Domain в другой слой?
3. Не появляется ли дублирование существующей функциональности?
4. Можно ли реализовать изменение без нарушения Конституции?
5. Не увеличивается ли связанность между модулями?
6. Соответствует ли решение принципам DDD и Clean Architecture?

Если хотя бы на один вопрос получен отрицательный ответ, изменение должно быть пересмотрено или оформлено отдельным ADR.

## Принципы развития

При развитии проекта необходимо придерживаться следующих правил:

- расширять существующую архитектуру вместо её обхода;
- отдавать предпочтение повторному использованию компонентов;
- сохранять обратную совместимость публичных контрактов;
- минимизировать связанность модулей;
- документировать архитектурные изменения;
- сопровождать значимые изменения тестами.

## Правило изменения Конституции

Изменение настоящей Конституции допускается только посредством нового Architecture Decision Record (ADR).

Редактирование базовых архитектурных принципов без принятого ADR запрещается.

---

# Приложение H. Правила разработки модулей

Каждый новый модуль разрабатывается в следующем порядке.

## Шаг 1. Domain

Создаются:

- Entity
- Aggregate
- Value Objects
- Domain Events
- Repository Interface
- Policies
- Specifications

После завершения Domain переходить к следующему шагу.

---

## Шаг 2. Application

Создаются:

- Commands
- Queries
- Handlers
- Application Service

Application использует только Repository Interface.

---

## Шаг 3. Infrastructure

Создаются:

- RepositorySQLAlchemy
- интеграции
- внешние сервисы
- файловые адаптеры

Infrastructure реализует интерфейсы Domain.

---

## Шаг 4. Persistence Layer

Создаются:

- CRUD
- фильтрация
- общие операции хранения

Persistence Layer не содержит бизнес-логики.

---

## Шаг 5. API

Создаются:

- Router
- Schemas
- DTO

Router вызывает только Application Service.

---

## Шаг 6. Tests

Минимальный набор:

- Domain Tests
- Repository Tests
- API Tests

---

# Правило завершения модуля

Модуль считается завершённым только при выполнении всех условий:

- Domain полностью реализован.
- Repository реализован.
- Application реализован.
- API реализован.
- Написаны тесты.
- Обновлена документация.
- Нет нарушений Конституции.
- При необходимости добавлен ADR.

---

# Архитектурный чек-лист

Перед каждым Commit необходимо проверить:

□ Нет SQL вне Persistence Layer.

□ Нет SQLAlchemy вне Infrastructure.

□ Нет CRUD вне Repository.

□ Нет бизнес-логики вне Domain.

□ Repository не содержит бизнес-правил.

□ Application реализует только Use Cases.

□ Router вызывает только Service.

□ Все зависимости направлены внутрь архитектуры.

□ Используются BaseRouter, BaseRepository, BaseApplicationService и BaseCRUD.

□ Код соответствует Конституции проекта.

---

# История версий

| Версия | Дата | Изменения |
|--------:|:-----|:----------|
| 1.0 | 2026-07 | Первичная архитектурная редакция |
| 1.1 | 2026-07-19 | Утверждена DDD + Clean Architecture, сохранён Generic CRUD, введены BaseApplicationService, BaseRepository и ADR |

---

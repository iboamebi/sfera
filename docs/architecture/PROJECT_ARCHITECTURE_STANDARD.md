# Project Architecture Standard

## Проект

**Сфера**

## Версия

v1.0

## Статус

Утверждено

---

# Назначение

Настоящий документ является основным архитектурным стандартом проекта «Сфера».

Все новые модули, изменения и доработки должны соответствовать настоящему документу.

При возникновении противоречий данный документ имеет наивысший приоритет.

---

# Архитектурный стиль

Проект строится на основе:

- Domain-Driven Design (DDD)
- Clean Architecture
- SOLID
- Repository Pattern
- Unit of Work
- Dependency Injection
- CQRS (облегченная реализация)
- Domain Events

---

# Общая архитектура

```text
                    HTTP

                      │

                      ▼

             FastAPI Router

                      │

                      ▼

          Application Service

                      │

                      ▼

================ DOMAIN ================

                      │

                      ▼

          Repository Interface

                      │

                      ▼

============= INFRASTRUCTURE ===========

                      │

                      ▼

              SQLAlchemy ORM

                      │

                      ▼

                PostgreSQL
```

---

# Структура проекта

```text
app/

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
├── models/
│
├── core/
│
├── database/
│
└── tests/
```

---

# Назначение слоев

## API

Отвечает за:

- HTTP;
- Swagger;
- DTO;
- сериализацию;
- вызов Application Service.

Не содержит бизнес-логики.

---

## Application

Отвечает за:

- пользовательские сценарии;
- бизнес-процессы;
- координацию Repository;
- Unit of Work;
- Domain Events.

Является центром прикладной логики.

---

## Domain

Отвечает за:

- бизнес-модель;
- агрегаты;
- сущности;
- Value Objects;
- инварианты;
- бизнес-правила.

Полностью независим от инфраструктуры.

---

## Infrastructure

Отвечает за:

- SQLAlchemy;
- Repository;
- PostgreSQL;
- внешние сервисы;
- файловое хранилище;
- Unit of Work;
- интеграции.

---

## CRUD

CRUD — технический слой доступа к данным.

Разрешены только:

- SELECT;
- INSERT;
- UPDATE;
- DELETE.

---

# Dependency Rule

Разрешенные зависимости:

```text
API

↓

Application

↓

Domain

↓

Repository Interface

↓

Infrastructure
```

Запрещено:

```text
Domain

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

CRUD
```

---

# Repository Pattern

Каждый модуль имеет:

```text
Repository Interface

↓

Repository Implementation
```

Service использует только интерфейс.

---

# Unit of Work

Все изменения выполняются внутри одной транзакции.

```text
begin()

↓

Repository

↓

Repository

↓

commit()
```

При ошибке:

```text
rollback()
```

---

# Domain Events

Все значимые изменения сопровождаются событиями.

Примеры:

```text
CustomerCreated

OrderCreated

OrderClosed

VerificationCompleted

RepairCompleted

WarehouseStockChanged
```

---

# CQRS

Используется облегченная реализация.

Команды:

```text
CreateCustomerCommand

UpdateCustomerCommand

CreateOrderCommand
```

Запросы:

```text
GetCustomerQuery

GetOrderQuery
```

---

# Dependency Injection

Все зависимости внедряются извне.

Запрещено:

```python
service = CustomerService()
```

Разрешено:

```python
Depends(customer_service_factory)
```

---

# ORM

SQLAlchemy используется только в Infrastructure.

Domain ничего не знает о:

- Session;
- relationship();
- ForeignKey;
- mapped_column();
- select().

---

# Работа с базой

Все обращения к PostgreSQL проходят путь:

```text
Service

↓

Repository

↓

CRUD

↓

SQLAlchemy

↓

Database
```

Прямые обращения запрещены.

---

# Архивирование

Физическое удаление данных запрещено.

Используется:

```text
archived = True
```

Во всех основных сущностях.

---

# Тестирование

Минимальный набор тестов:

## Domain

Unit Tests.

## Application

Service Tests.

## Infrastructure

Integration Tests.

## API

HTTP Tests.

---

# Именование

Repository:

```text
CustomerRepository

OrderRepository

RepairRepository
```

Service:

```text
CustomerService

OrderService

RepairService
```

Commands:

```text
CreateCustomerCommand

UpdateCustomerCommand
```

Queries:

```text
GetCustomerQuery
```

Events:

```text
CustomerCreated

OrderClosed
```

Exceptions:

```text
CustomerNotFound

OrderClosed

InvalidOrderStatus
```

---

# Бизнес-логика

Допускается только в:

- Domain;
- Application.

Запрещается размещать бизнес-логику в:

- Router;
- Repository;
- CRUD;
- SQLAlchemy Model.

---

# Кодирование

Все новые модули должны:

- соответствовать DDD;
- соответствовать Clean Architecture;
- использовать BaseRepository;
- использовать BaseRouter;
- использовать Application Service;
- использовать Unit of Work;
- использовать Dependency Injection.

---

# Контроль качества

Перед объединением изменений проверяется:

- отсутствие бизнес-логики в API;
- отсутствие бизнес-логики в Repository;
- отсутствие SQLAlchemy в Domain;
- отсутствие CRUD в Service;
- прохождение тестов;
- прохождение Swagger;
- соответствие настоящему документу.

---

# Архитектурное правило проекта

Любой новый код должен вписываться в существующую архитектуру проекта.

Изменение архитектурных принципов допускается только путем внесения изменений в настоящий документ.

Настоящий документ является архитектурной конституцией проекта «Сфера».

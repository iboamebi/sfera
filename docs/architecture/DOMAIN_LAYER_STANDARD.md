# Domain Layer Standard

## Версия

v1.0

## Назначение

Настоящий документ определяет единый стандарт реализации Domain Layer проекта «Сфера».

Domain Layer является ядром системы и содержит исключительно предметную область.

---

# Место в архитектуре

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

==========================
       DOMAIN LAYER
==========================

 │

 ▼

Repository Interface

 │

 ▼

Infrastructure

 │

 ▼

PostgreSQL
```

---

# Назначение Domain Layer

Domain Layer отвечает только за предметную область.

В Domain находятся:

- сущности (Entities);
- агрегаты (Aggregates);
- Value Objects;
- Domain Services;
- Domain Events;
- Domain Exceptions;
- бизнес-инварианты.

---

# Domain запрещено

Domain не знает о существовании:

- FastAPI;
- SQLAlchemy;
- PostgreSQL;
- Repository;
- CRUD;
- HTTP;
- JSON;
- Pydantic.

Domain полностью независим от инфраструктуры.

---

# Структура каталога

```text
app/

└── domain/

    ├── customer/

    │   ├── entity.py

    │   ├── events.py

    │   ├── exceptions.py

    │   ├── services.py

    │   └── value_objects.py

    │

    ├── order/

    ├── repair/

    ├── verification/

    └── ...
```

---

# Entity

Entity обладает собственной идентичностью.

Пример:

```text
Customer

Order

Repair

Verification

Warehouse
```

Entity может изменять собственное состояние только через свои методы.

---

# Aggregate

Aggregate объединяет связанные Entity.

Пример:

```text
Order

 ├── OrderItem

 ├── Diagnostic

 ├── Repair

 └── Verification
```

Изменение внутренних объектов Aggregate выполняется только через корневую сущность.

---

# Value Object

Value Object не имеет собственного идентификатора.

Примеры:

```text
Address

PhoneNumber

Email

Money

SerialNumber

VerificationPeriod
```

Value Object является неизменяемым (Immutable).

---

# Domain Service

Используется, если операция не принадлежит одной Entity.

Примеры:

```text
VerificationCalculationService

RepairCostService

WarehouseReservationService
```

Domain Service не использует Repository.

---

# Domain Events

Каждое значимое изменение сопровождается событием.

Примеры:

```text
CustomerCreated

CustomerArchived

OrderCreated

OrderClosed

VerificationCompleted

RepairCompleted

WarehouseStockChanged
```

---

# Domain Exceptions

Все бизнес-ошибки находятся в Domain.

Пример:

```text
CustomerAlreadyExists

CustomerArchived

OrderClosed

InvalidOrderStatus

RepairAlreadyCompleted

VerificationExpired
```

---

# Инварианты

Каждая Entity самостоятельно защищает свои правила.

Например:

Order:

```text
Закрытый заказ нельзя изменить.
```

Customer:

```text
Архивированный клиент не может использоваться в новых заказах.
```

Warehouse:

```text
Остаток не может стать отрицательным.
```

---

# Repository Interface

В Domain размещаются только интерфейсы Repository.

Пример:

```python
class OrderRepository:

    def get(self, id):
        ...

    def save(self, order):
        ...
```

Реализация находится в Infrastructure.

---

# Dependency Rule

Разрешённые зависимости:

```text
Application

↓

Domain
```

Запрещённые зависимости:

```text
Domain

↓

Infrastructure
```

Domain никогда не импортирует Infrastructure.

---

# ORM

Domain не содержит:

- mapped_column;
- relationship;
- ForeignKey;
- Session;
- select();
- SQLAlchemy.

ORM полностью изолирована в Infrastructure.

---

# Тестирование

Domain тестируется отдельно.

Используются обычные unit-тесты без базы данных.

Проверяются:

- бизнес-правила;
- инварианты;
- события;
- исключения;
- изменение состояния Entity.

---

# Контроль качества

Domain соответствует архитектуре, если:

- не использует SQLAlchemy;
- не использует FastAPI;
- не использует Pydantic;
- не использует CRUD;
- не использует Repository реализации;
- содержит только предметную область.

---

# Итоговый стандарт

Domain Layer является наиболее стабильной частью проекта.

Изменения в Infrastructure, API или базе данных не должны требовать изменений Domain Layer.

Именно Domain определяет поведение системы, а остальные слои лишь обеспечивают его выполнение.

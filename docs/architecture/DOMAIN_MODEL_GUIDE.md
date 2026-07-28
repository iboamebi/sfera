# Domain Model Guide

## Проект

Сфера

## Версия

1.0

## Статус

Утверждено

---

# Назначение

Настоящий документ определяет правила проектирования предметной области (Domain Model) проекта «Сфера».

Все бизнес-сущности создаются в соответствии с данным документом.

---

# Основной принцип

Domain описывает исключительно бизнес.

Domain не зависит от:

- FastAPI;
- SQLAlchemy;
- PostgreSQL;
- HTTP;
- JSON;
- Pydantic;
- Alembic.

---

# Состав Domain

Каждый модуль предметной области может содержать:

```text
Entity

Aggregate

Value Object

Repository Interface

Domain Service

Factory

Specification

Policy

Event

Exception
```

---

# Entity

Entity обладает собственной идентичностью.

Примеры:

```text
Customer

Order

OrderItem

Repair

Verification

Warehouse

Material

Document
```

Entity может изменять состояние в течение жизненного цикла.

---

# Aggregate

Aggregate объединяет связанные сущности и определяет границу транзакции.

Основные агрегаты проекта:

```text
Order

Customer

Warehouse

PriceList
```

Изменение внутренних объектов выполняется только через Aggregate Root.

---

# Aggregate Root

Aggregate Root является единственной точкой доступа к агрегату.

Например:

```text
Order

↓

OrderItem

↓

Verification

↓

Repair
```

Внешний код работает только с `Order`.

---

# Value Object

Value Object:

- не имеет собственного идентификатора;
- неизменяем;
- сравнивается по значениям.

Примеры:

```text
Money

PhoneNumber

Email

Address

SerialNumber

VerificationResult

MeasurementRange
```

---

# Repository Interface

Domain содержит только интерфейс.

Пример:

```python
class CustomerRepository:
    ...
```

SQLAlchemy здесь запрещён.

---

# Domain Service

Используется, если логика:

- относится к нескольким Entity;
- не принадлежит одной сущности;
- является бизнес-операцией.

Примеры:

```text
RepairCostCalculator

VerificationDecisionService

WarehouseReservationService
```

---

# Factory

Factory создаёт сложные объекты.

Используется если:

- много обязательных параметров;
- требуется проверка;
- требуется построение агрегата.

---

# Specification

Используется для описания бизнес-условий.

Например:

```text
CanCloseOrder

CanArchiveCustomer

CanCompleteRepair
```

---

# Policy

Policy определяет правило бизнеса.

Например:

```text
DiscountPolicy

WarrantyPolicy

VerificationPolicy
```

---

# Domain Event

Каждое важное изменение сопровождается событием.

Примеры:

```text
OrderCreated

OrderClosed

RepairStarted

RepairCompleted

VerificationCompleted

MaterialWrittenOff
```

---

# Domain Exception

Domain использует собственные исключения.

Примеры:

```text
InvalidOrderStatus

CustomerArchived

WarehouseOverflow

RepairAlreadyCompleted

VerificationExpired
```

---

# Инварианты

Каждая Entity обязана самостоятельно защищать своё корректное состояние.

Например:

```text
Нельзя закрыть уже закрытый заказ.

Нельзя завершить ремонт без диагностики.

Нельзя провести поверку архивированного прибора.
```

---

# Бизнес-методы

Entity содержит методы предметной области.

Хорошо:

```python
order.close()

repair.complete()

verification.reject()

warehouse.reserve()
```

Плохо:

```python
order.status = CLOSED
```

---

# Работа с состоянием

Изменение состояния допускается только через методы Entity.

Прямое изменение полей запрещено.

---

# Правило зависимостей

Domain может зависеть только от:

- собственного кода;
- стандартной библиотеки Python.

Импорт SQLAlchemy запрещён.

---

# Работа с временем

Domain не должен самостоятельно получать текущее время.

Время передаётся извне.

Пример:

```python
verification.complete(completed_at)
```

---

# Работа с UUID

Создание идентификатора допускается:

- через Factory;
- через Application Service.

Entity не должна самостоятельно обращаться к инфраструктуре.

---

# Работа с коллекциями

Коллекции внутри Aggregate изменяются только его методами.

Например:

```python
order.add_item()

order.remove_item()
```

---

# Правило одной ответственности

Каждая Entity отвечает только за собственные бизнес-правила.

---

# Правило отсутствия ORM

В Domain запрещены:

```python
relationship()

ForeignKey

mapped_column()

Session

select()

update()
```

---

# Проверка модели

Перед созданием новой Entity необходимо ответить:

1. Это действительно бизнес-сущность?
2. Есть ли собственная идентичность?
3. Какие инварианты необходимо защищать?
4. Какие события возникают?
5. Это Aggregate или часть Aggregate?
6. Какие Value Object используются?

---

# Итог

Domain является самым стабильным слоем проекта.

Любое изменение Domain должно происходить только после анализа бизнес-процесса.

Все остальные слои адаптируются к Domain, а не наоборот.

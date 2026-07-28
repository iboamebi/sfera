# Naming Conventions

## Проект

Сфера

## Версия

1.0

## Статус

Утверждено

---

# Назначение

Настоящий документ определяет единые правила именования объектов проекта «Сфера».

Все новые сущности, файлы, классы и методы должны соответствовать данным правилам.

---

# Общие правила

Используются:

- PascalCase — классы;
- snake_case — файлы, функции, переменные;
- UPPER_CASE — константы.

---

# Каталоги

Используется только snake_case.

Пример:

```text
customer
order
order_item
warehouse
warehouse_stock
price_list
price_list_item
verification
repair
diagnostic
```

---

# Файлы

Используется snake_case.

Пример:

```text
customer_service.py
customer_repository.py
customer_router.py
customer_factory.py
customer_crud.py
```

---

# Классы

Используется PascalCase.

Пример:

```python
Customer
Order
OrderItem
Repair
Verification
Warehouse
```

---

# Service

Именование:

```text
<Entity>NameService
```

Пример:

```python
CustomerService
OrderService
RepairService
VerificationService
WarehouseService
```

---

# Repository

Именование:

```text
<Entity>NameRepository
```

Пример:

```python
CustomerRepository
OrderRepository
RepairRepository
WarehouseRepository
```

---

# CRUD

Именование:

```text
<Entity>NameCRUD
```

Пример:

```python
CustomerCRUD
OrderCRUD
WarehouseCRUD
```

---

# Router

Именование:

```text
<Entity>NameRouter
```

или использование BaseRouter.

Пример:

```python
customer_router

order_router
```

---

# Factory

Именование:

```text
<Entity>NameFactory
```

Пример:

```python
CustomerFactory
RepairFactory
VerificationFactory
```

---

# Commands

Именование:

```text
Create<Entity>

Update<Entity>

Delete<Entity>

Archive<Entity>
```

Пример:

```python
CreateCustomer

UpdateOrder

ArchiveMaterial
```

---

# Queries

Именование:

```text
Get<Entity>

List<Entities>

Find<Entity>
```

Пример:

```python
GetCustomer

ListOrders

FindRepair
```

---

# Events

Прошедшее время.

Пример:

```python
CustomerCreated

CustomerArchived

OrderCreated

OrderClosed

RepairCompleted

VerificationCompleted

MaterialWrittenOff
```

---

# Exceptions

Начинаются с имени сущности.

Пример:

```python
CustomerNotFound

CustomerAlreadyExists

OrderClosed

InvalidOrderStatus

WarehouseOverflow

RepairAlreadyCompleted
```

---

# DTO

Используются следующие суффиксы.

Создание:

```python
CustomerCreate
```

Обновление:

```python
CustomerUpdate
```

Чтение:

```python
CustomerRead
```

Список:

```python
CustomerList
```

---

# Переменные

Используется snake_case.

Пример:

```python
customer

customer_id

order

order_item

verification

repair

warehouse_stock
```

---

# Идентификаторы

Используется суффикс `_id`.

Пример:

```python
customer_id

order_id

repair_id

verification_id

warehouse_id
```

---

# Булевы значения

Используются префиксы:

```python
is_

has_

can_
```

Пример:

```python
is_archived

is_completed

has_items

can_close
```

---

# Коллекции

Используется множественное число.

Пример:

```python
customers

orders

materials

warehouse_stocks
```

---

# Константы

Используется UPPER_CASE.

Пример:

```python
DEFAULT_PAGE_SIZE

MAX_FILE_SIZE

API_VERSION

DEFAULT_TIMEOUT
```

---

# Перечисления

Используется PascalCase.

Элементы перечисления — UPPER_CASE.

Пример:

```python
class OrderStatus(Enum):

    NEW

    IN_PROGRESS

    COMPLETED

    CLOSED
```

---

# Relationship SQLAlchemy

Имя relationship совпадает с именем сущности.

Один объект:

```python
customer

order

warehouse
```

Коллекция:

```python
orders

documents

materials

verifications
```

---

# Таблицы

Используется snake_case во множественном числе.

Пример:

```text
customers

orders

order_items

repairs

verifications

warehouses

warehouse_stocks
```

---

# Foreign Key

Используется шаблон:

```python
customer_id

order_id

warehouse_id
```

---

# API

URL всегда во множественном числе.

Пример:

```text
/customers

/orders

/order-items

/repairs

/verifications

/warehouses
```

---

# Тесты

Имена файлов:

```text
test_customer_service.py

test_order_repository.py

test_verification.py
```

Функции:

```python
test_create_customer()

test_archive_order()

test_complete_repair()
```

---

# Запрещено

Не использовать:

```text
data

temp

obj

item1

test123

new_data

value1
```

Имена должны отражать назначение объекта.

---

# Итог

Единые правила именования обеспечивают:

- читаемость кода;
- единообразие проекта;
- удобство поиска;
- простоту сопровождения;
- соответствие архитектурным стандартам проекта «Сфера».

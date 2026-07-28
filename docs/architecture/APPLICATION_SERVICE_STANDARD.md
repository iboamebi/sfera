# Application Service Standard

## Версия

v1.0

## Назначение

Настоящий документ определяет единый стандарт реализации слоя Application Services проекта «Сфера».

Application Service является центральным слоем прикладной логики системы.

---

# Место в архитектуре

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

Repository

      │

      ▼

CRUD

      │

      ▼

SQLAlchemy

      │

      ▼

PostgreSQL
```

---

# Ответственность Application Service

Application Service отвечает за:

- выполнение пользовательского сценария;
- координацию нескольких Repository;
- применение бизнес-правил;
- управление жизненным циклом объектов;
- запуск Domain Events;
- управление транзакциями;
- работу через Unit of Work.

---

# Application Service запрещено

Application Service не должен:

- выполнять SQL-запросы;
- использовать SQLAlchemy Session;
- обращаться к CRUD;
- знать о FastAPI;
- возвращать HTTP Response;
- формировать JSON.

---

# Структура

Каждый модуль содержит собственный Service.

Пример:

```text
app/

├── application/

│   ├── customer/

│   │   └── service.py

│   ├── order/

│   │   └── service.py

│   ├── repair/

│   │   └── service.py

│   └── ...
```

---

# Зависимости

Service получает зависимости через конструктор.

Пример:

```python
class OrderService:

    def __init__(
        self,
        order_repository,
        customer_repository,
        warehouse_repository,
        unit_of_work,
    ):
        ...
```

Service никогда самостоятельно не создает Repository.

---

# Repository

Service работает только через Repository.

```text
Service

   │

   ▼

Repository
```

CRUD напрямую использовать запрещено.

---

# Unit of Work

Все операции изменения данных выполняются внутри Unit of Work.

Пример:

```text
begin()

↓

Repository.save()

↓

Repository.save()

↓

commit()
```

При ошибке:

```text
rollback()
```

---

# Domain Events

После успешной операции Service публикует события.

Пример:

```text
OrderCreated

CustomerCreated

VerificationCompleted

RepairCompleted

WarehouseStockChanged
```

---

# Бизнес-правила

Все проверки находятся исключительно в Service.

Например:

```text
Можно ли закрыть заказ?

Можно ли архивировать клиента?

Можно ли выполнить экспорт?

Достаточно ли материалов?

Можно ли изменить статус?
```

Repository подобных решений принимать не должен.

---

# Работа с несколькими Repository

Допустимый пример:

```text
OrderService

    │

    ├── CustomerRepository

    ├── OrderRepository

    ├── WarehouseRepository

    └── RepairRepository
```

Service координирует работу нескольких источников данных.

---

# Исключения

Service выбрасывает только доменные исключения.

Например:

```text
CustomerAlreadyExists

OrderClosed

InvalidOrderStatus

InsufficientStock

VerificationExportError
```

---

# Возвращаемые объекты

Service возвращает:

- Domain Entity;
- Aggregate;
- DTO;
- коллекции объектов.

Service не возвращает HTTP Response.

---

# Команды

Все изменения выполняются через Commands.

Пример:

```text
CreateCustomerCommand

UpdateCustomerCommand

ArchiveCustomerCommand

CreateOrderCommand

CloseOrderCommand
```

---

# Запросы

Операции чтения оформляются отдельными Query.

Пример:

```text
GetCustomerQuery

GetOrderQuery

GetVerificationQuery
```

---

# Структура каталога

```text
app/

└── application/

    └── order/

        ├── service.py

        ├── commands/

        │   ├── create_order.py

        │   ├── close_order.py

        │   └── ...

        └── queries/

            ├── get_order.py

            └── ...
```

---

# Тестирование

Каждый Service покрывается модульными тестами.

Минимально проверяются:

- успешное выполнение сценария;
- ошибки бизнес-логики;
- работа нескольких Repository;
- публикация событий;
- корректная работа Unit of Work.

---

# Контроль качества

Application Service считается соответствующим архитектуре, если:

- не использует SQLAlchemy;
- не использует CRUD;
- работает через Repository;
- содержит всю прикладную логику;
- использует Unit of Work;
- использует Domain Events;
- покрыт тестами.

---

# Итоговый стандарт

Application Service является единственным местом размещения прикладной бизнес-логики проекта «Сфера».

Все пользовательские сценарии проходят исключительно через слой Application Services.

Любое размещение бизнес-логики в Router, Repository или CRUD считается нарушением архитектурного стандарта проекта.

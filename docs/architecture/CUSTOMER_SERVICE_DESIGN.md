# Customer Service Design

## Этап

Application Service Layer v1.0

## Модуль

Customer

---

# Назначение

`CustomerService` отвечает за сценарии работы с заказчиками.

Модуль не работает напрямую с SQLAlchemy.

Ответственность:

- управление жизненным циклом клиента;
- бизнес-проверки;
- вызов Repository;
- подготовка данных для API.

---

# Архитектура

```text
CustomerRouter
        |
        v
CustomerService
        |
        v
CustomerRepository
        |
        v
CustomerCRUD
        |
        v
PostgreSQL
```

---

# Структура проекта

```text
app/
├── application/
│   └── customer/
│       ├── service.py
│       ├── commands/
│       │   ├── create_customer.py
│       │   ├── update_customer.py
│       │   └── archive_customer.py
│       └── queries/
│           └── get_customer.py
│
├── domain/
│   └── customer/
│       ├── entity.py
│       ├── exceptions.py
│       └── events.py
│
├── infrastructure/
│   └── customer/
│       └── customer_repository.py
│
└── api/
    └── routers/
        └── customer.py
```

---

# Команды

## CreateCustomerCommand

Назначение:

Создание нового клиента.

Поля:

```python
name: str
organization_id: UUID
contact_person: str | None
phone: str | None
email: str | None
discount_percent: Decimal
```

---

## UpdateCustomerCommand

Назначение:

Изменение информации о клиенте.

Поля:

```python
customer_id: UUID
name: str
contact_person: str | None
phone: str | None
email: str | None
discount_percent: Decimal
```

---

## ArchiveCustomerCommand

Назначение:

Архивирование клиента.

Поля:

```python
customer_id: UUID
```

---

# Интерфейс CustomerService

```python
class CustomerService:

    def create(self, command):
        ...

    def update(self, command):
        ...

    def archive(self, command):
        ...

    def get(self, customer_id):
        ...

    def get_all(self):
        ...
```

---

# Бизнес-правила

## Создание клиента

Проверки:

- имя обязательно;
- организация должна существовать;
- запрещено создание клиента с одинаковым названием в одной организации.

---

## Изменение клиента

Проверки:

- клиент существует;
- клиент не архивирован.

---

## Архивация клиента

Правила:

- физическое удаление запрещено;
- используется поле `archived`;
- архивированный клиент недоступен для новых заказов.

---

# Domain Events

Используются события:

```text
CustomerCreated
CustomerUpdated
CustomerArchived
```

---

# Исключения домена

Файл:

```text
app/domain/customer/exceptions.py
```

Исключения:

```python
CustomerNotFound
CustomerAlreadyExists
CustomerArchived
OrganizationNotFound
```

---

# Контракт Repository

```python
class CustomerRepository:

    def get(self, customer_id):
        ...

    def get_all(self):
        ...

    def save(self, customer):
        ...

    def exists_by_name(self, organization_id, name):
        ...

    def archive(self, customer):
        ...
```

---

# Изменения API

До рефакторинга:

```text
Router
  |
  v
CRUD
```

После рефакторинга:

```text
Router
  |
  v
CustomerService
  |
  v
CustomerRepository
  |
  v
CustomerCRUD
```

---

# Unit of Work

Все операции изменения данных должны выполняться в рамках одной транзакции.

Пример:

```text
CustomerService
        |
        v
UnitOfWork
        |
        +--> CustomerRepository
        |
        +--> OrganizationRepository
```

---

# Покрытие тестами

Создать:

```text
tests/application/customer/test_customer_service.py
```

Минимальный набор тестов:

- создание клиента;
- отказ при создании дубликата;
- изменение клиента;
- архивирование клиента;
- получение клиента;
- получение списка клиентов.

---

# Критерий завершения

Модуль Customer считается полностью переведённым на Application Service Layer при выполнении условий:

- Router не обращается к CRUD напрямую;
- вся бизнес-логика находится в CustomerService;
- Repository используется только как слой доступа к данным;
- CRUD содержит только операции работы с БД;
- сервис покрыт модульными тестами;
- все REST API проходят проверку в Swagger.

# API. Правила разработки

Версия: 1.1

---

# Общие принципы

Backend реализован на:

- FastAPI
- SQLAlchemy 2.0
- Pydantic
- PostgreSQL

Архитектура API соответствует REST.

---

# Структура

```
app/
├── api/
│   └── routers/
├── crud/
├── schemas/
├── services/
├── models/
├── db/
└── core/
```

---

# URL

Используются существительные.

Правильно:

```
/customers
/orders
/order-items
/verifications
/repairs
/materials
```

Неправильно:

```
/createOrder
/getCustomer
/deleteRepair
```

---

# HTTP методы

Получение списка

```
GET
```

Получение объекта

```
GET /{id}
```

Создание

```
POST
```

Изменение

```
PUT
```

Частичное изменение

```
PATCH
```

Удаление

```
DELETE
```

---

# UUID

Все идентификаторы имеют тип UUID.

Пример:

```
GET /orders/{id}
```

---

# Ответы

Успешные запросы

```
200 OK
201 Created
204 No Content
```

Ошибки

```
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
422 Validation Error
500 Internal Server Error
```

---

# Pydantic

Для каждой сущности создаются схемы:

```
Create
Update
Read
```

Например

```
CustomerCreate
CustomerUpdate
CustomerRead
```

---

# CRUD

Для всех справочников используется BaseCRUD.

Специализированная логика выносится в Service.

---

# Router

Используется BaseRouter.

Индивидуальные маршруты добавляются отдельно.

---

# Валидация

Валидация выполняется:

- Pydantic;
- сервисами;
- доменными объектами.

---

# Логика

Router не содержит бизнес-логики.

Router выполняет только:

- получение запроса;
- вызов сервиса;
- возврат ответа.

---

# Транзакции

Изменения данных выполняются через Unit of Work.

---

# Ошибки

Используются HTTPException.

Пример

```
404

Заказ не найден.
```

---

# Swagger

Каждый маршрут должен иметь:

- описание;
- response_model;
- теги;
- корректные коды ответов.

---

# Именование

Router

```
customer.py
order.py
verification.py
```

CRUD

```
customer.py
order.py
verification.py
```

Schema

```
customer.py
order.py
verification.py
```

---

# Новые модули

Каждый новый модуль должен содержать:

```
Model
Schema
CRUD
Service
Router
Tests
Migration
```

---

# Запрещается

Запрещено:

- SQL внутри Router;
- бизнес-логика внутри Router;
- прямой доступ к БД из схем;
- дублирование CRUD;
- изменение моделей без миграции Alembic.

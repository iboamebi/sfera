# API Layer Standard

## Версия

v1.0

## Назначение

Настоящий документ определяет единый стандарт реализации REST API проекта «Сфера».

API Layer является внешним интерфейсом системы и отвечает исключительно за взаимодействие с клиентами по протоколу HTTP.

---

# Место в архитектуре

```text
HTTP Request

      │

      ▼

==================
    API LAYER
==================

      │

      ▼

Application Service

      │

      ▼

Domain

      │

      ▼

Infrastructure

      │

      ▼

PostgreSQL
```

---

# Ответственность API Layer

API отвечает только за:

- прием HTTP-запросов;
- проверку структуры входных данных;
- преобразование DTO;
- вызов Application Service;
- возврат HTTP-ответа;
- преобразование исключений в HTTP-коды.

---

# API запрещено

API Layer запрещается:

- обращаться к SQLAlchemy;
- использовать Session;
- обращаться к CRUD;
- обращаться к Repository;
- выполнять бизнес-проверки;
- изменять Domain Entity;
- выполнять вычисления;
- работать с транзакциями.

---

# Структура проекта

```text
app/

└── api/

    ├── routers/

    │   ├── customer.py

    │   ├── order.py

    │   ├── repair.py

    │   ├── verification.py

    │   └── ...

    │

    ├── dependencies.py

    ├── exception_handlers.py

    └── base_router.py
```

---

# BaseRouter

Все Router создаются через единый BaseRouter.

Пример:

```python
router = BaseRouter(
    service_factory=customer_service_factory,
    read_schema=CustomerRead,
    create_schema=CustomerCreate,
    update_schema=CustomerUpdate,
    prefix="/customers",
    tags=["Customers"],
).router
```

CRUD в Router использовать запрещено.

---

# DTO

API работает только через схемы.

Используются:

```text
Create

Update

Read

List

Response
```

DTO располагаются:

```text
app/schemas/
```

---

# Dependency Injection

Service передается через Dependency Injection.

Пример:

```python
Depends(customer_service_factory)
```

Router не создает Service самостоятельно.

---

# HTTP-коды

Используются стандартные ответы.

```text
200 OK

201 Created

204 No Content

400 Bad Request

401 Unauthorized

403 Forbidden

404 Not Found

409 Conflict

422 Validation Error

500 Internal Server Error
```

---

# Исключения

Domain Exceptions преобразуются в HTTP.

Пример:

```text
CustomerNotFound

↓

404
```

```text
CustomerAlreadyExists

↓

409
```

Все преобразования выполняются централизованно.

---

# Swagger

Каждый Router обязан автоматически документироваться.

Требования:

- описание;
- теги;
- модели запросов;
- модели ответов;
- примеры.

---

# Версионирование

При необходимости используется:

```text
/api/v1/

/api/v2/
```

Текущая версия:

```text
v1
```

---

# Формат ответа

Все успешные ответы используют единый формат.

Пример:

```json
{
    "id": "...",
    "name": "...",
    "created_at": "...",
    "updated_at": "..."
}
```

Ошибки:

```json
{
    "detail": "Customer not found."
}
```

---

# Аутентификация

API поддерживает подключение:

```text
JWT

OAuth2

API Key
```

Реализация располагается только в API Layer.

---

# Логирование

API может логировать:

- HTTP Method;
- URL;
- время выполнения;
- статус ответа.

Логирование бизнес-событий запрещено.

---

# Тестирование

Проверяются:

- HTTP-коды;
- сериализация;
- валидация;
- Swagger;
- преобразование исключений.

Бизнес-логика в API не тестируется.

---

# Контроль качества

API соответствует архитектуре, если:

- использует только Application Service;
- не знает о Repository;
- не знает о CRUD;
- не знает о SQLAlchemy;
- не содержит бизнес-логики;
- автоматически документируется через Swagger.

---

# Итоговый стандарт

API Layer является исключительно транспортным слоем системы.

Его задача — принять HTTP-запрос, передать выполнение Application Service и вернуть корректный HTTP-ответ.

Любая бизнес-логика в Router считается нарушением архитектурного стандарта проекта «Сфера».

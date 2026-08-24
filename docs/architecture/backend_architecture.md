# Архитектура Backend

Версия: 1.1

---

# Общая структура

```
app/
│
├── api/
├── application/
├── crud/
├── db/
├── domains/
├── infrastructure/
├── models/
├── schemas/
├── services/
├── shared/
├── utils/
└── main.py
```

---

# api/

REST API приложения.

Содержит:

- routers
- зависимости
- регистрацию маршрутов

Каждая сущность имеет собственный router.

Пример:

```
api/
    routers/
        customer.py
        order.py
        verification.py
```

---

# application/

Слой сценариев использования (Use Cases).

Содержит:

- команды
- обработчики
- сервисы приложения

Не работает напрямую с SQLAlchemy.

Использует Repository и Unit of Work.

---

# crud/

Универсальные CRUD.

Основаны на BaseCRUD.

Используются простыми REST-операциями.

---

# db/

Работа с базой данных.

Содержит:

- engine
- session
- Base
- зависимости FastAPI

---

# domains/

Предметная область.

Содержит:

- агрегаты
- сущности
- доменные сервисы
- события
- value objects

Domain ничего не знает о FastAPI и SQLAlchemy.

---

# infrastructure/

Реализация инфраструктуры.

Содержит:

- SQLAlchemy Repository
- Unit of Work
- адаптеры
- интеграции

---

# models/

ORM-модели SQLAlchemy.

Каждая модель соответствует таблице PostgreSQL.

Все модели наследуются от BaseModel.

---

# schemas/

Pydantic-схемы.

Используются для:

- запросов
- ответов
- валидации

---

# services/

Прикладные сервисы.

Используются в случаях, когда логика не относится к одному агрегату.

---

# shared/

Общие компоненты.

Содержит:

- BaseAggregate
- Repository
- Domain Events
- Event Dispatcher
- общие исключения

---

# utils/

Вспомогательные функции.

Не содержит бизнес-логики.

---

# main.py

Точка входа FastAPI.

Отвечает за:

- создание приложения;
- регистрацию роутеров;
- middleware;
- обработчики исключений.

---

# Правила зависимостей

```
API
    ↓
Application
    ↓
Domain
    ↑
Infrastructure
```

Разрешены зависимости только сверху вниз.

Infrastructure реализует интерфейсы Domain.

---

# Работа с БД

```
Router
    ↓
Service
    ↓
Repository
    ↓
SQLAlchemy
    ↓
PostgreSQL
```

---

# Работа с агрегатами

```
Router
    ↓
Application Service
    ↓
UnitOfWork
    ↓
Repository
    ↓
Aggregate
```

---

# Общие правила

- SQLAlchemy используется только в Infrastructure и Models.
- Domain не импортирует SQLAlchemy.
- API не содержит бизнес-логики.
- Repository не содержит HTTP-кода.
- Все изменения агрегатов выполняются через Unit of Work.
- Все изменения структуры базы данных выполняются только через Alembic.

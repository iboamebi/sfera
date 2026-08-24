# Структура проекта «Сфера»

**Версия:** 1.1
**Дата актуализации:** 2026-07-16

---

# 1. Назначение

Документ описывает организацию каталогов проекта и правила размещения кода.

Структура соответствует принципам:

- DDD;
- Clean Architecture;
- разделения ответственности.

---

# 2. Общая структура

```text
backend/

├── alembic/
├── app/
├── docs/
├── tests/
├── requirements.txt
├── alembic.ini
└── .env
```

---

# 3. Каталог alembic

```text
alembic/
```

Назначение:

- миграции базы данных;
- история изменений схемы;
- настройка Alembic.

Правило:

Изменения структуры БД выполняются только через миграции.

---

# 4. Каталог app

```text
app/
```

Основной исходный код приложения.

---

# 5. API Layer

```text
app/api/
```

Назначение:

HTTP интерфейс приложения.

Содержит:

```text
api/

├── routers/
├── dependencies/
├── middleware/
└── exceptions/
```

Ответственность:

- HTTP-запросы;
- валидация;
- сериализация;
- авторизация.

---

# 6. Application Layer

```text
app/application/
```

Назначение:

реализация сценариев использования.

Содержит:

```text
application/

├── services/
├── commands/
├── queries/
└── dto/
```

Ответственность:

- выполнение бизнес-сценариев;
- управление транзакциями;
- взаимодействие с доменом.

---

# 7. Domain Layer

```text
app/domains/
```

Назначение:

бизнес-модель системы.

Структура:

```text
domains/

├── order/
├── verification/
├── repair/
├── device/
├── warehouse/
└── shared/
```

Каждый домен может содержать:

```text
domain/

├── entities/
├── value_objects/
├── events/
├── services/
├── repositories/
└── factories/
```

---

# 8. Infrastructure Layer

```text
app/infrastructure/
```

Назначение:

технические реализации.

Содержит:

```text
infrastructure/

├── repositories/
├── sqlalchemy/
├── unit_of_work/
├── storage/
└── integrations/
```

---

# 9. ORM Models

```text
app/models/
```

Содержит SQLAlchemy модели.

Назначение:

- описание таблиц;
- связи;
- ограничения;
- индексы.

ORM-модель не является доменной сущностью.

---

# 10. Schemas

```text
app/schemas/
```

Содержит Pydantic модели.

Назначение:

- входные данные API;
- ответы API;
- валидация.

---

# 11. CRUD

```text
app/crud/
```

Содержит общие CRUD-операции.

Используется для стандартных операций без сложной бизнес-логики.

---

# 12. Database

```text
app/db/
```

Содержит:

- подключение к PostgreSQL;
- настройку сессий;
- конфигурацию базы данных.

---

# 13. Shared

```text
app/shared/
```

Общие компоненты:

- Aggregate;
- Repository interfaces;
- Domain Events;
- Exceptions;
- общие базовые классы.

---

# 14. Documentation

```text
docs/
```

Структура:

```text
docs/

├── architecture/
├── database/
├── api/
├── deployment/
└── modules/
```

---

# 15. Tests

```text
tests/
```

Структура:

```text
tests/

├── unit/
├── integration/
└── api/
```

---

# 16. Направление зависимостей

```text
API

↓

Application

↓

Domain

↓

Infrastructure
```

---

# 17. Правила размещения кода

Запрещается:

- размещать бизнес-логику в API;
- обращаться к БД из Domain;
- использовать ORM внутри Domain;
- создавать новые архитектурные слои без согласования.

---

# 18. Главный принцип

Структура проекта должна отражать бизнес-область системы, а не технические детали реализации.

# Infrastructure Layer

**Версия:** 1.1
**Дата актуализации:** 2026-07-16

---

# 1. Назначение

Infrastructure Layer содержит технические реализации проекта «Сфера».

Этот слой обеспечивает связь бизнес-логики с внешним миром:

- база данных;
- файловое хранилище;
- внешние сервисы;
- технические адаптеры.

---

# 2. Место в архитектуре

```text
API

↓

Application

↓

Domain

↓

Infrastructure

↓

External Systems
```

---

# 3. Ответственность Infrastructure

Infrastructure отвечает за:

- реализацию репозиториев;
- работу с PostgreSQL;
- работу SQLAlchemy;
- управление подключениями;
- Unit of Work;
- внешние интеграции;
- хранение файлов.

---

# 4. Расположение

```text
app/infrastructure/
```

---

# 5. Структура

```text
infrastructure/

├── repositories/
├── sqlalchemy/
├── unit_of_work/
├── storage/
└── integrations/
```

---

# 6. Репозитории

Infrastructure реализует интерфейсы, определённые в Domain.

Пример:

```text
Domain

OrderRepository

        ↓

Infrastructure

SQLAlchemyOrderRepository
```

---

# 7. Правила репозиториев

Репозиторий отвечает только за:

- получение данных;
- сохранение данных;
- поиск;
- удаление.

Репозиторий не содержит:

- бизнес-правил;
- переходов состояний;
- пользовательских сценариев.

---

# 8. SQLAlchemy

Используется для доступа к PostgreSQL.

Компоненты:

```text
Engine

Session

ORM Models

Repositories
```

---

# 9. ORM Models

ORM-модели находятся:

```text
app/models/
```

Они описывают:

- таблицы;
- связи;
- индексы;
- ограничения.

ORM-модель не является Domain Entity.

---

# 10. Unit Of Work

Используется для управления транзакциями.

Пример:

```text
Application Service

↓

Unit Of Work

↓

Repositories

↓

Database
```

---

# 11. Хранение файлов

Большие бинарные данные не хранятся в PostgreSQL.

Внешнее хранилище используется для:

- документов;
- фотографий;
- сканов;
- отчётов.

---

# 12. Внешние интеграции

Infrastructure содержит адаптеры внешних систем.

Примеры:

```text
Arshin Integration

Notification Service

Document Storage
```

---

# 13. Зависимости

Infrastructure может зависеть от:

- Domain;
- Application interfaces.

Domain не зависит от Infrastructure.

---

# 14. Запрещается

Infrastructure не должна:

- содержать бизнес-решения;
- изменять агрегаты напрямую;
- вызывать API Router;
- реализовывать пользовательские сценарии.

---

# 15. Тестирование

Infrastructure проверяется через:

- Integration Tests;
- тестовую PostgreSQL;
- проверку репозиториев;
- проверку внешних адаптеров.

---

# 16. Главный принцип

Infrastructure является заменяемым техническим слоем.

Изменение базы данных, хранилища или внешнего сервиса не должно менять бизнес-логику системы.

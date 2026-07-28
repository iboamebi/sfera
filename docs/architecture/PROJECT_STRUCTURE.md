# Project Structure

## Проект

Сфера

## Версия

1.0

## Статус

Утверждено

---

# Назначение

Настоящий документ определяет единую структуру каталогов проекта «Сфера».

Изменение структуры допускается только по архитектурному решению.

---

# Общая структура проекта

```text
sphere/

├── backend/
│
├── frontend/
│
├── docs/
│
├── scripts/
│
├── docker/
│
├── deployments/
│
├── tests/
│
└── README.md
```

---

# Backend

```text
backend/

├── alembic/
├── app/
├── tests/
├── requirements.txt
├── pyproject.toml
└── Dockerfile
```

---

# Структура app

```text
app/

├── api/
├── application/
├── domain/
├── infrastructure/
├── crud/
├── schemas/
├── models/
├── database/
├── core/
├── services/
├── utils/
└── main.py
```

---

# API

```text
api/

├── routers/
├── dependencies.py
├── exception_handlers.py
└── base_router.py
```

---

# Application

```text
application/

├── customer/
├── order/
├── repair/
├── verification/
├── warehouse/
├── document/
├── pricing/
└── base_service.py
```

Каждый модуль содержит:

```text
commands.py
queries.py
service.py
dto.py
```

---

# Domain

```text
domain/

├── customer/
├── order/
├── repair/
├── verification/
├── warehouse/
├── shared/
└── events/
```

Каждый модуль может содержать:

```text
entities.py
value_objects.py
services.py
repositories.py
events.py
exceptions.py
```

---

# Infrastructure

```text
infrastructure/

├── customer/
├── order/
├── repair/
├── verification/
├── warehouse/
├── document/
├── arshin/
├── storage/
├── events/
├── sqlalchemy_unit_of_work.py
└── base_repository.py
```

---

# CRUD

```text
crud/

├── base.py
├── customer.py
├── order.py
├── repair.py
├── verification.py
└── warehouse.py
```

CRUD содержит только операции работы с данными.

---

# Schemas

```text
schemas/

├── customer.py
├── order.py
├── repair.py
├── verification.py
└── warehouse.py
```

Каждый файл содержит:

- Create;
- Update;
- Read;
- List.

---

# Models

```text
models/

├── base_model.py
├── customer.py
├── order.py
├── order_item.py
├── repair.py
├── verification.py
├── warehouse.py
├── material.py
├── document.py
└── ...
```

Модели содержат только ORM-описание таблиц.

---

# Database

```text
database/

├── session.py
├── base.py
└── init_db.py
```

---

# Core

```text
core/

├── config.py
├── logging.py
├── security.py
├── exceptions.py
└── constants.py
```

---

# Utils

```text
utils/

├── datetime.py
├── validators.py
├── formatting.py
└── helpers.py
```

Используются только универсальные функции.

---

# Документация

```text
docs/

├── architecture/
├── api/
├── database/
├── deployment/
├── business/
└── user/
```

---

# Архитектурная документация

```text
docs/architecture/

PROJECT_CONSTITUTION.md

PROJECT_ARCHITECTURE_STANDARD.md

APPLICATION_SERVICE_STANDARD.md

DOMAIN_LAYER_STANDARD.md

REPOSITORY_LAYER_STANDARD.md

INFRASTRUCTURE_LAYER_STANDARD.md

API_LAYER_STANDARD.md

CODING_STANDARD.md

NAMING_CONVENTIONS.md

TESTING_STANDARD.md

GIT_WORKFLOW.md

PROJECT_STRUCTURE.md
```

---

# Тесты

```text
tests/

├── api/
├── application/
├── domain/
├── infrastructure/
├── fixtures/
├── factories/
└── conftest.py
```

---

# Скрипты

```text
scripts/

backup.sh

restore.sh

lint.sh

format.sh

run_tests.sh

build_docs.sh
```

---

# Docker

```text
docker/

docker-compose.yml

Dockerfile

postgres/

nginx/
```

---

# Deployment

```text
deployments/

production/

staging/

development/
```

---

# Правила размещения файлов

Каждый файл должен иметь единственное назначение.

Не допускается смешивание:

- бизнес-логики;
- инфраструктуры;
- HTTP;
- SQL;
- ORM;
- утилит.

---

# Добавление нового модуля

При создании нового модуля рекомендуется следующая структура:

```text
api/
application/
domain/
infrastructure/
crud/
schemas/
models/
tests/
```

Все уровни должны быть реализованы единообразно.

---

# Контроль структуры

Перед добавлением новых каталогов необходимо убедиться, что аналогичная структура отсутствует.

Дублирование каталогов и модулей запрещено.

---

# Итог

Единая структура проекта обеспечивает:

- предсказуемость расположения файлов;
- удобство сопровождения;
- простоту навигации;
- соответствие принципам DDD и Clean Architecture;
- единый подход к разработке всех модулей проекта «Сфера».

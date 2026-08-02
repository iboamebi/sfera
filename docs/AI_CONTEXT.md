# Sfera Project AI Context

## Назначение проекта

Сфера — информационная система сервисного центра и метрологической лаборатории.

Основное направление:

- учёт средств измерений (СИ);
- поверка средств измерений;
- ремонт;
- диагностика;
- технологические процессы;
- документы;
- склад;
- финансы;
- интеграция с ФГИС Аршин.

Ключевой бизнес-процесс:


Order
↓
Case
↓
Workflow
↓
Technological Card
↓
Verification / Repair / Diagnostic


Основная бизнес-ценность системы:

- управление жизненным циклом средств измерений;
- проведение поверок;
- фиксация результатов;
- подготовка документов;
- экспорт данных в ФГИС Аршин.

---

# Технологический стек

Backend:

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Docker / Docker Compose

Инструменты качества:

- pytest
- ruff
- pre-commit

Репозиторий:


GitHub:
iboamebi/sfera


Основная ветка:


develop


---

# Архитектура

Проект использует:


DDD + Clean Architecture


Целевая структура:


API
↓
Application Service
↓
Domain
↓
Repository Interface
↑
Infrastructure Repository
↓
Database


---

# Архитектурные правила

## Domain

Domain:

- содержит бизнес-правила;
- содержит Entity;
- содержит Aggregate Root;
- содержит Value Objects;
- содержит Domain Exceptions.

Запрещено:

- SQLAlchemy;
- ORM модели;
- Infrastructure зависимости;
- API зависимости.

---

## Application

Application:

- реализует Use Cases;
- содержит Application Services;
- принимает Commands;
- вызывает Repository Interfaces.

Запрещено:

- SQLAlchemy;
- Database Session;
- Infrastructure зависимости;
- API зависимости.

---

## Infrastructure

Infrastructure:

- содержит SQLAlchemy реализации;
- содержит ORM mapping;
- содержит Repository implementations.

Запрещено:

- зависеть от API;
- зависеть от Application.

---

## API

API:

- принимает HTTP запрос;
- валидирует входные данные через schemas;
- вызывает Application Services;
- обрабатывает Application Exceptions.

Запрещено:

- бизнес-логика;
- Repository вызовы;
- SQLAlchemy;
- прямой доступ к Database.

---

# Migration Status

## Sfera Architecture v2.0

Статус:

COMPLETED

Завершено:

- Project Constitution;
- Architecture Standards;
- Layer Standards;
- DDD migration;
- Legacy CRUD removal;
- Domain isolation;
- Application isolation;
- API isolation;
- Domain Exceptions Isolation;
- Architecture Dependency Audit.

---

# Миграция модулей

| Module | Status |
|---|---|
| Organization | COMPLETED |
| Customer | COMPLETED |
| Order | COMPLETED |
| Material | COMPLETED |
| Warehouse | COMPLETED |
| Verification | COMPLETED |
| Repair | COMPLETED |
| Diagnostic | COMPLETED |
| PriceList | COMPLETED |
| PriceListItem | COMPLETED |
| Device | COMPLETED |
| Workflow | COMPLETED |

---

# Legacy Layers

Статус:

REMOVED

Удалено:

- app/crud;
- app/services/price_list_service.py;
- app/api/base_router.py.

Проверено:

- нет активных импортов app.crud;
- нет активных импортов legacy services;
- нет использования BaseRouter.

---

# Dependency Audit

Проверено:

- API isolation;
- Application isolation;
- Domain isolation;
- Repository boundaries;
- Infrastructure dependency direction.

Результаты:


API
✓ no repositories

Application
✓ no Infrastructure
✓ no ORM

Domain
✓ no ORM
✓ no Infrastructure

Infrastructure
✓ no API
✓ no Application


---

# Exceptions Isolation

Статус:

COMPLETED

Выполнено:

- Domain-specific exceptions;
- Application-specific exceptions;
- удаление generic ValueError из migrated domain/application logic;
- разделение ошибок по слоям.

Модули Domain Exceptions:

- Device;
- Order;
- Verification;
- Warehouse.

---

# Validation

Последняя проверка:


pytest: 16 passed


Quality checks:


ruff check
ruff format
pre-commit


---

# Current Checkpoint

Branch:


develop


Baseline:


Sfera Architecture v2.0


Last checkpoint:


cf0ad1e docs: add architecture dependency audit checkpoint


Последние изменения:


cf0ad1e docs: add architecture dependency audit checkpoint
dbd38b9 docs: add domain exception isolation checkpoint
80a0923 refactor: isolate domain exceptions


Validation:


pytest: 16 passed
ruff: passed
pre-commit: passed


---

# Текущий этап развития

После завершения миграции начинается этап:


Architecture Stabilization
+
Business Feature Development


Следующие направления:

1. аудит Application Services;
2. аудит Repository Interfaces;
3. аудит Infrastructure Mappers;
4. автоматические architecture tests;
5. развитие бизнес-функций.

---

# Правила разработки новых функций

Новый функционал создаётся только через:


Application Service
↓
Repository Interface
↓
Infrastructure Repository
↓
Database


Не использовать:

- CRUD;
- прямой SQL из Application;
- бизнес-логику в API.

---

# Документация проекта

Основные документы:


docs/

AI_CONTEXT.md

MIGRATION_STATUS.md

architecture/
MIGRATION_MATRIX.md
PROJECT_CONSTITUTION.md
ARCHITECTURE.md


Перед началом работы читать:

1. AI_CONTEXT.md;
2. MIGRATION_STATUS.md;
3. соответствующий раздел архитектуры.

---

# Инструкция для AI

При подключении:

1. Восстановить состояние через GitHub.
2. Проверить текущий branch.
3. Проверить последний commit.
4. Проверить чистоту рабочего дерева.
5. Прочитать архитектурную документацию.

Не пересказывать документацию.

Сообщить только:

- восстановленный checkpoint;
- текущий статус;
- следующий логический этап.

---

# Правила работы с кодом

Перед изменениями:

- читать актуальный код из репозитория;
- проверять зависимости;
- определить текущий модуль;
- определить статус миграции модуля;
- проверить MIGRATION_MATRIX;
- проверить наличие legacy-кода;
- учитывать модели, схемы и миграции;
- не предполагать наличие файлов.

Работа:

1. анализ;
2. один файл;
3. полный код файла;
4. ожидание подтверждения перед следующим файлом.

При изменении файлов:

- не использовать diff как замену файла;
- не создавать новый код без анализа текущей структуры.

---

# После завершения логического этапа

Выполнить:


pytest
ruff check
ruff format --check
git status
commit
push origin develop


---

# Архитектурное ограничение

Не предлагать переписывание архитектуры.

Сохранять текущий:


Sfera Architecture v2.0
DDD + Clean Architecture baseline

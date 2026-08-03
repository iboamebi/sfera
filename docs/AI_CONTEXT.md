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

Основная бизнес-ценность системы:

- управление жизненным циклом средств измерений;
- проведение поверок;
- фиксация результатов;
- подготовка документов;
- экспорт данных в ФГИС Аршин.

---

# Ключевой бизнес-процесс

Order
↓
Case
↓
Workflow
↓
Technological Card
↓
Verification / Repair / Diagnostic

Текущие реализованные объекты:

Order;
Workflow;
Verification;
Repair;
Diagnostic.

Будущие доменные объекты:

Case;
Technological Card.

Статус:

PLANNED

Технологический стек

Backend:

Python 3.12;
FastAPI;
PostgreSQL;
SQLAlchemy;
Alembic;
Pydantic;
Docker / Docker Compose.

Инструменты качества:

pytest;
ruff;
pre-commit.

Репозиторий:

GitHub:
iboamebi/sfera

Основная рабочая ветка:

develop
Структура проекта

Основной backend:

backend/app/

api/
application/
domains/
infrastructure/
models/
schemas/
shared/

Назначение слоёв:

api
HTTP интерфейс

application
Use Cases

domains
Бизнес-правила

infrastructure
Persistence и внешние интеграции

models
SQLAlchemy ORM модели

schemas
Pydantic API схемы

shared
Общие компоненты
Архитектура

Проект использует:

DDD + Clean Architecture

Целевая структура:

API
↓
Application Service
↓
Domain Model
↓
Repository Interface
↑
Infrastructure Repository
↓
Database
Архитектурные правила
Domain

Domain содержит:

Entity;
Aggregate Root;
Value Objects;
Domain Services;
Domain Exceptions;
Repository Interfaces.

Разрешено:

бизнес-правила;
валидация доменных объектов;
изменение состояния сущностей.

Запрещено:

SQLAlchemy;
ORM модели;
Database Session;
Infrastructure зависимости;
API зависимости.
Application

Application содержит:

Use Cases;
Application Services;
Commands;
Application Exceptions.

Application:

управляет сценариями использования;
вызывает Domain;
работает через Repository Interfaces.

Application зависит только от Domain и Repository Interfaces.

Запрещено:

SQLAlchemy;
Database Session;
ORM модели;
Infrastructure Repository;
API зависимости.
Infrastructure

Infrastructure содержит:

SQLAlchemy Repository implementations;
ORM mapping;
database access;
external integrations.

Разрешено:

SQLAlchemy;
Session;
ORM models.

Запрещено:

зависеть от API;
зависеть от Application.
API

API содержит:

FastAPI routers;
request/response schemas;
dependency injection;
обработку Application Exceptions.

API:

принимает HTTP запрос;
вызывает Application Services;
возвращает результат.

Запрещено:

бизнес-логика;
Repository вызовы;
SQLAlchemy;
прямой доступ к Database.
Repository Boundary
Domain Repository

Расположение:

app/domains/*/repositories/

Назначение:

только интерфейсы;
абстракции хранения.

Запрещено:

SQLAlchemy;
Session;
ORM.
Infrastructure Repository

Расположение:

app/infrastructure/*/

Назначение:

реализация Repository Interface;
работа с SQLAlchemy;
преобразование ORM ↔ Domain через Mapper.

Application зависит только от Repository Interface.

Infrastructure Repository подключается через Dependency Injection.

ORM Models Policy

app/models сохраняется.

Назначение:

SQLAlchemy persistence models only

Правила:

используются только Infrastructure;
не импортируются в Domain;
не импортируются в Application;
не импортируются в API.

На текущем этапе app/models сохраняется как persistence layer.

Возможная дальнейшая эволюция ORM mapping рассматривается отдельно через миграцию без нарушения архитектурных границ.

Database Baseline

Database:

PostgreSQL

Migration:

Alembic enabled

Источник миграций:

backend/alembic
Migration Status
Sfera Architecture v2.0

Статус:

COMPLETED

Завершено:

Project Constitution;
Architecture Standards;
Layer Standards;
DDD migration;
Legacy CRUD removal;
Domain isolation;
Application isolation;
API isolation;
Domain Exceptions Isolation;
Architecture Dependency Audit.
Миграция модулей
Module	Status
Organization	COMPLETED
Customer	COMPLETED
Order	COMPLETED
Material	COMPLETED
Warehouse	COMPLETED
Verification	COMPLETED
Repair	COMPLETED
Diagnostic	COMPLETED
PriceList	COMPLETED
PriceListItem	COMPLETED
Device	COMPLETED
Workflow	COMPLETED
Legacy Layers

Статус:

REMOVED

Удалено:

app/crud;
app/services/price_list_service.py;
app/api/base_router.py.

Проверено:

нет активных импортов app.crud;
нет активных legacy services;
нет BaseRouter.
Dependency Audit

Проверено:

API isolation;
Application isolation;
Domain isolation;
Repository boundaries;
Infrastructure dependency direction.

Результат:

API

✓ no repositories
✓ no ORM


Application

✓ no Infrastructure
✓ no ORM


Domain

✓ no ORM
✓ no Infrastructure


Infrastructure

✓ no API
✓ no Application
Exceptions Isolation

Статус:

COMPLETED

Выполнено:

Domain-specific exceptions;
Application-specific exceptions;
удаление generic ValueError из бизнес-слоёв;
разделение ошибок по слоям.

Domain Exceptions:

Device;
Order;
Verification;
Warehouse.
Validation Baseline

Последняя зафиксированная проверка:

2026-08-02

pytest tests/

16 passed

Quality checks:

ruff check
ruff format
pre-commit

Не уменьшать количество тестов без отдельного решения.

Architecture Validation Commands
Domain isolation
grep -R --exclude-dir=__pycache__ "app.models" -n app/domains

Ожидаемый результат:

нет результатов
Application isolation
grep -R --exclude-dir=__pycache__ "app.infrastructure" -n app/application

Ожидаемый результат:

нет результатов
Application ORM isolation
grep -R --exclude-dir=__pycache__ "Session\|select\|commit\|flush" -n app/application

Ожидаемый результат:

нет результатов
API isolation
grep -R --exclude-dir=__pycache__ "repository" -n app/api

Ожидаемый результат:

нет Repository dependencies
Infrastructure direction
grep -R --exclude-dir=__pycache__ "app.api\|app.application" -n app/infrastructure

Ожидаемый результат:

нет результатов
Current Checkpoint

Branch:

develop

Baseline:

Sfera Architecture v2.0

Текущий checkpoint хранится в Git history.

Перед началом работы проверить:

git status
git log --oneline -5
Текущий этап развития

После завершения миграции начинается:

Architecture Stabilization
+
Business Feature Development

Business Feature Development начинается только после прохождения Architecture Stabilization Phase 1.

Architecture Stabilization Phase 1

Порядок:

Audit Application Services;
Audit Repository Interfaces;
Audit Infrastructure Mappers;
Add automated Architecture Tests;
Business Feature Development.
Правила разработки новых функций

Новый функционал создаётся только через:

Application Service
↓
Repository Interface
↓
Infrastructure Repository
↓
Database

Не использовать:

CRUD;
прямой SQL из Application;
бизнес-логику в API.
Документация проекта

Основные документы:

docs/

AI_CONTEXT.md

MIGRATION_STATUS.md

architecture/

MIGRATION_MATRIX.md
PROJECT_CONSTITUTION.md
ARCHITECTURE.md

Перед началом работы читать:

AI_CONTEXT.md;
MIGRATION_STATUS.md;
MIGRATION_MATRIX.md;
соответствующий архитектурный документ.
Инструкция для AI

При подключении:

Восстановить состояние через GitHub.
Проверить branch.
Проверить последний commit.
Проверить чистоту рабочего дерева.
Прочитать архитектурную документацию.

Не пересказывать документацию.

Сообщить только:

восстановленный checkpoint;
текущий статус;
следующий логический этап.
Правила работы с кодом

Перед изменениями:

читать актуальный код;
проверять зависимости;
определить модуль;
определить статус миграции;
проверить MIGRATION_MATRIX;
проверить наличие legacy;
учитывать модели, схемы и миграции;
не предполагать наличие файлов.

Работа:

анализ;
один файл;
полный код файла;
ожидание подтверждения перед следующим файлом.

При изменениях:

не использовать diff как замену файла;
не создавать новый код без анализа текущей структуры.
После завершения логического этапа

Выполнить:

pytest

ruff check

ruff format --check

git status

git commit

git push origin develop
Архитектурное ограничение

Не предлагать переписывание архитектуры.

Сохранять:

Sfera Architecture v2.0
DDD + Clean Architecture baseline

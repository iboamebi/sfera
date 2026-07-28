# Sfera Project AI Context

## Назначение проекта

Сфера — информационная система сервисного центра и метрологической лаборатории.

Основное направление:
- учёт средств измерений (СИ);
- поверка средств измерений;
- ремонт;
- диагностика;
- документы;
- склад;
- финансы;
- интеграция с ФГИС Аршин.

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

---

# Архитектура

Проект развивается по принципам:

DDD + Clean Architecture

Целевые слои:

Domain
→ Application
→ Infrastructure
→ API
→ Tests

Правило разработки:

Новая бизнес-логика создаётся через:

Application Service
→ Repository
→ Infrastructure

CRUD является временным legacy-слоем.

---

# Основные бизнес-сущности

Центральная сущность:

Order

Workflow:

Order
→ Case
→ Workflow
→ Technological Card
→ Verification / Repair / Diagnostic

Статусы Order:

- NEW
- REGISTERED
- IN_WORK
- WAITING
- COMPLETED
- ISSUED
- CLOSED

---

# Текущее состояние архитектуры

В проекте существует старый слой:

API
→ CRUD
→ SQLAlchemy Model

Идёт постепенная миграция:

API
→ Application Service
→ Repository
→ Infrastructure
→ Database

Миграция выполняется без полного переписывания проекта.

---

# Уже выполнено

## Organization

Переведена на service layer:

- domain entity
- repository interface
- SQLAlchemy repository
- application service
- dependency injection
- API migration

---

# Текущий этап

## PriceList migration

Выполнено:

- создан PriceListRepository interface
- создан SQLAlchemyPriceListRepository
- создан PriceListService

Следующий этап:

- подключить dependency injection;
- убрать зависимость API от price_list_crud;
- удалить использование CRUD после проверки.

---

# Правила работы с кодом

Перед изменениями:

- анализировать существующий код;
- не предполагать наличие файлов;
- учитывать модели, схемы и миграции.

Изменения:

- один файл за шаг;
- полный файл;
- без diff;
- после каждого файла проверка.

---

# Важные ограничения

Не делать:

- массовый rewrite;
- перенос всей архитектуры сразу;
- удаление legacy до проверки нового слоя.

Делать:

- маленькие безопасные миграции;
- сохранять работоспособность;
- фиксировать архитектурные решения.

---

# Репозиторий

GitHub:

iboamebi/sfera

Основная ветка разработки:

develop

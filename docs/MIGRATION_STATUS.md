# Sfera Migration Status

## Текущая задача

Переход от CRUD-архитектуры к DDD/Clean Architecture.

Текущая схема:

API
→ CRUD
→ SQLAlchemy Model

Целевая схема:

API
→ Application Service
→ Repository
→ Infrastructure
→ Database


---

# Выполнено

## Organization

Статус:

COMPLETED

Сделано:

- Domain entity
- Repository interface
- SQLAlchemy repository
- Application service
- Dependency injection
- API migration


---

# В работе

## PriceList

Статус:

IN_PROGRESS


Создано:

- domain repository interface
- SQLAlchemy repository
- Application Service


Осталось:

- подключить dependency injection;
- перевести API router;
- проверить тесты;
- удалить зависимость от price_list_crud.


---

# Следующие кандидаты миграции

Порядок:

1. PriceList
2. Customer
3. Order
4. Material
5. Warehouse
6. Verification
7. Repair
8. Diagnostic


---

# Правила миграции

Для каждой сущности:

1. Создать Repository Interface.
2. Создать Infrastructure Repository.
3. Создать Application Service.
4. Подключить Dependency Injection.
5. Перевести API.
6. Проверить тесты.
7. Удалить старый CRUD после подтверждения.

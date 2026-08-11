# Sfera AI Documentation Index

Этот раздел содержит документы для восстановления контекста проекта при работе с ИИ.

## Текущий статус

По состоянию на 2026-08-11:

- Backend DDD/Clean Architecture migration — **COMPLETE**.
- Application Services Audit — **COMPLETE**.
- API Layer Audit — **COMPLETE**.
- Identifier Generation Audit — **COMPLETE**.
- Legacy CRUD layers — **REMOVED**.
- Infrastructure Mapper Alignment — **COMPLETE**.
- Frontend — **NEXT PHASE**.
- pytest: **26 passed**.
- `ruff check`: **passed**.
- `ruff format --check`: **passed**.

Known technical debt is isolated and must be handled incrementally. Current primary debt: the `PriceList` / `PriceListItem` creation contract does not consistently provide the mandatory `Entity.id`, and dedicated PriceList application tests are absent.

---

## Основные документы

### AI_CONTEXT.md

Основной контекст проекта:

- назначение;
- стек;
- текущая архитектура;
- текущая стадия разработки;
- завершённые аудиты;
- технический долг;
- ближайшие этапы.

### PROJECT_CONSTITUTION.md

Архитектурные правила проекта:

- DDD;
- Clean Architecture;
- dependency direction;
- Domain/Application/Infrastructure/API boundaries;
- repository interfaces;
- Unit of Work;
- правила миграции;
- правила работы с legacy.

### ARCHITECTURE.md

Актуальное архитектурное описание:

- слои приложения;
- зависимости между слоями;
- repository boundary;
- identifier generation policy;
- mapper responsibilities;
- migration strategy;
- текущий backend status;
- known technical debt;
- frontend direction.

### MIGRATION_STATUS.md

Текущий технический статус:

- завершённые миграции;
- завершённые архитектурные аудиты;
- текущий checkpoint;
- технический долг;
- результаты архитектурной очистки.

### MIGRATION_MATRIX.md

Матрица состояния модулей и архитектурных этапов.

Используется для проверки того, какие миграции завершены и какие cleanup/follow-up задачи остаются.

### FRONTEND_ARCHITECTURE.md

Целевая архитектура frontend:

- React / TypeScript / Vite;
- Feature-Sliced Design;
- API integration;
- server/client state;
- forms and validation;
- routing;
- incremental user-scenario workflow.

Frontend ещё не является реализованным production layer; документ описывает согласованную целевую архитектуру.

---

## Порядок работы нового чата

Новый чат должен восстановить контекст в следующем порядке:

1. Прочитать:

```text
 docs/AI_CONTEXT.md
```

2. Прочитать:

```text
 docs/architecture/PROJECT_CONSTITUTION.md
```

3. Прочитать:

```text
 docs/ARCHITECTURE.md
```

4. Прочитать:

```text
 docs/MIGRATION_STATUS.md
```

5. Прочитать:

```text
 docs/architecture/MIGRATION_MATRIX.md
```

6. Если работа относится к frontend, прочитать:

```text
 docs/FRONTEND_ARCHITECTURE.md
```

7. Проверить фактическое состояние репозитория:

- текущая ветка;
- `git status`;
- последний commit;
- синхронизация с `origin/develop`.

8. Сопоставить документацию с фактическим кодом перед изменениями.

9. Продолжить работу только с текущего подтверждённого этапа.

---

## Правила работы

Архитектура:

```text
Domain
    ↓
Application
    ↓
Infrastructure
    ↓
API
    ↓
Tests
```

Repository boundary:

```text
Application / Domain
        ↓
Repository Interface
        ↑
Infrastructure Repository
        ↓
Database
```

Основные правила:

- не добавлять бизнес-логику в API;
- Domain не зависит от Infrastructure, ORM или API;
- Application не зависит от Infrastructure или ORM;
- API не обращается напрямую к Repository, ORM или Database;
- новые изменения выполнять через Application Service → Repository Interface → Infrastructure Repository;
- CRUD legacy не использовать для новой функциональности;
- перед изменением читать актуальный код;
- анализировать зависимости;
- изменять один файл за раз;
- после каждого изменения ожидать подтверждение `y`;
- feature migration и architectural cleanup не смешивать;
- документацию синхронизировать с фактической реализацией.

Identifier policy:

- API routers не генерируют domain identifiers;
- Application Services генерируют identifiers для простых entity creation flows;
- Domain factories могут генерировать identifiers, когда создание полного domain structure является их ответственностью;
- Domain `create()` methods получают identifiers явно, если генерация identifier не является domain business rule.

После завершения логического этапа:

- проверить `git status`;
- выполнить tests и `ruff`, если изменён Python;
- выполнить commit;
- выполнить push;
- только после синхронизации с GitHub переходить к следующему этапу.

---

## Репозиторий

GitHub:

```text
iboamebi/sfera
```

Основная рабочая ветка:

```text
develop
```

Рабочий каталог backend обычно:

```text
backend
```

---

## Следующий этап

Backend migration и архитектурные аудиты завершены.

Следующий основной этап — frontend development:

```text
frontend architecture validation
        ↓
frontend application shell
        ↓
backend API integration
        ↓
one user scenario
        ↓
validate
        ↓
next scenario
```

До начала frontend implementation отдельно можно выполнить изолированный cleanup `PriceList / PriceListItem` creation contract с добавлением application tests.

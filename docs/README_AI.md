# Sfera AI Documentation Index

Этот раздел содержит документы для восстановления контекста проекта при работе с ИИ.

## Текущий статус

По состоянию на 2026-08-16:

- Backend DDD/Clean Architecture migration — **COMPLETE**.
- Application Services Audit — **COMPLETE**.
- API Layer Audit — **COMPLETE**.
- Identifier Generation Audit — **COMPLETE**.
- Legacy CRUD layers — **REMOVED**.
- Infrastructure Mapper Alignment — **COMPLETE**.
- Device creation validation — **COMPLETE**.
- Device application transaction boundary — **COMPLETE**.
- Frontend — **NEXT PHASE**.
- pytest: **33 passed**.
- `ruff check .`: **passed**.
- `ruff format --check .`: **passed**.
- `git diff --check`: **passed**.

### Последний backend checkpoint

`DeviceApplicationService` теперь получает `UnitOfWork` через Dependency Injection. Use cases `create`, `connect` и `disconnect` выполняются внутри transaction boundary.

При создании Device Application layer проверяет существование `InstrumentType`. При отсутствии типа выбрасывается `InstrumentTypeNotFoundApplicationError`, а API преобразует его в HTTP 404.

Последний синхронизированный commit:

```text
b69b551 refactor: add unit of work to device service
```

Ветка:

```text
develop
```

Working tree после последнего push был чистым, `develop` синхронизирован с `origin/develop`.

Known technical debt is isolated and must be handled incrementally. Current primary debt: the `PriceList` / `PriceListItem` creation contract does not consistently provide the mandatory `Entity.id`, and dedicated PriceList application tests are absent.

---

## Основные документы

### AI_CONTEXT.md

Основной контекст проекта: назначение, стек, архитектура, текущая стадия, завершённые аудиты и технический долг.

### PROJECT_CONSTITUTION.md

Нормативные архитектурные правила: DDD, Clean Architecture, dependency direction, repository interfaces, Unit of Work и правила миграции.

### ARCHITECTURE.md

Актуальное архитектурное описание слоёв, зависимостей, repository boundary, identifier policy, mapper responsibilities и frontend direction.

### MIGRATION_STATUS.md

Текущий статус миграции, архитектурных аудитов и технического долга.

### MIGRATION_MATRIX.md

Матрица состояния модулей и архитектурных этапов.

### FRONTEND_ARCHITECTURE.md

Целевая архитектура frontend на React / TypeScript / Vite.

---

## Порядок работы нового чата

1. Прочитать `docs/AI_CONTEXT.md`.
2. Прочитать `docs/architecture/PROJECT_CONSTITUTION.md`.
3. Прочитать `docs/ARCHITECTURE.md`.
4. Прочитать `docs/MIGRATION_STATUS.md`.
5. Прочитать `docs/architecture/MIGRATION_MATRIX.md`.
6. При frontend-задаче прочитать `docs/FRONTEND_ARCHITECTURE.md`.
7. Проверить фактическое состояние репозитория: ветку, `git status`, последний commit и синхронизацию с `origin/develop`.
8. Сопоставить документацию с фактическим кодом перед изменениями.
9. Продолжить только с текущего подтверждённого этапа.

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
- Domain factories могут генерировать identifiers, когда создание полной domain structure является их ответственностью;
- Domain `create()` methods получают identifiers явно, если генерация identifier не является domain business rule.

После завершения логического этапа:

- проверить `git status`;
- выполнить tests и `ruff`, если изменён Python;
- выполнить commit;
- выполнить push;
- только после синхронизации с GitHub переходить к следующему этапу.

---

## Репозиторий

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

После текущего Device checkpoint следующий логичный backend шаг — интеграционная проверка Device API с FastAPI `TestClient` и dependency overrides.

Проверить:

1. `POST /devices/` с существующим `InstrumentType`.
2. `POST /devices/` с отсутствующим `InstrumentType` → HTTP 404.
3. DI цепочку `get_device_service`.
4. API → Application → Repository/UoW boundary.
5. Отсутствие бизнес-логики в router.

Работа продолжается по правилу:

```text
analyze → one file → y → next
```

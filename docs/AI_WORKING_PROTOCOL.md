# Рабочий протокол ИИ для проекта «Сфера»

## Назначение

Этот документ определяет постоянный рабочий процесс при работе ИИ с проектом «Сфера».

Он описывает:

- архитектурные границы;
- порядок анализа и изменения кода;
- правила работы с GitHub;
- правила локальной валидации;
- порядок работы с документацией;
- взаимодействие с пользователем;
- требования к качеству изменений.

Документ не заменяет `PROJECT_CONSTITUTION.md` и не изменяет нормативные архитектурные правила.

---

## 1. Приоритет документации

Перед архитектурными изменениями ИИ обязан ознакомиться с актуальными документами проекта.

Приоритет:

1. `docs/architecture/PROJECT_CONSTITUTION.md` — нормативные архитектурные правила.
2. `docs/ARCHITECTURE.md` — актуальное описание архитектуры.
3. `docs/MIGRATION_STATUS.md` — текущий статус миграции и архитектурных аудитов.
4. `docs/architecture/MIGRATION_MATRIX.md` — состояние миграции по модулям.
5. `docs/architecture/AUTHENTICATION.md` — authentication contract.
6. `docs/architecture/AUTHORIZATION.md` — authorization contract.
7. `docs/FRONTEND_ARCHITECTURE.md` — frontend architecture.
8. `docs/AI_CONTEXT.md` — текущий технический контекст и checkpoint.
9. `docs/AI_WORKING_PROTOCOL.md` — данный рабочий протокол.

Если документы противоречат друг другу, нормативные правила Конституции имеют приоритет.

`PROJECT_CONSTITUTION.md` нельзя изменять как обычный documentation file. Изменение Конституции требует новой утвержденной версии.

---

## 2. Архитектурная модель

Проект использует DDD + Clean Architecture.

Основное направление зависимостей:

```text
API
  ↓
Application
  ↓
Domain
  ↓
Repository Interface
  ↑
Infrastructure Repository
  ↓
Database
```

Правила:

1. API не содержит бизнес-логики.
2. Application работает через Repository Interfaces / Ports.
3. SQLAlchemy используется только в Infrastructure.
4. Domain не знает FastAPI, SQLAlchemy, HTTP, cookies и внешние технические библиотеки.
5. Infrastructure не импортирует Application или API.
6. Application не импортирует Infrastructure или API.
7. Router не обращается напрямую к Repository или Database.
8. Legacy CRUD не возвращается в новую архитектуру.
9. Feature migration и architectural cleanup не смешиваются без необходимости.
10. Не создаются duplicate SQLAlchemy models, tables или migrations.
11. Security decisions не угадываются.
12. При наличии готовой инфраструктуры используется существующий контракт, а не создается дубль.

---

## 3. Основной workflow

Для каждого независимого изменения:

```text
read current state
  ↓
analyze
  ↓
identify smallest architectural change
  ↓
read all affected files
  ↓
implement minimal change
  ↓
run/recommend validation
  ↓
commit and push to GitHub
  ↓
synchronize local checkout
  ↓
validate locally
  ↓
analyze result
  ↓
continue to next independent stage
```

Изменения должны быть:

- минимальными;
- связанными с одной задачей;
- инкрементальными;
- обратимо проверяемыми;
- покрытыми тестами в соответствии с риском.

Не следует объединять несколько независимых feature changes в один этап.

---

## 4. Работа с GitHub

Если GitHub доступен, ИИ читает актуальные файлы напрямую из GitHub.

Обязательные правила:

- не предполагать существование файла, класса, функции или API;
- перед изменением читать фактический текущий файл;
- при необходимости анализировать связанные зависимости пакетно;
- для `update_file` использовать фактический blob SHA;
- после записи считать изменение подтвержденным только после получения commit SHA от GitHub;
- не утверждать, что GitHub синхронизирован, без фактического результата операции;
- после изменения сообщать commit SHA и точные команды локальной синхронизации/проверки.

Стандартная синхронизация:

```bash
cd ~/sfera
git pull --ff-only origin develop
```

Если локальная ветка уже содержит изменения пользователя, не использовать destructive sync-команды.

---

## 5. Локальная валидация

### Backend

```bash
cd ~/sfera/backend
source .venv/bin/activate

pytest -q
ruff check .
ruff format --check .

git status
git log -5 --oneline
```

Если изменение содержит Alembic migration:

```bash
alembic upgrade head
```

Если изменены конкретные тесты, допускается сначала выполнить их, затем полный набор backend checks.

### Frontend

```bash
cd ~/sfera/frontend

npm ci
npm run typecheck
npm run build
```

Для production deployment используется существующий ручной nginx workflow. Не создавать автоматический deployment pipeline без отдельного требования.

---

## 6. Ruff

Ожидаемая локальная версия:

```text
ruff 0.16.1
```

При неожиданном formatting mismatch:

1. проверить фактическую версию Ruff;
2. прочитать `pyproject.toml`;
3. получить актуальный файл из GitHub;
4. выполнить formatter один раз;
5. повторно проверить `ruff format --check .`.

Не создавать несколько слепых formatting commits.

---

## 7. Тестирование

Значимый функционал должен иметь тесты на соответствующих архитектурных границах:

```text
Domain
Application
Infrastructure
API
```

Конкретный набор зависит от характера изменения.

Для security-sensitive изменений обязательно покрывать regression behavior.

Architecture tests нельзя ослаблять ради прохождения CI. При нарушении dependency direction исправляется код.

---

## 8. Security workflow

Authentication и Authorization — разные ответственности.

```text
Authentication
Who is the user?

Authorization
What may the user do?
```

Authentication использует server-side sessions и HttpOnly cookie согласно `AUTHENTICATION.md`.

Authorization принимается на уровне конкретного Application use case.

Общий принцип:

```text
Authenticated User
        ↓
Application Authorization Policy
        ↓
Application Use Case
        ↓
Domain
```

Frontend visibility и route guards не являются security boundary.

Не выводить authorization rules механически из CRUD. Каждое новое правило должно следовать из конкретного бизнес-use-case.

---

## 9. Работа с Application authorization

Для state-changing business use case, которому требуется authorization:

1. определить бизнес-требование;
2. передать authenticated `User` из API boundary в Application use case;
3. выполнить authorization check в Application;
4. вызвать Domain behavior после успешной проверки;
5. покрыть authorized и unauthorized behavior Application tests;
6. покрыть API forwarding/authentication boundary tests;
7. обновить `docs/architecture/AUTHORIZATION.md`.

Role checks не должны быть разбросаны по React components или FastAPI routers.

---

## 10. Работа с миграциями

Перед созданием migration:

1. проверить текущий Alembic head;
2. проверить существующие ORM models и registry;
3. проверить существующие tables/migrations;
4. убедиться, что таблица или модель не существует уже в проекте;
5. проверить `down_revision`.

Нельзя создавать duplicate table или duplicate migration для уже существующей persistence structure.

После migration пользователь локально выполняет:

```bash
alembic upgrade head
```

---

## 11. Документация

Документация является частью реализации.

Архитектурное изменение должно отражаться в соответствующем рабочем документе.

Использовать документы по назначению:

- `PROJECT_CONSTITUTION.md` — только нормативные правила;
- `ARCHITECTURE.md` — архитектурная модель;
- `MIGRATION_STATUS.md` — migration/checkpoint status;
- `MIGRATION_MATRIX.md` — migration matrix;
- `AUTHENTICATION.md` — authentication contract;
- `AUTHORIZATION.md` — authorization contract;
- `FRONTEND_ARCHITECTURE.md` — frontend architecture;
- `AI_CONTEXT.md` — volatile project state and recovery context;
- `AI_WORKING_PROTOCOL.md` — stable AI workflow rules.

Не помещать в рабочий protocol volatile commit hashes, результаты последнего тестового запуска или временные checkpoints. Такие сведения относятся к `AI_CONTEXT.md`.

---

## 12. Взаимодействие с пользователем

Пользователь выполняет локальные команды и возвращает фактический вывод.

Если локальная проверка необходима, ИИ останавливается после выдачи точных команд.

После получения результата ИИ:

1. анализирует вывод;
2. не повторяет уже успешные шаги;
3. исправляет только необходимое;
4. продолжает следующий независимый этап.

`y` означает, что предыдущая локальная проверка завершена и можно продолжать.

Для GitHub-only чтения, анализа зависимостей и связанных проверок не требуется ждать `y`.

Не запрашивать разрешение на чтение файлов, если GitHub уже доступен.

Не выполнять background work и не обещать работу после ответа.

---

## 13. Правило «один локальный шаг»

Пользователь обслуживает один локальный validation step за раз.

Команды должны быть компактными и достаточными для текущего этапа.

После успешного результата следующий этап определяется автоматически.

Не выдавать повторно уже выполненные команды без причины.

---

## 14. Commit policy

Commit должен описывать одну независимую логическую задачу.

Примеры:

```text
feat: authorize customer creation
feat: authorize customer updates
test: cover customer deletion authorization
docs: define order update authorization
```

Перед commit необходимо убедиться, что в изменениях нет unrelated файлов.

После commit и push необходимо подтвердить GitHub synchronization.

---

## 15. Quality bar

Для значимого feature stage ожидается:

```text
Domain
✓

Application
✓

Repository Interface
✓

Infrastructure
✓

API
✓

Tests
✓

Documentation
✓

Frontend
✓ where applicable
```

Нельзя обходить слой архитектуры ради более короткой реализации.

---

## 16. Recovery procedure

При восстановлении работы после паузы:

1. прочитать этот документ;
2. прочитать `PROJECT_CONSTITUTION.md`;
3. прочитать соответствующие architecture/security documents;
4. прочитать `AI_CONTEXT.md` для текущего checkpoint;
5. проверить GitHub `develop` и последние commits;
6. только после этого выбирать следующий use case.

Текущий checkpoint не является частью постоянного protocol и должен храниться в `AI_CONTEXT.md`.

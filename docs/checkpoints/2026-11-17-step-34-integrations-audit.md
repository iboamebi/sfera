# Step 34 — Integrations, import/export and operational infrastructure

**Дата аудита:** 2026-11-17  
**Статус:** PARTIALLY_IMPLEMENTED / OPEN  
**Тип:** исторический план + фактический аудит текущего `develop`

---

## 1. Назначение исторического шага

Исторический Step 34 объединяет:

- интеграционный слой;
- журнал обменов;
- экспорт результатов поверки в ФГИС «Аршин»;
- импорт справочных и начальных данных;
- внешние API;
- сетевую эксплуатацию через ZeroTier;
- резервное копирование;
- мониторинг.

Исторический план является источником требований, но не доказательством существующей реализации.

---

## 2. Фактическое состояние на момент аудита

Аудит выполнен по текущему `develop` с приоритетом фактического backend-кода и существующей документации.

### 2.1. Arshin

В ORM существует модель:

`backend/app/models/arshin_export.py`

Она содержит:

- `verification_id`;
- `file_name`;
- `exported_at`;
- `exported_by`;
- `comment`.

То есть persistence-слой для факта экспорта существует.

При этом в проверенных путях не обнаружены:

- отдельный Arshin Domain aggregate;
- Application service экспорта;
- Arshin API router;
- Infrastructure XLSM exporter;
- workflow валидации/подготовки/экспорта;
- текущий API для создания/получения Arshin export;
- генерация XLSM;
- полноценный контроль eligibility перед экспортом.

Документ `docs/modules/arshin.md` описывает целевое поведение, но не является доказательством реализации.

### 2.2. Интеграционный журнал

Модель/aggregate `integration_logs` в проверенных путях не обнаружена.

Не обнаружены также:

- Integration Domain/Application слой;
- API `/integrations/*`;
- persistence журнала внешних обменов;
- единый контракт статусов `STARTED/SUCCESS/WARNING/ERROR/CANCELLED`.

### 2.3. Импорт

В проверенных backend-путях не обнаружен отдельный импортный pipeline:

```text
Файл
  ↓
Проверка
  ↓
Предпросмотр
  ↓
Подтверждение
  ↓
Импорт
```

Также не обнаружены подтверждённые текущим кодом:

- универсальный import job;
- import preview;
- import validation report;
- duplicate detection framework;
- persistent import error journal.

### 2.4. Внешние API

Текущий `backend/app/main.py` содержит обычные бизнес-router'ы, но отдельный integration API router в проверенном коде отсутствует.

Это не означает запрет на будущие внешние API; означает, что отдельный интеграционный слой ещё не сформирован.

### 2.5. Эксплуатационная инфраструктура

В рамках текущего backend-аудита отдельные application-модули для:

- backup;
- backup verification/restore check;
- monitoring;
- disk-space checks;
- integration error monitoring

не обнаружены.

При этом текущая эксплуатационная схема уже использует nginx, backend service, PostgreSQL и ZeroTier. Это относится к deployment/infrastructure и не должно дублироваться как Domain/Application логика.

### 2.6. Health

В `backend/app/main.py` уже существует:

`GET /health`

Он возвращает:

```json
{"status": "ok"}
```

Это базовая проверка доступности приложения, но она не является полноценным `GET /system/status` из исторического Step 34.

---

## 3. Важное ограничение для реализации

Step 34 нельзя реализовать как один монолитный «integration service».

Нужно разделить как минимум:

1. **Domain/Application integration contracts** — только бизнес-правила и orchestration;
2. **Arshin adapter/exporter** — XLSM и внешний обмен;
3. **Import pipeline** — validation/preview/confirmation/import;
4. **Integration log** — история попыток обмена;
5. **Operational infrastructure** — backup, monitoring, ZeroTier, deployment;
6. **API boundary** — внешние HTTP endpoints.

Инфраструктурные проверки не должны становиться бизнес-логикой Domain.

---

## 4. Arshin — особая граница

Arshin не должен изменять исходные данные `Verification`.

Целевой поток:

```text
Verification
    ↓
Eligibility validation
    ↓
Export preparation
    ↓
XLSM generation
    ↓
ArshinExport persistence
    ↓
External transmission / handoff
```

Экспорт должен быть идемпотентно контролируемым и трассируемым.

Отдельно требуется сохранить различие между:

- разрешением на экспорт;
- подготовкой экспортных данных;
- созданием файла;
- фактом передачи;
- подтверждением внешней системы.

Наличие только `arshin_exports` недостаточно для этих состояний.

---

## 5. Импорт

Импорт должен быть пакетной операцией с отдельной жизнью от исходных доменных сущностей.

Минимальная граница:

```text
Upload
  ↓
Parse
  ↓
Validate
  ↓
Preview
  ↓
Confirm
  ↓
Apply
  ↓
Result
```

Ошибки отдельных строк не должны теряться.

Дубли и конфликтующие записи должны быть выявлены до изменения authoritative data.

---

## 6. Операционная часть

Исторический план объединяет backup, monitoring и ZeroTier, но это разные уровни ответственности.

### ZeroTier

ZeroTier относится к сетевому доступу и эксплуатации. Его настройки не должны храниться в Domain.

### Backup

Для PostgreSQL и файлов требуется отдельная эксплуатационная процедура с:

- регулярностью;
- retention;
- контролем успешности;
- проверкой восстановления.

### Monitoring

Нужны как минимум наблюдаемые состояния:

- приложение доступно;
- PostgreSQL доступен;
- свободное место не ниже порога;
- API не генерирует массовые ошибки;
- интеграционные операции не накапливаются в состоянии ошибки.

Точный инструмент мониторинга пока не зафиксирован.

---

## 7. Статусы требований

| Область | Статус |
|---|---|
| Arshin ORM persistence | PARTIALLY_IMPLEMENTED |
| Arshin export service | OPEN |
| Arshin XLSM generation | OPEN |
| Arshin eligibility validation | OPEN |
| Integration logs | IMPLEMENTED — persistence boundary and lifecycle contract |
| Import pipeline | OPEN |
| External integration API | OPEN |
| `GET /health` | IMPLEMENTED |
| `GET /system/status` | OPEN |
| ZeroTier operational access | EXISTING INFRASTRUCTURE / DOCUMENTATION REQUIRED |
| PostgreSQL backup | OUTSIDE CURRENT BACKEND CODE / VERIFY OPERATIONAL CONFIG |
| File backup | OUTSIDE CURRENT BACKEND CODE / VERIFY OPERATIONAL CONFIG |
| Backup restore verification | OPEN |
| Monitoring | OPEN |

---

## 8. Что не следует делать на этом шаге

Не следует:

- создавать второй независимый Arshin persistence layer;
- дублировать `Verification` как экспортную сущность;
- смешивать Audit Trail и Integration Log;
- считать `GET /health` полноценным monitoring subsystem;
- реализовывать backup внутри бизнес-приложения без отдельного эксплуатационного контракта;
- автоматически импортировать весь внешний справочник без правил authoritative ownership;
- менять исходные результаты поверки ради требований Arshin.

---

## 9. Следующая реализационная последовательность

Рекомендуемый порядок:

1. зафиксировать Integration boundary и IntegrationLog contract;
2. реализовать Arshin eligibility + export application flow вокруг существующего `arshin_exports`;
3. реализовать XLSM adapter и тесты;
4. реализовать import pipeline как отдельный bounded application flow;
5. добавить внешние integration endpoints;
6. отдельно проверить и документировать backup/restore;
7. отдельно определить monitoring contract и эксплуатационные checks.

Шаги 6–7 требуют проверки реальной эксплуатационной конфигурации, а не только backend-кода.

---

## 10. Реализационный этап 1 — Integration Log

На ветке `feat/integration-log-foundation` реализована первая минимальная граница Step 34:

- общий контракт `IntegrationLog`;
- статусы `STARTED/SUCCESS/WARNING/ERROR/CANCELLED`;
- контролируемые переходы из `STARTED` в конечный статус;
- repository interface;
- SQLAlchemy persistence;
- JSONB request/response payloads;
- Alembic migration `d1e7b4c9a2f1`;
- repository/domain tests.

Граница не добавляет HTTP API и не смешивает Integration Log с Audit Trail. Следующий этап — использовать этот контракт в Arshin application flow.

---

## 11. Источники

- `docs/modules/arshin.md` — исторически сохранённый целевой контракт Arshin.
- `backend/app/models/arshin_export.py` — фактическая текущая persistence-модель.
- `backend/app/main.py` — фактическая текущая регистрация API и существующий `GET /health`.
- `docs/architecture/DOCUMENTATION_HISTORY.md` — правила сопоставления исторических документов с текущим кодом.


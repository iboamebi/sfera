# Sfera Frontend Architecture

## 1. Статус документа

Этот документ описывает **актуальную архитектуру и правила frontend Sfera**.

Frontend развивается поэтапно поверх существующего backend API. Backend DDD/Clean Architecture остаётся источником бизнес-правил; frontend отвечает за UI, клиентскую валидацию и orchestration server state.

Текущий frontend checkpoint включает Orders и read/detail slices для Customer, Organization, Material, Verification, Diagnostic, Repair и PriceList, InstrumentType list/detail, а также Warehouse Stock read slice.

---

## 2. Технологический стек

Фактически используется:

* React 19;
* TypeScript 7;
* Vite 8;
* React Router 8;
* TanStack Query 5;
* Axios;
* Material UI 9;
* React Hook Form;
* Zod.

Версии фиксируются в `frontend/package.json` и `frontend/package-lock.json`.

---

## 3. Архитектурный подход

Frontend использует **feature-oriented architecture**, согласованную с принципами Feature-Sliced Design.

Основные правила:

* API изолирован от UI;
* backend DTO отделяются от frontend models;
* server state управляется TanStack Query;
* pages являются точками композиции сценариев;
* бизнес-логика не помещается в pages/UI;
* новые уровни (`widgets`, `entities`, `shared`) добавляются только при реальной необходимости;
* один пользовательский сценарий реализуется небольшими последовательными шагами.

---

## 4. Фактическая структура

```text
frontend/src/

app/
    App.tsx
    router.tsx
    providers/

pages/
    auth/
    orders/
    customers/
    organizations/
    materials/
    verifications/
    diagnostics/
    repairs/
    price-lists/
    instrument-types/

features/
    auth/
    orders/
    customers/
    organizations/
    materials/
    verifications/
    diagnostics/
    repairs/
    price-lists/
    instrument-type/
```

Структура является живой архитектурой и уточняется по мере появления пользовательских сценариев.

---

## 5. Application shell

Текущая композиция:

```text
App
 ├── QueryProvider
 └── RouterProvider
```

Маршрутизация определяется в `frontend/src/app/router.tsx`.

---

## 6. Маршрутизация

Актуальные маршруты на `develop`:

```text
/login
/change-password
/
/orders
/orders/new
/orders/:orderId
/customers
/customers/:customerId
/organizations
/organizations/:organizationId
/materials
/materials/:materialId
/verifications/:verificationId
/diagnostics/:diagnosticId
/repairs/:repairId
/price-lists/:priceListId
/instrument-types
/instrument-types/:instrumentTypeId
/warehouse-stocks/warehouse/:warehouseId
/users
```

`/login` является публичным. `/change-password` доступен только аутентифицированному пользователю. Остальные пользовательские маршруты защищены `RequireAuth`.

---

### Warehouse Stock

Реализован read slice:

```text
API DTO
  ↓
mapper
  ↓
frontend model
  ↓
query hook
  ↓
WarehouseStockPage
  ↓
/warehouse-stocks/warehouse/:warehouseId
```

Frontend отвечает только за отображение и orchestration server state.

### 6.1 Authentication and first-login flow

Implemented:

- login and current-user API adapters;
- mapping of backend `must_change_password` into frontend `mustChangePassword`;
- React Query current-user state;
- authenticated route guard;
- mandatory redirect to `/change-password` while first-login password change is pending;
- password-change form and mutation;
- CSRF header forwarding for cookie-authenticated cross-origin requests.

The frontend route guard is not a security boundary. Backend business routers enforce authentication and first-login completion.

## 7. Реализованные frontend slices

### Orders

Реализованы:

* список заказов;
* loading/error/empty states;
* создание заказа;
* просмотр заказа;
* позиции заказа;
* переходы от позиции заказа к связанным поверкам по verification IDs из order read contract;
* регистрация заказа;
* обновление cache после регистрации;
* customer selection.

### Customer

Реализованы list/detail API integration, frontend model/mapper, query hook и detail page/route.

### Organization

Реализованы list/detail API integration, frontend model/mapper, query hooks, list/detail pages и защищённые routes. List связан с detail.

### Material

Реализованы list/detail API integration, frontend DTO/model/mapper, query hooks, list/detail pages и защищённые routes. List связан с detail.

### Verification

Реализованы create, detail read slice и lifecycle actions.

Создание поверки доступно из позиции заказа, если запрошена операция поверки, назначено конкретное СИ и для позиции ещё нет поверки:

```text
OrderItems
  ↓
CreateVerification form
  ↓
createVerification()
  ↓
POST /verifications
  ↓
useCreateVerification()
  ↓
invalidate order query
  ↓
/verifications/:verificationId
```

Форма передаёт дату, тип поверки (PRIMARY, PERIODIC, AFTER_REPAIR) и необязательную методику. Backend остаётся источником проверки полномочий и наличия назначенного СИ.

Detail and lifecycle flow:

```text
API DTO
  ↓
mapper
  ↓
frontend model
  ↓
getVerification()
  ↓
useVerification()
  ↓
VerificationPage
  ├── CREATED → StartVerificationButton
  └── IN_PROGRESS
        ├── ApproveVerificationButton
        └── RejectVerificationButton
  ↓
/verifications/:verificationId
```

Lifecycle actions use dedicated API functions and TanStack Query mutations:

- start: `POST /verifications/{verification_id}/start`;
- approve: `POST /verifications/{verification_id}/approve?valid_until=...`;
- reject: `POST /verifications/{verification_id}/reject?reason=...`.

After a successful mutation, the verification detail query is invalidated. Mutation pending and error states are displayed by the action UI. The page hides actions for archived records and only shows actions valid for the current lifecycle state.

### Diagnostic

Реализован аналогичный detail read slice:

```text
API DTO → mapper → frontend model → getDiagnostic() → useDiagnostic() → DiagnosticPage
```

Route:

```text
/diagnostics/:diagnosticId
```

### Repair

Реализован detail read slice:

```text
API DTO → mapper → frontend model → getRepair() → useRepair() → RepairPage
```

Route:

```text
/repairs/:repairId
```

### PriceList

Реализован detail read slice:

```text
API DTO
  ↓
mapper
  ↓
frontend model
  ↓
getPriceList()
  ↓
usePriceList()
  ↓
PriceListPage
  ↓
/price-lists/:priceListId
```

В текущем frontend-коде нет подтверждённого существующего источника `priceListId` для list→detail navigation, поэтому ссылку из списка пока не добавляем.

### InstrumentType

Реализованы list и detail read slices.

List:

```text
GET /instrument-types/
  ↓
getInstrumentTypes()
  ↓
mapper
  ↓
useInstrumentTypes()
  ↓
InstrumentTypesPage
```

Detail:

```text
GET /instrument-types/{instrument_type_id}
  ↓
getInstrumentType()
  ↓
mapper
  ↓
useInstrumentType()
  ↓
InstrumentTypePage
```

CRUD mutations для InstrumentType во frontend пока не реализованы.

---

## 8. Boundary API → model

Backend является источником истины.

Общий поток:

```text
FastAPI backend
      ↓
Axios API layer
      ↓
backend DTO
      ↓
mapper
      ↓
frontend model
      ↓
React Query hook
      ↓
Page / Feature UI
```

Backend `snake_case` не распространяется по UI model. Например `instrument_id` преобразуется в `instrumentId`, `measurement_type` — в `measurementType`.

Generated TypeScript API client пока не используется.

---

## 9. Server state

TanStack Query используется для:

* загрузки данных;
* cache;
* query hooks;
* mutations;
* pending/error states;
* обновления данных после пользовательских действий.

Бизнес-данные не должны без необходимости дублироваться в глобальном client state.

---

## 10. Pages и UI

Pages являются точками композиции сценария и не должны содержать HTTP-запросы или domain-specific business logic.

Типовой read flow:

```text
Page
  ↓
useQuery hook
  ↓
loading / error / empty / data
  ↓
presentation
```

Сложные состояния и действия выносятся в feature model/API/UI.

---

## 11. Формы и валидация

* формы реализуются через React Hook Form;
* схемы проверки — Zod;
* frontend validation отвечает за UX;
* backend остаётся источником истины для business validation.

Frontend validation не заменяет backend validation.

---

## 12. Обработка состояний

Для каждого применимого пользовательского сценария учитываются:

* loading;
* success/data;
* empty state;
* API error;
* mutation pending;
* mutation error.

Ошибки backend не должны молча подавляться.

---

## 13. Правила разработки

```text
анализ
↓
один файл / один небольшой шаг
↓
проверка
↓
y
↓
следующий шаг
```

Соблюдаются:

* анализ существующего кода перед изменением;
* один небольшой сценарий за итерацию;
* разделение API/model/UI;
* отсутствие бизнес-логики в pages;
* typecheck после изменений;
* build после изменений;
* документация синхронизируется с кодом;
* изменения фиксируются и синхронизируются с GitHub.

---

## 14. Definition of Done

Frontend slice считается завершённым, когда:

* backend contract существует;
* API layer реализован;
* DTO/model boundary определён;
* mapper реализован при необходимости;
* React Query hook реализован;
* UI реализован;
* применимые loading/error/empty states обработаны;
* typecheck проходит;
* build проходит;
* документация обновлена;
* commit опубликован в `develop`.

---

## 15. Current implementation checkpoint

На текущем `develop`:

```text
Orders
  ├── list                 ✓
  ├── create               ✓
  ├── detail               ✓
  ├── items                ✓
  └── register             ✓

Customer
  └── detail               ✓

Organization
  ├── list                 ✓
  └── detail               ✓

Material
  ├── list                 ✓
  └── detail               ✓

Verification
  ├── detail               ✓
  └── lifecycle actions    ✓

Diagnostic
  └── detail               ✓

Repair
  └── detail               ✓

PriceList
  └── detail               ✓

InstrumentType
  ├── list                 ✓
  └── detail               ✓
```

Последний опубликованный frontend checkpoint перед обновлением документации:

```text
b953cb5 feat: add price list detail route
```

Последняя локальная валидация:

```text
npm run typecheck — passed
npm run build     — passed
```

Vite сообщает warning о bundle chunk > 500 kB. Это не является ошибкой сборки.

---

## 16. Production runtime

```text
Browser
    ↓
nginx
    ├── static React SPA
    └── /api/*
          ↓
        FastAPI backend
```

Production frontend использует Vite build и nginx. Постоянно работающий Vite development server для production не требуется.

---

## 17. Next-step policy

После завершения серии read/detail slices следующий сценарий выбирается **только после аудита актуального backend и frontend состояния**.

Нельзя:

* автоматически начинать CRUD только потому, что detail готов;
* создавать list→detail links без подтверждённого ID source;
* добавлять backend authorization для `Device`, `InstrumentType`, `PriceList` или `Workflow` без explicit business requirement;
* возвращаться к legacy CRUD architecture.

Следующий шаг определяется фактическим пользовательским flow и существующим backend contract.


## User Administration

User administration UI and API integration are implemented on the active feature branch:

- `GET /users/?include_archived=` loads users through a DTO mapper and React Query;
- `POST /users/` creates a user and displays the temporary password from the creation response only;
- role changes use `PATCH /users/{user_id}/role`;
- activation/deactivation uses `PATCH /users/{user_id}/status`;
- archive and restore use their dedicated POST endpoints;
- the list can optionally include archived accounts.

Route:

```text
/users
```

Backend Application authorization remains the security boundary. The page route guard only requires authentication and does not replace backend administrator authorization. Local typecheck/build validation is required after this implementation.

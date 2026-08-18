# Sfera Frontend Architecture

## 1. Статус документа

Этот документ описывает **актуальную архитектуру и правила frontend Sfera**.

Frontend application уже реализован и развивается поэтапно поверх существующего backend API.

Текущий реализованный пользовательский контур — **Orders**:

* список заказов;
* отображение пустого состояния;
* отображение ошибки загрузки;
* создание заказа;
* просмотр заказа;
* регистрация заказа;
* обновление cache после регистрации.

Backend DDD/Clean Architecture остается источником бизнес-правил. Frontend отвечает за пользовательский интерфейс, локальную валидацию и orchestration клиентских запросов.

---

## 2. Назначение

Frontend является пользовательским интерфейсом информационной системы Sfera.

Основная задача frontend:

* предоставить рабочий интерфейс сотрудникам сервисного центра и метрологической лаборатории;
* заменить использование Swagger в ежедневной работе;
* реализовать пользовательские сценарии поверх существующего backend API.

Frontend не содержит бизнес-правил предметной области. Бизнес-логика остается в backend слоях Domain и Application.

---

## 3. Технологический стек

Фактически используется следующий стек:

* React 19;
* TypeScript 7;
* Vite 8;
* React Router 8;
* TanStack Query 5;
* Axios;
* Material UI 9;
* React Hook Form;
* Zod.

Назначение технологий:

* React — построение пользовательского интерфейса;
* TypeScript — типизация;
* Vite — сборка и development server;
* React Router — маршрутизация;
* TanStack Query — server state, cache и mutations;
* Axios — HTTP-клиент;
* Material UI — UI-компоненты;
* React Hook Form — управление формами;
* Zod — клиентская валидация форм.

Версии библиотек фиксируются в `frontend/package.json` и `frontend/package-lock.json`.

---

## 4. Архитектурный подход

Frontend использует **feature-oriented architecture**, согласованную с принципами Feature-Sliced Design.

Текущая реализация развивается от application shell к пользовательским features.

Основные цели:

* разделение ответственности;
* изоляция API-слоя от UI;
* отделение frontend models от backend DTO;
* повторное использование feature components;
* развитие одного пользовательского сценария за итерацию;
* отсутствие бизнес-логики в pages и UI-компонентах.

Архитектура не должна усложняться ради формального соответствия FSD. Новые уровни (`widgets`, `entities`, `shared`) добавляются только при наличии реальной потребности.

---

## 5. Фактическая структура frontend

Текущая структура проекта:

```text
frontend/src/

app/
    App.tsx
    router.tsx
    providers/
        QueryProvider.tsx

pages/
    orders/
        OrdersPage.tsx
        CreateOrderPage.tsx
        OrderPage.tsx

features/
    orders/
        api/
            getOrders.ts
            getOrder.ts
            createOrder.ts
            orderMapper.ts
            types.ts
        model/
            types.ts
            useOrders.ts
            useOrder.ts
        create-order/
            api/
            model/
            ui/
        register-order/
            api/
            model/
            ui/
        ui/
            OrderListItem.tsx
            OrderListEmpty.tsx
            OrderListError.tsx
            OrderActions.tsx
            OrderDetails.tsx
```

Структура является живой архитектурой: она уточняется по мере появления новых пользовательских сценариев.

---

## 6. Application shell

`app/App.tsx` является корневым компонентом приложения.

Текущая композиция:

```text
App
 ├── QueryProvider
 └── RouterProvider
```

`QueryProvider` предоставляет TanStack Query для работы с server state.

Маршрутизация определяется в `app/router.tsx`.

---

## 7. Маршрутизация

Фактически реализованы следующие маршруты:

```text
/orders
/orders/new
/orders/:orderId
```

Назначение:

* `/orders` — список заказов;
* `/orders/new` — создание заказа;
* `/orders/:orderId` — просмотр конкретного заказа.

Новые маршруты добавляются только вместе с соответствующим пользовательским сценарием.

---

## 8. Pages

Pages являются точками композиции пользовательского сценария.

Например, `OrdersPage`:

```text
OrdersPage
    ↓
useOrders()
    ↓
loading / error / empty / data
    ↓
OrderListItem
```

Page не должна содержать HTTP-запросы, бизнес-правила или сложную domain-specific логику.

Сложные действия и состояния выносятся в features и UI-компоненты.

---

## 9. Features

Feature представляет конкретное пользовательское действие или функциональный контур.

Уже реализованы:

### Orders

* получение списка заказов;
* получение заказа по ID;
* создание заказа;
* регистрация заказа.

### Create Order

Feature отвечает за форму создания заказа, её model/API/UI части и клиентскую валидацию.

### Register Order

Feature содержит:

* API mutation;
* React Query hook;
* кнопку регистрации;
* отображение ошибки.

После успешной регистрации cache конкретного заказа обновляется через TanStack Query.

---

## 10. Работа с API

Backend является источником истины.

Текущая схема взаимодействия:

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

API-логика находится внутри соответствующей feature, а не непосредственно в pages и UI-компонентах.

Для Orders backend DTO отделены от frontend models.

Например:

```text
OrderApiDto
    ↓
orderMapper
    ↓
OrderRead
```

Это позволяет не распространять backend naming и транспортные детали по всему UI.

Generated TypeScript API client пока не используется. Поэтому документация не должна утверждать, что frontend уже построен вокруг автоматически сгенерированного OpenAPI client.

---

## 11. Управление состоянием

Используется разделение server state и client state.

### Server State

TanStack Query используется для:

* загрузки данных;
* cache;
* mutations;
* обновления данных после действий пользователя;
* состояний loading/error.

### Client State

Локальное состояние используется только там, где оно действительно необходимо:

* состояние UI;
* состояние формы;
* временные данные взаимодействия пользователя.

Бизнес-данные не должны без необходимости дублироваться в глобальном client state.

---

## 12. UI-компоненты

UI-компоненты разделяются по ответственности.

Примеры текущей реализации:

* `OrderListItem` — отображение элемента списка;
* `OrderListEmpty` — пустое состояние списка;
* `OrderListError` — состояние ошибки;
* `OrderDetails` — отображение деталей заказа;
* `OrderActions` — композиция действий над заказом;
* `RegisterOrderButton` — кнопка регистрации;
* `RegisterOrderError` — ошибка регистрации.

Страницы не должны превращаться в большие монолитные компоненты.

Повторно используемые или feature-specific UI элементы выносятся из pages по мере необходимости.

---

## 13. Формы и валидация

Правила:

* формы реализуются через React Hook Form;
* схема проверки через Zod;
* frontend выполняет пользовательскую валидацию;
* backend остается источником истины для бизнес-валидации.

Frontend validation не заменяет backend validation.

---

## 14. Обработка состояний и ошибок

Каждый пользовательский сценарий должен явно учитывать:

* loading;
* success/data;
* empty state, если он применим;
* API error;
* mutation pending;
* mutation error.

Ошибки backend не должны молча подавляться.

HTTP-ошибки преобразуются в пользовательское состояние на соответствующем уровне feature/page.

---

## 15. Правила разработки

Соблюдаются принципы:

* один пользовательский сценарий за итерацию;
* небольшие изменения;
* анализ существующего кода перед изменением;
* разделение API, model и UI ответственности;
* отсутствие бизнес-логики в pages;
* проверка после каждого этапа;
* документация синхронизируется с кодом.

Workflow:

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

---

## 16. Frontend Definition of Done

Пользовательский сценарий считается завершенным, когда:

* определен пользовательский flow;
* необходимый backend API существует;
* API layer реализован;
* backend DTO отделены от frontend models, если это необходимо;
* React Query hook реализован для server state;
* UI реализован;
* loading/error/empty состояния обработаны;
* формы имеют клиентскую валидацию, если она нужна;
* typecheck проходит;
* build проходит;
* документация обновлена;
* изменения зафиксированы в Git и синхронизированы с GitHub.

---

## 17. Текущий implementation checkpoint

На текущем этапе реализован пользовательский контур Orders.

```text
Orders
  ├── list                 ✓
  ├── loading state        ✓
  ├── error state          ✓
  ├── empty state          ✓
  ├── create order         ✓
  ├── order details        ✓
  └── register order       ✓
```

Регистрация заказа использует mutation и после успешного выполнения обновляет cache соответствующего заказа.

Frontend application shell, routing, API integration и базовый Orders flow уже реализованы.

---

## 18. Production Runtime

Frontend production runtime использует статический Vite build, размещенный через nginx.

```text
Browser
    ↓
nginx
    ├── static React SPA
    │
    └── /api/*
          ↓
        FastAPI backend
```

SPA routing обслуживается через fallback на:

```text
/index.html
```

Production runtime **не требует постоянно работающего Vite development server**.

Vite development server используется только для локальной разработки и не является частью production deployment.

Frontend production deployment выполняется вручную. Автоматический deployment pipeline в текущей архитектуре не заявляется.

---

## 19. Frontend Roadmap

Дальнейшая разработка выполняется по пользовательским сценариям, а не по механическому заполнению каталогов.

Целевой workflow:

```text
audit current UI
        ↓
select one user scenario
        ↓
analyze existing backend API
        ↓
implement feature
        ↓
validate typecheck/build/tests
        ↓
update documentation
        ↓
sync GitHub
        ↓
next scenario
```

Следующий запланированный frontend сценарий:

```text
Customer selection flow
        ↓
Order creation
```

Перед реализацией необходимо проверить существующий Customer API и текущий Order creation contract, чтобы не дублировать backend functionality и не вводить frontend-specific business rules.

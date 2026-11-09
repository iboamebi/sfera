# Customer Application Design

## Статус

Этот документ заменяет ранний эскиз CustomerService. Описанная ниже бизнес-модель является актуальной и согласована с `docs/architecture/CUSTOMER_ORGANIZATION_SITE_MODEL.md`.

Customer и Organization — независимые сущности. Постоянная связь Customer–Organization не создаётся. Полный предметный контракт, правила Site/Instrument и этапы внедрения определены в документе модели.

## Customer

Customer — устойчивый клиентский контекст / заказчик сервисного центра.

- Customer может быть физическим лицом и существовать без Organization.
- Customer содержит собственные имя, контакты и общую информацию.
- Создание и редактирование Customer не требуют выбора Organization.
- Customer может иметь несколько Site.
- Заказ и принадлежность приборов относятся к Customer.

Текущий Domain contract:

- `id`;
- `name`;
- `contact_person?`;
- `phone?`;
- `email?`;
- `comment?`;
- `discount_percent`;
- `archived`.

В Customer не должно быть `organization_ids`, `organization_id` или иных постоянных ссылок на Organization.

## Organization

Organization — самостоятельная юридическая сущность с реквизитами.

- Все существующие Organization и их реквизиты сохраняются независимо от Customer.
- Organization не является дочерней записью Customer.
- Выбор Organization выполняется отдельно в документальном/финансовом контексте конкретного заказа.
- Не выводить связь по совпадению названий, ИНН или истории.

Выбор Organization для счёта и хранение соответствующего контекста заказа — отдельный этап. Invoice и финансовый модуль не входят в текущий Customer use case.

## Site и Instrument

- Site принадлежит одному Customer и представляет адрес / проектный узел.
- Customer может иметь ноль, один или несколько Site.
- Instrument принадлежит Customer напрямую.
- `Instrument.site_id` необязателен.
- Если Site указан, его `customer_id` должен совпадать с `Instrument.customer_id`.
- Закреплённый по проектной документации прибор нельзя произвольно переносить на другой Site.
- Изменение закрепления требует документированного основания и отдельного сценария с историей.

Операции поверки, ремонта и диагностики не должны требовать наличия Site.

## Order

- Order принадлежит одному Customer.
- Создание Order не требует Organization.
- Organization выбирается отдельно для документального/финансового контекста.
- Приборы добавляются в Order как конкретные OrderItems.
- Site используется для поиска/фильтрации приборов Customer, но выбор Site в заказе не меняет постоянный `Instrument.site_id`.
- В заказ можно включать приборы из нескольких Site и приборы без Site.
- При регистрации/поиске прибора при создании заказа поиск выполняется последовательно: сначала среди приборов выбранного Customer, затем в глобальной базе приборов Сферы, затем во внешнем ФГИС Аршин.
- Результат поиска в глобальной базе Сферы или Аршин не изменяет автоматически владельца прибора или его Site. Обнаружение совпадения является поиском, а не переносом принадлежности.
- Готовность Site для выдачи, если она будет реализована, рассчитывается только по приборам этого Site, включённым в конкретный Order.

## Архитектура

Сценарии реализуются через существующие DDD/Clean Architecture границы:

```text
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
```

API не обращается к Repository или ORM напрямую. Application использует Repository Interfaces. SQLAlchemy остаётся в Infrastructure.

## Validation

Проверять как минимум:

- Customer создаётся без Organization;
- Customer можно редактировать без выбора Organization;
- Organization и её реквизиты не зависят от Customer;
- Site принадлежит Customer;
- Instrument принадлежит Customer независимо от Site;
- при указанном Site Customer у Site и Instrument совпадает;
- отсутствие Site не блокирует создание или обработку прибора;
- Order создаётся без Organization;
- Order может содержать приборы из разных Site и без Site;
- выбор Site для поиска не меняет постоянное закрепление прибора.

Этапы реализации и статус миграции ведутся в `CUSTOMER_ORGANIZATION_SITE_MODEL.md` и `MIGRATION_MATRIX.md`.

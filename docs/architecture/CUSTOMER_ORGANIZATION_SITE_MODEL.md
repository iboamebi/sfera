# Customer / Organization / Site Model

## Статус

`DECIDED`

Бизнес-модель уточнена 2026-11-05. Customer и Organization являются независимыми сущностями. Site принадлежит Customer и используется для пространственной навигации и группировки приборов. Оператор выбирает необходимые Organization и Site при работе с заказом; интерфейс помогает найти и выбрать записи, но не создаёт постоянную связь Customer–Organization.

Документ не изменяет `PROJECT_CONSTITUTION.md`.

## 1. Сущности

### Customer — заказчик

Customer — устойчивый клиентский контекст, с которым сервисный центр работает по заказам.

- Customer существует независимо от юридических лиц и может быть физическим лицом.
- Customer не содержит список обязательных или заранее связанных Organization.
- Customer может иметь несколько Site.
- Заказ и принадлежность приборов относятся к Customer, а не к Organization.

### Organization — юридическое лицо

Organization — самостоятельная запись юридического лица с юридическими реквизитами.

- Organization не принадлежит Customer и не является его дочерней записью.
- Одна Organization может использоваться в контексте разных заказов.
- Записи Organization и все их реквизиты должны сохраняться независимо от изменений модели Customer.
- Наличие Organization не обязательно для создания Customer или заказа.
- Система не выводит связь Customer–Organization из совпадения названий, ИНН или исторических данных.

### Выбор Organization при работе с заказом

Оператор самостоятельно определяет, какая Organization относится к конкретному заказу и его документальному/финансовому контексту.

- Выбор делается в контексте заказа, а не путём создания постоянной связи Customer–Organization.
- Интерфейс помогает искать Organization и выбирать подходящую запись.
- Нельзя автоматически считать ранее использованную Organization окончательным выбором.
- Выбранную Organization можно уточнить при согласовании взаиморасчётов.
- Точная cardinality выбора Organization в одном заказе и способ хранения этого контекста должны быть определены отдельным этапом до реализации соответствующего persistence contract.
- Invoice и полноценный финансовый модуль не создаются в рамках этого этапа.

## 2. Site и Instrument

### Site — узел / адрес Customer

Site — известный узел, адрес или площадка Customer, используемая для поиска и группировки конкретных приборов.

```text
Customer 1:N Site
Site     1:N Instrument
Instrument 0..1 Site
```

Правила:
- Site принадлежит ровно одному Customer.
- У Customer может быть ноль, один или несколько Site.
- У Site есть собственные название и адрес.
- Один Instrument может быть закреплён максимум за одним Site.
- `Instrument.site_id` nullable. Неизвестный Site не блокирует работу с прибором.
- Если Site известен, Customer у Site и Instrument должен совпадать.
- Site используется для поиска приборов по адресу/узлу и для группировки работ.
- Отсутствие Site не означает, что прибор можно произвольно перемещать или закреплять за другим узлом.

### Контролируемое изменение Site

Если прибор закреплён за узлом по проектной документации, его нельзя произвольно перенести на другой Site.

Изменение закрепления требует документированного основания — например, нового проекта или согласованного изменения проектной документации. История должна позволять восстановить прибор, старый и новый Site, дату, пользователя и основание изменения.

Это отдельный бизнес-сценарий. Обычные поверка, ремонт, диагностика и другие операции не должны блокироваться отсутствием Site.

### Instrument — конкретное СИ

Instrument — конкретный экземпляр средства измерений. Он принадлежит Customer напрямую, даже если Site ещё неизвестен.

Целевая модель:
- `Instrument.customer_id` — обязательный владелец.
- `Instrument.site_id` — nullable дополнительная привязка к узлу.
- При наличии Site его `customer_id` должен совпадать с `Instrument.customer_id`.

Прямое владение Instrument через Customer и проверки согласованности Site внедряются отдельным техническим этапом.

## 3. Order и выбор приборов

```text
Order     → Customer   required
OrderItem → Instrument конкретный прибор в заказе
Order     → Organization не является постоянной принадлежностью Customer
Order     → Site        не является постоянной привязкой; Site определяется через выбранные Instrument
```

При создании и редактировании заказа оператор должен иметь возможность:

1. Выбрать Customer.
2. Найти и выбрать подходящую Organization для контекста заказа.
3. Найти Site этого Customer по названию или адресу.
4. Выбрать один или несколько Site как фильтр/контекст поиска приборов.
5. Увидеть приборы, закреплённые за выбранными Site.
6. Найти и добавить приборы Customer, у которых Site не указан.
7. Включить в заказ приборы из нескольких Site и приборы без Site.

Интерфейс помогает поиском, фильтрами и подсказками. Он не должен автоматически назначать Organization, менять постоянное закрепление Instrument за Site или ограничивать заказ только одним Site.

Выбор Site в интерфейсе заказа не меняет постоянный `Instrument.site_id`. Контекст Site для конкретного прибора определяется через Instrument.

### Готовность Site в заказе

Если в дальнейшем реализуется выдача по группам Site, учитываются только приборы данного Site, включённые в конкретный Order. Остальные приборы Site не должны блокировать выдачу по этому заказу. Разные Site одного Customer могут быть готовы и выдаваться независимо.

## 4. Очередь поверки

Очередь поверки — отдельный механизм производственного планирования.

- В очередь могут входить конкретные приборы из разных заказов и Site.
- Группировка в очереди не меняет Customer, Site, Order или OrderItem.
- Очередь не является группой выдачи.
- Состояние очереди само по себе не определяет готовность Site в заказе.

Правила совместимости методик, оборудования, исполнителей и сортировки очереди определяются отдельным этапом.

## 5. Сохранение и переход от старой модели

- Существующие Organization и их реквизиты сохраняются.
- Старые записи `customer_organizations` не считаются достоверными отношениями и не переносятся в новую модель.
- Связь Customer–Organization удаляется из ORM, Domain/Application repository contracts, Infrastructure, DI и API.
- Таблица `customer_organizations` удаляется отдельной Alembic-миграцией.
- Миграция не удаляет и не изменяет строки таблицы `organizations`.
- Старые тестовые или автоматически скопированные отношения не используются для назначения Organization заказу.
- Не создавать новую постоянную Customer–Organization связь под другим именем.

Историческая инвентаризация одной локальной базы показывала 162 Customer, 162 Organization, 16 строк `customer_organizations`, 27 Order и 41 Instrument. Эти цифры не являются гарантией текущего состояния других окружений и не используются миграцией как предположение.

## 6. Этапы реализации

1. Удалить устаревшую Customer–Organization association, сохранив Organization и реквизиты.
2. Добавить прямое владение Instrument через Customer и проверку согласованности Instrument/Site/Customer. Реализовано в backend.
3. Удалить устаревшую связь Order–Site после проверки зависимостей; Site для OrderItem получать через Instrument. Реализовано в backend.
4. Частично реализовать поиск Site/Instrument в интерфейсе заказа: фильтр по нескольким Site и отдельное включение СИ без Site добавлены в order-item selector. Выбор Organization и persistence order context остаются открытыми до отдельного решения о cardinality и контракте хранения.
5. Реализовать контролируемое изменение Instrument–Site с основанием и историей.

Каждый этап проверяется и фиксируется отдельно.


## 7. Clean-slate data reset — 2026-11-05

The user approved a one-time reset of the current untrusted business data before operational use.

- Preserve every `organizations` row and all legal requisites unchanged.
- Preserve the existing `alex` account with `admin` role; preserve its password and account settings.
- Remove current Customer, Site, Instrument, Order, production, verification, repair, diagnostic, document, warehouse, price-list and reference/master-data rows. Future records will be entered by an operator or imported from XLS.
- Do not infer or reconstruct ownership, Customer–Organization links, Site assignments or instrument relations from the discarded data.
- This is a data reset, not a cancellation of the business model above. The agreed Customer / Site / Instrument rules remain the target for future data entry and implementation.
- See Alembic revision `a6c8e1f3b520` and the 2026-11-05 checkpoint in `docs/AI_CONTEXT.md` for the exact preservation boundary.

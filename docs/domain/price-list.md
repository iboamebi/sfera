# Price List Domain Design

## 1. Назначение

Модуль PriceList отвечает за управление стоимостью услуг и материалов сервисного центра.

Основные задачи:

- хранение прайс-листов;
- хранение стоимости услуг;
- хранение стоимости материалов;
- применение цен при создании заказов;
- формирование расчётов стоимости работ;
- подготовка коммерческих предложений.

Модуль используется для:

- поверки средств измерений;
- ремонта;
- диагностики;
- продажи материалов;
- дополнительных услуг.


## 2. Domain Context

PriceList является отдельным доменным контекстом.

Связи:

Customer

    |
    v

Order

    |
    +---- Verification
    |
    +---- Repair
    |
    +---- Diagnostic

            |
            v

       PriceList


PriceList не зависит от Order.

Order получает стоимость через Application Layer.


## 3. Основные сущности


## PriceList

Aggregate Root.

Назначение:

- объединяет набор цен;
- управляет состоянием прайс-листа;
- содержит позиции стоимости.


Поля:
id
name
description
price_list_type
currency
valid_from
valid_to
is_active
created_at
updated_at



Типы:
VERIFICATION
REPAIR
DIAGNOSTIC
MATERIAL
GENERAL



## PriceListItem

Элемент прайс-листа.


Поля:
id
price_list_id

service_code
name
description

unit
price

created_at
updated_at



Пример:
VER-001
Поверка мультиметра
1500 RUB

REP-010
Замена платы
3500 RUB

MAT-001
Кабель
450 RUB



# 4. Domain Rules


## PriceList Rules

- название обязательно;
- прайс-лист может быть активным или архивным;
- цены имеют период действия;
- история цен сохраняется;
- удаление активных цен запрещено.


## PriceListItem Rules

- цена не может быть отрицательной;
- код услуги обязателен;
- код услуги уникален внутри прайс-листа;
- позиция принадлежит одному PriceList.


# 5. Aggregate Structure

PriceList Aggregate Root

    |
    |
    +---- PriceListItem
    |
    +---- PriceListItem
    |
    +---- PriceListItem


PriceListItem не существует отдельно от PriceList.
# 6. Application Layer


Application Service:


PriceListApplicationService



Commands:


CreatePriceList

UpdatePriceList

ActivatePriceList

DeactivatePriceList

AddPriceListItem

UpdatePriceListItem

RemovePriceListItem



Queries:


GetPriceList

GetActivePriceList

GetPriceByServiceCode

ListPriceLists



# 7. Repository


Domain Interface:



PriceListRepository



Методы:


get_by_id()

get_active()

save()

delete()

find_price()

list()



Infrastructure implementation:



SQLAlchemyPriceListRepository



# 8. API


Endpoints:



GET /price-lists

POST /price-lists

GET /price-lists/{id}

PUT /price-lists/{id}

DELETE /price-lists/{id}

POST /price-lists/{id}/items

GET /price-lists/{id}/items

PUT /price-lists/{id}/items/{item_id}

DELETE /price-lists/{id}/items/{item_id}



# 9. Integration


Order Application Service:



OrderApplicationService

    |
    v

PriceListApplicationService

    |
    v

PriceListRepository



Расчёт стоимости:



OrderItem

|
v

ServiceCode

|
v

PriceList lookup

|
v

Calculated Amount



# 10. Будущие расширения


Планируется:


- индивидуальные цены клиента;
- скидки;
- договорные цены;
- история изменения стоимости;
- импорт XLSX;
- экспорт прайс-листов;
- коммерческие предложения;
- расчёт себестоимости.


# Status


Architecture baseline:

v2.0-architecture


Implementation order:


1. Domain Entity

2. Domain Exceptions

3. Repository Interface

4. SQLAlchemy Models

5. Mapper

6. Repository Adapter

7. Application Service

8. API Router

9. Tests

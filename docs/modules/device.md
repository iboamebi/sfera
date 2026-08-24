# Модуль Device

**Версия:** 1.1
**Дата актуализации:** 2026-07-16

---

# 1. Назначение

Device реализует управление средствами измерений в системе «Сфера».

Модуль отвечает за:

- хранение данных о средствах измерений;
- идентификацию приборов;
- историю производственных операций;
- связь с поверкой и ремонтом.

---

# 2. Роль Device в системе

Средство измерения является объектом производства.

Основная связь:

```text
Customer

↓

Instrument

↓

OrderItem

↓

Production Process
```

---

# 3. Основная сущность

```text
Device
```

Device представляет конкретное средство измерения.

---

# 4. Данные устройства

Хранятся:

- регистрационный номер;
- заводской номер;
- наименование;
- тип;
- модель;
- производитель;
- владелец;
- состояние.

---

# 5. Жизненный цикл

Пример состояний:

```text
REGISTERED

↓

AVAILABLE

↓

IN_SERVICE

↓

VERIFICATION

↓

REPAIR

↓

ARCHIVED
```

---

# 6. Идентификация

Основные идентификаторы:

```text
Registry Number

Serial Number

Label
```

---

# 7. Связь с заказом

Device участвует в работе через:

```text
OrderItem
```

Пример:

```text
Order

↓

OrderItem

↓

Device

↓

Verification / Repair
```

---

# 8. Domain Model

Основные компоненты:

```text
Device Entity

DeviceStatus

DeviceFactory

DeviceRepository

DeviceDomainEvents
```

---

# 9. Domain Events

События:

```text
DeviceCreated

DeviceConnected

DeviceDisconnected

DeviceStatusChanged
```

---

# 10. Application Services

Основной сервис:

```text
DeviceService
```

Операции:

```text
Create Device

Update Device

Get Device History

Change Status
```

---

# 11. Repository

Интерфейс:

```text
DeviceRepository
```

Реализация:

```text
SQLAlchemyDeviceRepository
```

---

# 12. Ограничения

Запрещается:

- создавать дубликаты идентификаторов;
- удалять историю операций;
- изменять юридически значимые данные без аудита.

---

# 13. Интеграция с Аршин

Данные Device используются при подготовке экспорта:

```text
Device

↓

Verification

↓

ArshinExport
```

Используются:

- регистрационный номер;
- серийный номер;
- модификация;
- владелец.

---

# 14. Тестирование

Проверяются:

- создание устройства;
- уникальность идентификаторов;
- изменение состояния;
- связь с заказом;
- формирование истории.

---

# 15. Главный принцип

Device является источником идентификационных данных средства измерения и обеспечивает непрерывность истории его эксплуатации в системе «Сфера».

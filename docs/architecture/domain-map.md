# SFERA Domain Map

## Core

- Order
- Customer
- Organization
- Instrument
- InstrumentType
- Methodology

## Production

- Verification
- Calibration
- Diagnostic
- Repair
- ProductionOperation

## Warehouse

- Warehouse
- Material
- Stock
- Movement
- Purchase
- Supplier

## Finance

- PriceList
- Quote
- Invoice

## Documents

- Document
- Template
- Label
- PrintJob

## Identity

- User
- Role
- Permission

## Integration

- ArshinExport
- DeviceGateway
- Notification

## System

- Audit
- Settings
- ReferenceData

---

# Aggregate Roots

- Order
- Customer
- Organization
- Warehouse
- Material
- PriceList
- Document
- User
- Role
- Methodology
- InstrumentType
- Supplier
- Purchase

---

# Child Entities

- OrderItem
- Verification
- Calibration
- Diagnostic
- Repair
- Movement
- Stock
- QuoteItem
- InvoiceItem
- Label

---

# Value Objects

- OrderNumber
- SerialNumber
- InventoryNumber
- RegistryNumber
- Money
- Address
- Phone
- Email
- Temperature
- Pressure
- Humidity
- DateRange
- Priority
- OrderStatus
- VerificationResult

---

# Engines

- MetrologyEngine
- CalculationEngine
- RuleEngine
- DocumentEngine
- PrintEngine
- ExportEngine
- NotificationEngine

# Historical plan audit — Step 29: Diagnostics, Repair and recommendations

**Audit date:** 2026-11-16  
**Repository branch inspected:** `develop`  
**Inspected commit:** `bb0d3279de58528cb8c8c12ef0d38862317af36d`  
**Status:** `PARTIALLY_EVOLVED` — basic Diagnostic and Repair processes exist and are linked to Order items; defect records, explicit Diagnostic↔Repair association, repair operations, material consumption integration, repeat-repair analytics, and commercial proposals are not implemented in the inspected code.

## 1. Historical intent

Step 29 described a complete workflow for an Instrument that may be faulty:

1. Perform diagnostics in the context of an Order item.
2. Record the conclusion, detected defects, severity, and controlled recommendation.
3. Offer the appropriate next actions (repair, adjustment, replacement, write-off, return to manufacturer).
4. If repair is selected, track the repair lifecycle and individual operations.
5. Reserve, issue, consume, and account for materials through the warehouse.
6. Preserve repair history and support analysis of repeated faults/repairs.
7. After repair, allow a new Verification record without overwriting an earlier Verification.
8. Prepare a commercial proposal based on work, materials, price lists, and customer discounts.

The proposed table/field names and statuses are historical design, not the current technical contract.

## 2. Actual implementation found in develop

### 2.1 Diagnostics

Relevant sources:

- `backend/app/domains/diagnostic/entities/diagnostic.py`
- `backend/app/domains/diagnostic/value_objects/recommendation.py`
- `backend/app/application/diagnostic/services/diagnostic_application_service.py`
- `backend/app/api/routers/diagnostic.py`
- `backend/app/schemas/diagnostic.py`
- `backend/app/models/diagnostic.py`
- `backend/app/infrastructure/diagnostic/diagnostic_repository.py`
- `backend/app/infrastructure/mappers/diagnostic_mapper.py`

Current Diagnostic stores:

- `order_item_id` (required);
- optional free-text `conclusion`;
- optional controlled `recommendation`.

The recommendation enum already contains the six values from the historical plan:

- `NO_ISSUES`
- `REPAIR_REQUIRED`
- `REPLACEMENT_RECOMMENDED`
- `REPAIR_NOT_ECONOMIC`
- `WRITE_OFF`
- `RETURN_TO_MANUFACTURER`

Application use cases currently support create, complete with a conclusion, and set recommendation. Mutations require `TECHNICIAN` or `ADMIN`. Diagnostic completion writes an Audit record.

The API exposes:

- `POST /diagnostics`
- `GET /diagnostics/{diagnostic_id}`
- `POST /diagnostics/{diagnostic_id}/conclusion`
- `POST /diagnostics/{diagnostic_id}/recommendation`

The current model does not store `instrument_id` directly; it is reached through OrderItem. It does not store a diagnostic date, assigned employee, normalized diagnostic result, recommendation history, or separate Defect records with severity. Conclusion remains free text.

The frontend has a basic diagnostic detail page showing Order item, conclusion, and recommendation. No complete guided diagnostic workflow or defect-entry UI was found in the inspected paths.

### 2.2 Repair

Relevant sources:

- `backend/app/domains/repair/entities/repair.py`
- `backend/app/domains/repair/value_objects/repair_status.py`
- `backend/app/application/repair/services/repair_application_service.py`
- `backend/app/api/routers/repair.py`
- `backend/app/schemas/repair.py`
- `backend/app/models/repair.py`
- `backend/app/infrastructure/repair/repair_repository.py`
- `backend/app/infrastructure/mappers/repair_mapper.py`

Current Repair stores:

- required `order_item_id`;
- `status`;
- optional free-text `description`;
- optional free-text `result`.

Current statuses are:

```text
NEW → IN_WORK → WAITING → COMPLETED
  └──────────────────────→ CANCELLED
```

Application use cases support create, start, complete, cancel, and get. Mutations require `TECHNICIAN` or `ADMIN`. Repair completion writes an Audit record.

The API exposes:

- `POST /repairs`
- `GET /repairs/{repair_id}`
- `POST /repairs/{repair_id}/start`
- `POST /repairs/{repair_id}/complete`
- `POST /repairs/{repair_id}/cancel`

Differences from historical proposal:

- `WAITING` is the current status name; there is no distinct `PLANNED` or `WAITING_PARTS`.
- The aggregate does not store `diagnostic_id`, start/completion timestamps, assigned employee, or repair operations.
- There is no `repair_operations` model/API.
- No normalized fault/repair-operation catalogue was found.
- Repair history is persisted as separate Repair records associated with Order items; there is no dedicated repair analytics/reporting implementation.

The frontend has a basic Repair detail page showing Order item, status, description, and result.

### 2.3 Relationship between Diagnostic and Repair

Both aggregates are linked to the same Order item, but the current Repair model has no `diagnostic_id` and the Diagnostic model has no direct repair relation.

The application service does not automatically create a Repair from `REPAIR_REQUIRED`, nor create a replacement/stock-offer workflow for other recommendations.

A recommendation is currently a controlled value stored on Diagnostic. It is not yet a workflow/action plan with generated downstream records.

### 2.4 Warehouse and material consumption

Relevant existing warehouse sources:

- `backend/app/domains/warehouse/entities/warehouse_stock.py`
- `backend/app/domains/warehouse/entities/warehouse_movement.py`
- `backend/app/application/warehouse/services/warehouse_application_service.py`
- `backend/app/models/material.py`
- `backend/app/models/warehouse_stock.py`
- `backend/app/models/warehouse_movement.py`

Current warehouse foundations include stock balances, reserved quantity, reserve/release operations, and movement records. Material master data currently includes name, optional article, unit, and description.

However, the inspected implementation does not connect a material requirement or consumption record to a specific Repair or repair operation:

- no `repair_materials` persistence;
- no Repair-linked reservation;
- no issue-to-performer operation;
- no material write-off/consumption workflow tied to Repair completion;
- no return of unused issued materials tied to a Repair.

The existing stock reserve/release and movement operations are separate warehouse capabilities. They must not be described as a completed repair-material workflow. The previously recorded Step 30 warehouse audit documents additional gaps in movement/stock consistency and warehouse flows.

### 2.5 Repeat Verification after Repair

Verification already exists as an independent aggregate associated with an Order item and Instrument. It preserves separate verification records, has its own lifecycle and immutable audit trail, and supports later decisions/corrections with reasons.

The Repair application service currently does not create or schedule a Verification after completion. There is no direct Repair↔Verification association or explicit post-repair handoff workflow in the inspected code.

A later Verification must be a new record/fact. It must not overwrite the result of a previous Verification. The exact business trigger and whether post-repair Verification is mandatory depend on the Instrument and applicable requirements; do not infer it for every repair.

### 2.6 Price lists and commercial proposals

Current price-list module exists:

- `backend/app/domains/price_list/entities/price_list.py`
- `backend/app/domains/price_list/entities/price_list_item.py`
- `backend/app/application/price_list/services/price_list_application_service.py`
- `backend/app/api/routers/price_list.py`
- `backend/app/api/routers/price_list_item.py`
- `backend/app/models/price_list.py`
- `backend/app/models/price_list_item.py`

Price lists support type, currency, validity dates, activation, and items with service code, name, price, unit, and description.

This is a service price catalogue, not a commercial proposal/quotation or financial accounting module. The inspected code does not demonstrate:

- proposal/quotation aggregate and lifecycle;
- proposal lines generated from repair operations/materials;
- customer-specific discounts or discount rules;
- replacement instrument offers;
- approval/acceptance/rejection by Customer;
- invoice/payment/revenue/cost accounting;
- conversion from accepted proposal to Order or work;
- standalone material sales.

The price list must not be treated as actual revenue or as a completed financial integration. Step 33 audit records the broader finance/reporting limitations.

## 3. Status by historical requirement

| Requirement | Current assessment |
|---|---|
| Diagnostic created for Order item | Implemented |
| Diagnostic conclusion | Implemented as free text |
| Controlled recommendation list | Implemented |
| Diagnostic date/responsible employee | Not found |
| Normalized diagnostic result catalogue | Not found |
| Defect records and severity | Not found |
| Guided next actions from recommendation | Not implemented |
| Repair created for Order item | Implemented |
| Repair lifecycle | Partially implemented |
| Repair linked to originating Diagnostic | Not implemented |
| Repair operations and time/performer | Not found |
| Repair-linked material requirements | Not found |
| Repair-linked reserve/issue/consumption/write-off | Not implemented |
| Repeat repair history | Basic records exist; analytics not implemented |
| New Verification after Repair | Verification module supports separate records; no Repair handoff |
| Service price list | Implemented |
| Commercial proposal for repair/replacement | Not found |
| Proposal approval and conversion to work/order | Not found |
| Diagnostic and Repair basic detail pages | Implemented |

## 4. Important boundaries for future design

### 4.1 Do not conflate Diagnostic, Repair, Verification, and Order

They are distinct production facts/processes:

- Diagnostic records what was examined, what was found, and what is recommended.
- Repair records the actual repair work and its outcome.
- Verification records a metrological verification execution and decision.
- Order/OrderItem provides the Customer-facing work context.

One Order item may be associated with multiple operations over time. The exact cardinality and allowed sequences should be defined without collapsing all work into one status or overwriting earlier records.

### 4.2 Recommendation is not automatic authorization

A recommendation such as repair, replacement, write-off, or return to manufacturer should make appropriate next actions available. It does not by itself mean the Customer has approved paid work, a new Order has been created, or the Instrument has been written off.

Commercial approval/acceptance and operational execution are separate facts. Preserve the recommendation even if the Customer declines the proposal.

### 4.3 Preserve history and context

- A completed Diagnostic is a historical finding; later repair does not rewrite it.
- A Repair is a separate record; repeat repair creates another traceable event/work record.
- A later Verification is a new Verification record; never overwrite a previous result.
- Changes to current Instrument ownership/Site must not rewrite historical Order, Diagnostic, Repair, Verification, or Audit context.

### 4.4 Repair materials need a full stock lifecycle

A material requirement, reservation, physical issue, actual consumption/write-off, and return of unused material are different events/quantities. A reserve is not consumption. A warehouse movement record is not necessarily a stock-balance mutation unless the corresponding transaction actually updates both consistently.

Material consumption must be attributable to the relevant Repair and, if useful, a particular operation. It should be possible to distinguish planned from actual quantity.

### 4.5 Fault analytics require structured data

Free-text conclusions/results are useful for operators but insufficient for reliable statistics on repeated faults, repair frequency, common defects, and repair economics. Structured defect/failure codes may be introduced incrementally, without losing the original free-text description and without forcing an exhaustive defect catalogue at intake.

### 4.6 Commercial documents depend on the Customer/Organization model

The Customer is the durable client/owner context; Organization is selected in the billing/document context. A proposal should be addressed to the appropriate Customer and use the selected Organization's requisites when required. Do not make an Organization mandatory at initial diagnostic or repair intake.

## 5. Open questions

1. Can multiple Diagnostics exist for one Order item (e.g. initial inspection and follow-up), and when is a Diagnostic considered complete?
2. Can multiple Repairs exist for one Order item, including repeated repair attempts or repair after an unsuccessful Verification?
3. Which Diagnostic conclusions/recommendations require Customer approval before paid Repair or replacement?
4. Is repair always created within the same Order, or can it require a separate/additional Order after a proposal is accepted?
5. Which repair operations and labor-time facts must be recorded, and is employee assignment required at creation or only during execution?
6. Which materials are reservable, when are they issued, how is actual consumption confirmed, and how are unused materials returned?
7. Which repair outcomes require a new Verification, and how is that determined from the Instrument type/method and applicable regulation?
8. What is the lifecycle and approval mechanism for a commercial proposal, including partial acceptance, expiry, revisions, and conversion to work?
9. How are replacement instruments selected/priced, and is the replacement a new Instrument identity linked to the replaced one?
10. Which repair/diagnostic document types are required, generated from templates, and associated with the specific Diagnostic/Repair?

## 6. Recommended next analysis

Before changing code:

1. Review real diagnostic and repair examples, including cases where repair is declined, impossible, or repeated.
2. Define the Diagnostic → recommendation → Customer decision → Repair/replacement/return/write-off path as separate events and use cases.
3. Reconcile repair material consumption with the existing Warehouse module and the Step 30 audit; design a single stock transaction lifecycle rather than a parallel repair-only stock ledger.
4. Define post-repair Verification trigger using actual instrument/method requirements and preserve prior Verification facts.
5. Review Customer/Organization billing context and document requirements before designing commercial proposals.
6. Introduce structured defect/operation catalogues only to the extent justified by real recurring work; retain free-text detail.

No application code, database schema, API behavior, or frontend behavior was changed by this audit. Historical requirements remain relevant unless explicitly superseded by a later business decision.

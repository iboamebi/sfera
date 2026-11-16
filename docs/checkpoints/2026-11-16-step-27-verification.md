# Historical plan audit — Step 27: Verification of measuring instruments

**Audit date:** 2026-11-16  
**Repository branch inspected:** `develop`  
**Inspected commit:** `1cc7d6738cf261ef3f74adfaa92154ca79294271`  
**Status:** `PARTIALLY_EVOLVED` — the basic verification lifecycle exists; method-specific execution, verification tools, documents, and Arshin export are not implemented as described by the historical plan.

## 1. Historical intent

Step 27 described the end-to-end verification process:

- one verification is created for a concrete Order item and Instrument;
- the verification lifecycle progresses from registration to execution and a final suitability decision;
- the result and its evidence remain associated with that particular verification, independently of later repair or subsequent verification work;
- suitability requires a validity date where applicable; unsuitability requires a reason;
- the applied methodology and verification tools are recorded;
- export eligibility is evaluated per verification record;
- only complete, validated records explicitly allowed for export are included in the Arshin XLSM file;
- generated verification documents and export history are linked to the relevant verification.

The original proposed status names were `NEW → IN_WORK → COMPLETED → APPROVED`. These are historical names, not the current lifecycle contract.

## 2. Actual implementation found in develop

### 2.1 Verification aggregate and lifecycle

Relevant code:

- `backend/app/domains/verification/entities/verification.py`
- `backend/app/domains/verification/value_objects/verification_status.py`
- `backend/app/domains/verification/value_objects/verification_result.py`
- `backend/app/application/verification/services/verification_application_service.py`
- `backend/app/api/routers/verification.py`
- `backend/app/api/routers/verification_actions.py`
- `backend/app/models/verification.py`
- `backend/app/infrastructure/verification/verification_repository.py`
- `backend/app/infrastructure/mappers/verification_mapper.py`
- `backend/app/schemas/verification.py`

The current lifecycle is:

```text
CREATED → IN_PROGRESS → DECIDED
                         ├── SUITABLE
                         └── UNSUITABLE
```

- `CREATED`: verification registered, execution has not started.
- `IN_PROGRESS`: execution started; `started_at` records the actual start.
- `DECIDED`: a final decision has been recorded.
- `SUITABLE` / `UNSUITABLE` are result values, not statuses.
- `CANCELLED` is also persisted for cancellation of a created or active verification.

Application use cases include create, start, approve, reject, cancel, correct decision, and correct validity date. Mutating operations require `METROLOGIST` or `ADMIN` and write audit records within the same Unit of Work.

### 2.2 Order and Instrument relationship

Creation accepts `order_item_id`, loads the Order and the corresponding item, and derives the concrete `instrument_id` from that item. Creation is rejected if the item has no Instrument.

The database has a partial unique index allowing at most one unarchived active verification (`CREATED` or `IN_PROGRESS`) per Order item. A previously decided record does not block a later verification for that item.

This implements the essential association with a concrete Order item and Instrument. The precise business cardinality for repeated attempts within one Order should be read together with the later rule that repeat work must not rewrite an already completed verification.

### 2.3 Result and validity invariants

The current result is an enum with `SUITABLE` and `UNSUITABLE`; a separate `verification_results` reference table from the historical plan is not present.

Current Domain rules include:

- suitable decision requires `valid_until`;
- unsuitable decision requires a non-empty `unsuitable_reason`;
- unsuitable decision has no `valid_until`;
- decision can be made only from `IN_PROGRESS`;
- a correction to a decided result requires a reason and is audited;
- validity-date correction requires a reason and is audited.

The current code records a final decision, but it does not yet derive that decision from a complete set of method-specific measurements, calculations, and acceptance evaluations.

### 2.4 Methodology

Current persistence contains both:

- `backend/app/models/methodology.py`: name, optional code, document number, version, description;
- `backend/app/models/verification_method.py`: code, name, description, active flag.

However, the Verification aggregate currently stores `methodology` as an optional string, not a foreign key to a versioned method. The current `InstrumentType` model does not expose the historical `instrument_type_methods` association.

The repository also contains methodology architecture and metrology documents:

- `docs/architecture/VERIFICATION_METHOD_MODEL_ANALYSIS.md`
- `docs/metrology/VERIFICATION_METHODS.md`
- `docs/metrology/verification_methods/`

The architecture distinguishes Method / MethodVersion / MethodVariant from the facts of a particular Verification. This is a later, more developed direction than the original simple `verification_methods` table. The current ORM models do not yet implement that complete versioned association.

### 2.5 Verification tools and method execution evidence

The inspected current tree contains no `verification_tools` persistence model or association for internal/external verification equipment.

The inspected Verification aggregate and API do not persist method-specific conditions, operations, measurement points, measurements, calculations, metrological characteristics, or acceptance evaluations.

These are not safely replaceable by a generic free-text field. Their required structure depends on the actual MethodVersion and the real verification protocol.

### 2.6 Documents

Current generic `Document` persistence contains an optional `order_id`, optional template ID, name, file path, and comment.

The inspected model does not provide a direct Verification-to-Document relationship or explicit document kinds for protocol, certificate, or notice of unsuitability. No complete verification document generation flow was found in the inspected paths.

### 2.7 Arshin export

Current code contains `backend/app/models/arshin_export.py`, with:

- `verification_id`;
- `file_name`;
- `exported_at`;
- optional `exported_by`;
- optional `comment`.

The current model does not contain the historical per-record flags `export_to_arshin` and `exported_to_arshin`. Migration `c5ce4959d90d_remove_obsolete_arshin_export_flags.py` explicitly removed those flags.

No current Arshin export Application service, API router, XLSM generation implementation, per-record preview, eligibility validator, or export workflow was found in the inspected repository tree. The presence of the `ArshinExport` model alone does not establish that export is implemented.

The existing `docs/modules/arshin.md` describes intended export behavior, but parts of it are not reflected in the current code. Treat it as a requirements/design document, not proof of implementation.

### 2.8 Frontend

The current frontend has verification list and detail pages and actions for creation, start, approve, reject, cancellation, and corrections.

The frontend supports the implemented basic lifecycle. No method-specific measurement workflow, verification-tool entry, document generation, or Arshin export UI was found in the inspected frontend paths.

## 3. Status by historical requirement

| Requirement | Current assessment |
|---|---|
| Create verification from an Order item | Implemented |
| Bind verification to a concrete Instrument | Implemented |
| Separate registration from actual start | Implemented |
| Final suitable / unsuitable decision | Implemented at basic record level |
| Validity date required for suitable result | Implemented |
| Unsuitability reason required | Implemented |
| Preserve separate verification records over time | Partially implemented; active-record uniqueness and repeat semantics need to be considered |
| Versioned methodology linked to Instrument Type | Open / partially evolved in design documents |
| Internal and external verification tools | Not found in current implementation |
| Method-specific operations, measurements and calculations | Not found in current implementation |
| Per-verification document linkage and generation | Not found in current implementation |
| Per-record Arshin export eligibility | Not implemented in current code; old flags were removed |
| XLSM generation and validation | Not found in current implementation |
| Arshin export history | Persistence model exists; workflow/API not found |
| Verification list/detail and lifecycle UI | Implemented for the basic lifecycle |

## 4. Important evolution beyond the historical plan

The later architecture documents materially refine the original plan:

1. `Verification` is a process aggregate, not merely a row containing a result.
2. A final decision must be supported by the facts and evaluations required by the applicable method.
3. Method / MethodVersion / MethodVariant describe normative rules; a Verification records the actual execution and evidence.
4. There must not be a universal fixed set of measurement fields or a generic calculation engine imposed on every type of Instrument.
5. Insufficient data is not the same as an unsuitable Instrument. The Verification remains in progress until the method-specific decision conditions are met.
6. A later repair or repeat verification must not silently overwrite the facts and result of an earlier verification.
7. Audit Trail records changes and corrections, but it does not replace the detailed metrological evidence of the verification itself.

Relevant current design documents:

- `docs/modules/verification.md`
- `docs/architecture/VERIFICATION_AGGREGATE_MODEL.md`
- `docs/architecture/VERIFICATION_DOMAIN_MODEL.md`
- `docs/architecture/VERIFICATION_LIFECYCLE_AND_INVARIANTS.md`
- `docs/architecture/VERIFICATION_METHOD_MODEL_ANALYSIS.md`
- `docs/modules/arshin.md`
- `docs/metrology/VERIFICATION_METHODS.md`

## 5. Boundaries and open questions

These points must not be decided by mechanically restoring the historical schema:

- Define when a repeat verification is a new record within the same Order item versus a new Order item or separate work scenario. Preserve all previous decisions.
- Determine the actual lifecycle meaning of “completed” versus “approved” if a future workflow needs separate technical completion, review, and legal/authorized decision. The current contract has one final `DECIDED` state.
- Define the method/version selection and effective-date rules using the actual methodology documents and instrument type/modification/production period.
- Define which verification tools are mandatory for each method and how their calibration/validity is checked.
- Define which method-specific facts must be stored before the final decision can be made.
- Define the document types, generation templates, file storage, and relationship to a particular Verification.
- Recover the actual Arshin XLSM template and authoritative field mapping before implementing export. The historical column map must be validated against the current template and current FGIS requirements.
- Define per-record export opt-out, validation errors, retry, repeat export, and confirmation semantics without restoring the removed flags blindly.
- Confirm whether Arshin export is file preparation only, actual submission, or both; distinguish file generation from successful external acceptance.

## 6. Recommended next analysis

Before changing code:

1. Read the actual methodology registry and the existing Verification lifecycle/invariant documents.
2. Review representative real completed verification protocols and the current Arshin XLSM template, when supplied/available.
3. Trace current Document and file-storage contracts.
4. Define the smallest concrete method-specific execution scenario from a real instrument type.
5. Design Arshin export only after the current template and required data sources are verified.

No application code, database schema, or API behavior was changed by this audit. The historical requirements remain relevant unless explicitly superseded by a later business decision.

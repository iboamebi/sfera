# Historical plan audit — Step 28: Documents, Instrument passports and duplicates

**Audit date:** 2026-11-16  
**Repository branch inspected:** `develop`  
**Inspected commit:** `9ffdae1a6bfffaf5a4617246fc479b0b967e1661`  
**Status:** `PARTIALLY_EVOLVED` — basic Document and DocumentTemplate persistence models exist; the document lifecycle, Instrument passport records, duplicate relationships, version history, and dedicated file-storage capability from the historical plan were not found in the inspected implementation.

## 1. Historical intent

Step 28 proposed one document-management capability for documents related to Instruments, Orders, and production operations.

Its key business rules:

- An Instrument passport is a document associated with the Instrument card.
- If the passport is lost, a duplicate is issued as a new document/record.
- The original passport and its history remain available.
- Documents and their history are not physically deleted.
- Changes and versions are traceable.
- Documents may be generated from templates, uploaded, or created by production processes.
- Documents may be related to Instruments, Orders, Verifications, Repairs, Diagnostics, and Organizations.

The proposed tables (`documents`, `document_types`, `document_links`, `instrument_passports`, `document_relations`, `document_duplicate_reasons`, `document_versions`, `files`) are a historical conceptual design, not a current database contract.

## 2. Actual implementation found in develop

### 2.1 Document ORM model

Source: `backend/app/models/document.py`

The current `Document` model contains:

- inherited `id`, `created_at`, `updated_at`, and `archived` from `BaseModel`;
- optional `order_id` foreign key to `orders.id`;
- optional `document_template_id` foreign key to `document_templates.id`;
- required `name`;
- optional `file_path`;
- optional `comment`.

This is a basic persistence record. It does not currently contain the historical document number/series/type/status, Instrument foreign key, Verification/Repair links, file metadata/hash, or version number.

The model's `archived` flag is not evidence of a complete document archive workflow, lifecycle, or immutable version history.

### 2.2 Document templates

Source: `backend/app/models/document_template.py`

The current `DocumentTemplate` model contains:

- inherited `id`, timestamps, and `archived`;
- `name`;
- `document_type` as a string;
- `version` as a string;
- optional `template_path`;
- optional `description`.

A template has a version label. This is not the same as versioning generated/issued document instances. The model does not establish template approval/effective-date rules or a reproducible document-generation pipeline.

### 2.3 Application, API, and frontend

The inspected repository tree contains no dedicated Document domain/Application/Infrastructure implementation, Document API router/schema, or frontend Document feature/page.

The paths `backend/app/api/routers/document.py`, `backend/app/schemas/document.py`, and `backend/app/application/document/services/document_application_service.py` do not exist at the inspected commit.

Therefore the presence of ORM models alone must not be described as a working document-management module or public API.

### 2.4 Instrument association

Source: `backend/app/models/instrument.py`

The current Instrument model has no direct relationship/foreign key to a passport or Document collection.

The existing `InstrumentLabel` model in `backend/app/models/instrument_label.py` is for QR/barcode/DataMatrix labels. It is not a passport, a document attachment, or a document version record.

The current Instrument model and its label model must not be repurposed as document storage without a deliberate domain design.

### 2.5 File storage

The current Document model stores an optional `file_path` string. The inspected backend tree contains no dedicated file-storage service/adapter or separate `files` persistence model matching the historical proposal.

A path string does not establish:

- where binary data is stored;
- whether files are private and access-controlled;
- how uploads/downloads are authorized;
- whether file hashes and sizes are checked;
- whether old file contents remain immutable;
- how backup, retention, and recovery work.

These are open infrastructure and security contracts.

### 2.6 Audit and history

Current Audit Trail implementation uses immutable `audit_records` and `audit_operations` persistence. Audit records preserve actor, action, entity, changes, reason, related record, and timestamp; database enforcement prevents UPDATE/DELETE of audit records.

This is a useful foundation for tracing document operations, but it is not equivalent to:

- storing old and new binary document versions;
- representing an original/duplicate relationship;
- preserving document status transitions as a document lifecycle;
- retrieving a document's complete version chain.

Audit must complement, not replace, document-version and document-relation models.

## 3. Status by historical requirement

| Requirement | Current assessment |
|---|---|
| Basic Document persistence | Partially implemented |
| Document template persistence | Partially implemented |
| Template version label | Implemented as a field only |
| Document type directory with stable codes/categories | Not found |
| Document lifecycle/statuses | Not found |
| Direct Document ↔ Instrument association | Not found |
| Instrument passport record | Not found |
| Original passport preservation | Not established by current model |
| Duplicate passport creation workflow | Not found |
| Original ↔ duplicate relation and reason | Not found |
| Document instance version history | Not found |
| Dedicated file metadata/storage model | Not found |
| Secure file upload/download/access control | Not found |
| Document links to Verification/Repair/Diagnostic | Not found |
| Template-based document generation workflow | Not found |
| Audit foundation for future document actions | Implemented as a general mechanism |
| Document API and frontend workflow | Not found |

## 4. Important boundaries for future design

### 4.1 Passport is a document attached to a persistent Instrument identity

An Instrument is a long-lived identity. A passport is one of the documents describing that Instrument and must not become the Instrument's identity itself.

Loss of a passport does not mean loss/deletion of the Instrument record. Issuing a duplicate must preserve the original passport record and the fact/reason that a duplicate was issued.

The duplicate is a new document issuance related to the original; it must not overwrite the original file or mutate old historical facts.

### 4.2 Distinguish document kinds, document instances, files, and versions

The historical proposal combines several concepts that should be kept distinct during design:

- document type: what kind of document this is (passport, certificate, protocol, repair act, etc.);
- document instance: a particular issued/received/registered document;
- binary file: the stored content or scan;
- document version/revision: a changed edition of the same logical document, where applicable;
- document relation: duplicate of, corrected by, or version of another document;
- business association: which Instrument, Order, Verification, Repair, Diagnostic, or Organization the document concerns.

Not every new file is necessarily a new document version. A duplicate passport, a corrected certificate, a new scan of the same paper, and a new Verification certificate may represent different business events.

### 4.3 Preserve provenance and legal meaning

For legal/regulated documents, retain provenance: who created or uploaded the document, when, from which template/version and source data, whether it was issued/registered/cancelled, and why a replacement or correction occurred.

Do not assume every document type needs the same status sequence. Drafting, generation, registration, issue, cancellation, and archival rules may differ by document type and process.

### 4.4 Do not make documents mandatory for all operations

A missing passport or optional attachment must not automatically block Instrument intake, Order creation, Verification, Repair, or Diagnostics unless a concrete regulatory/business rule requires it. The service-center workflow must remain operable while information is progressively accumulated.

### 4.5 Connect to Verification and methodology without conflating them

Verification documents (protocol, certificate, notice of unsuitability) should be associated with the specific Verification execution/result, not merely with the Instrument or Order in general.

Methodology documents are different: they describe normative method versions and applicability. They should be linked to the Method/MethodVersion and selected for a Verification according to Instrument Type, modification, and production period, as discussed in the current project work. A generated Verification document should preserve which method version and execution facts supported the decision.

## 5. Open questions

These require business examples or source documents before implementation:

1. Which passport formats are handled: paper scan, original electronic document, generated Sfera duplicate, or all of these?
2. What exact data and wording are required to issue a duplicate passport, and who is authorized to issue/sign it?
3. Does issuing a duplicate automatically mark the original as lost/invalid, or can an original later be recovered and retained with a historical status?
4. How should damaged, unreadable, corrected, and restored-from-archive documents differ?
5. Which document types have legal status transitions and which are simply attachments?
6. Is a correction a new version of the same document, a new related document, or a replacement issuance? This may differ by type.
7. Which source documents/templates are authoritative, and how are template revisions approved and made effective?
8. What is the actual binary storage requirement (local/object storage, access model, backup, retention, maximum file size, allowed formats)?
9. Which documents must be attached to Instrument, Order, OrderItem, Verification, Repair, Diagnostic, Customer, or Organization?
10. Which operations need a reason and immutable audit entry?

## 6. Recommended next analysis

Before changing code:

1. Review representative real Instrument passports, duplicate passports, Verification certificates/protocols, repair acts, and unsuitability notices.
2. Confirm the existing file storage/deployment/backup requirements rather than assuming a local filesystem path is sufficient.
3. Define the smallest domain model that distinguishes DocumentType, Document, File, DocumentRelation, and version/revision where the real document cases require them.
4. Define passport issuance and duplicate workflow as a concrete business scenario, including recovery of an allegedly lost original.
5. Trace Verification document creation from the final approved Verification and preserve its MethodVersion and source data.
6. Define authorization and immutable audit behavior for issue, correction, cancellation, archive, and duplicate operations.

No application code, database schema, API behavior, or frontend behavior was changed by this audit. Historical requirements remain relevant unless explicitly superseded by a later business decision.

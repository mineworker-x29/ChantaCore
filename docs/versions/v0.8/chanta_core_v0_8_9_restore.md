# ChantaCore v0.8.9 Restore

## Version

ChantaCore v0.8.9 — OCEL Compatibility & Report Quality Hardening

## Purpose

v0.8.9 is a hardening release before v0.9. It does not add a major runtime
capability. It focuses on OCEL compatibility, canonical consistency, export and
import round trips, report quality, inspector readability, and static hygiene.

## OCEL Compatibility Scope

ChantaCore still uses its own internal canonical OCEL model:

- `OCELEvent.event_activity`
- `OCELEvent.event_attrs`
- `OCELObject.object_attrs`
- `OCELRelation.relation_attrs`

The SQLite store includes:

- standard-oriented OCEL tables: `event`, `object`, `event_object`,
  `object_object`
- ChantaCore canonical payload tables: `chanta_event_payload`,
  `chanta_object_state`, relation extension tables
- operational extension tables such as `chanta_raw_event_mirror`

v0.8.9 does not claim full OCEL 2.0 JSON/XML conformance.

## ChantaCore Canonical JSON

`OCELExporter.export_chanta_json(...)` writes ChantaCore canonical JSON:

- `format = "chanta_ocel_json"`
- `version = "0.8.9"`
- `events` with `event_activity` and `event_attrs`
- `objects` with `object_attrs`
- `relations` with `relation_attrs`
- `export_attrs.full_ocel2_json = false`

`OCELImporter.import_chanta_json(...)` imports this format into an `OCELStore`.
IDs are handled idempotently through the existing store insert/upsert behavior.
Imported records are marked with `imported_from_chanta_json` provenance in event,
object, and relation attributes.

`export_json_stub(...)` remains a stub for future full OCEL 2.0 JSON export and
points callers to `export_chanta_json(...)`.

## SQLite Export

`OCELExporter.export_sqlite_copy(...)` copies an existing SQLite database to the
target path. It creates parent directories and fails clearly if the source DB is
missing. It does not destructively overwrite a ChantaCore runtime store through
import logic.

## Validator Hardening

`OCELValidator` includes:

- `validate_canonical_model()`
- `validate_export_readiness()`
- existing structure, duplicate relation, session trace, and minimum count checks

Readiness checks include counts, malformed attrs JSON, missing timestamps,
missing activities, missing object types, events without relations, and duplicate
relation status.

## Report Quality

`PIGReportService` report text is more operator-readable and includes concise
sections for:

- trace
- objects
- relations
- variant
- performance precursor
- process and queue conformance
- guidance and decision
- skill and tool usage
- editing and patch applications
- worker and scheduler state
- human/external PI artifacts

Structured detail remains in `report_attrs`; report generation is read-only.

## Inspector Quality

`PISubstrateInspector` now presents operator-facing sections for:

- OCEL health
- OCPX health
- PIG health
- skills
- tools
- worker queue
- scheduler
- editing/patch
- conformance
- warnings

Warnings are diagnostic and avoid blocking runtime behavior.

## Guardrails

v0.8.9 does not add:

- full OCEL 2.0 conformance claim
- pm4py or ocpa mandatory integration
- pandas, numpy, or networkx
- FastAPI or Streamlit
- async runtime
- MCP/plugin system
- shell or web/network tools
- self-modification
- automatic policy promotion

## Remaining Limitations

- no full OCEL 2.0 JSON/XML conformance
- no pm4py/ocpa mandatory integration
- no formal discovery/conformance/performance metrics
- no UI dashboard
- no external connector/plugin layer

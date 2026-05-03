# ChantaCore v0.6.4 Restore Notes

Version name: ChantaCore v0.6.4 - External OCEL & Human PI Assimilation

## Scope

This version adds two assimilation channels:

- External OCEL-like record ingestion under `src/chanta_core/ocel`
- Human or external PI assimilation under `src/chanta_core/pig`

## External OCEL Ingestion

External OCEL-like records are normalized through `ExternalOCELNormalizer` and appended through `ExternalOCELIngestionService`.

Imported ids are namespaced before persistence:

- `external:<source_id>:event:<original_event_id>`
- `external:<source_id>:object:<original_object_id>`

External source provenance is preserved in event, object, and relation attrs. Invalid rows are rejected per record and do not crash the whole ingestion batch when other records are valid.

## Human / External PI Assimilation

Human PI is stored as advisory `PIArtifact` under PIG. `PIArtifactStore` is an append-only JSONL store at `data/pig/pi_artifacts.jsonl` by default. `HumanPIAssimilator` records confidence, scope, evidence refs, object refs, and advisory metadata.

Human PI is not treated as ground truth, hard policy, or automatic execution rule in this version.

## PIGContext

`PIGContext` can include structured `pi_artifacts`. `PIGFeedbackService` can include concise Human / External PI summaries in `context_text`, using artifact type, title, and confidence. Raw long artifact content is not dumped into prompt context by default.

## Architecture Guardrails

The process intelligence layer remains PIG. No separate `process_intelligence`, `pi`, or `intelligence` package is introduced.

Full OCEL 2.0 import, full OCPA algorithms, full OPeRA metrics, automatic policy promotion, human review UI, and external tool-based ingestion are future work.

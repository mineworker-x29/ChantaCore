# ChantaCore v0.14.4 Restore Note - External OCEL Import Candidate

Date: 2026-05-08

Version: 0.14.4

This document is a human-readable restore note. It is not canonical runtime state. ChantaCore canonical runtime/process state remains OCEL-based.

## Summary

v0.14.4 adds an OCEL-native foundation for registering external OCEL or OCEL-like payloads as review-required import candidates.

The key boundary is strict:

External OCEL payloads are candidates only. They are not merged into the canonical ChantaCore OCEL store as accepted runtime facts.

## Added Models

v0.14.4 adds:

- `ExternalOCELSource`
- `ExternalOCELPayloadDescriptor`
- `ExternalOCELImportCandidate`
- `ExternalOCELValidationResult`
- `ExternalOCELPreviewSnapshot`
- `ExternalOCELImportRiskNote`

Location:

- `src/chanta_core/external/ocel_import.py`

## Added Service

Added:

- `ExternalOCELImportCandidateService`

The service supports:

- registering an external OCEL source;
- registering a provided dict payload as a descriptor;
- structurally validating the payload;
- creating a preview snapshot;
- recording risk notes;
- creating a review-required import candidate;
- running the full provided-dict-to-candidate flow through `register_as_candidate()`.

## Candidate Boundary

Every external OCEL import candidate is created with:

- `candidate_status="pending_review"`
- `review_status="pending_review"`
- `merge_status="not_merged"`
- `canonical_import_enabled=False`

`canonical_import_enabled` must remain false in v0.14.4.

## No Canonical Merge

v0.14.4 does not:

- merge external events into canonical OCEL event tables as accepted facts;
- merge external objects into canonical OCEL object tables as accepted facts;
- merge external relations into canonical OCEL relation tables as accepted facts;
- create a canonical external OCEL import store in JSONL;
- treat Markdown as canonical;
- use terminal scrollback as canonical;
- auto-approve import candidates.

Only ChantaCore's own metadata events/objects are recorded:

- source registration;
- payload descriptor registration;
- structural validation;
- preview snapshot creation;
- risk note recording;
- candidate creation;
- review-required marker.

## Validation

Validation is structural only.

It examines supplied dict content for:

- events;
- objects;
- relations;
- event activities;
- object types;
- relation types;
- timestamps.

It does not call an LLM judge.

It does not fetch schemas from network.

It does not accept the payload into canonical runtime history.

## Preview Snapshot

Preview snapshots are read-model summaries only.

They include:

- event count;
- object count;
- relation count;
- event activity counts;
- object type counts;
- relation type counts;
- timestamp range;
- sample event ids;
- sample object ids.

Preview snapshots do not create canonical OCEL facts for the external payload's internal events or objects.

## Risk Notes

Risk notes can record:

- untrusted source;
- large payload;
- unknown schema;
- missing timestamps;
- missing object relations;
- potential PII;
- potential secrets;
- canonical pollution risk;
- unknown/other risk.

`canonical_pollution_risk` is expected for external OCEL candidates because the future danger is confusing untrusted imported history with canonical runtime facts.

## OCEL Object Types

The following object types are used:

- `external_ocel_source`
- `external_ocel_payload_descriptor`
- `external_ocel_import_candidate`
- `external_ocel_validation_result`
- `external_ocel_preview_snapshot`
- `external_ocel_import_risk_note`

Candidate object attrs include:

- `canonical_import_enabled=False`
- `merge_status="not_merged"`

## OCEL Event Activities

The following activities are recorded:

- `external_ocel_source_registered`
- `external_ocel_payload_registered`
- `external_ocel_validation_started`
- `external_ocel_validation_recorded`
- `external_ocel_preview_created`
- `external_ocel_risk_note_recorded`
- `external_ocel_candidate_created`
- `external_ocel_candidate_review_required`

The implementation keeps relation intent where current OCEL APIs allow:

- descriptor from source;
- candidate derived from descriptor;
- validation validates descriptor/candidate;
- preview previews descriptor/candidate;
- risk note describes descriptor/candidate.

## Context History

Added history adapter helpers:

- `external_ocel_candidates_to_history_entries`
- `external_ocel_validation_results_to_history_entries`
- `external_ocel_preview_snapshots_to_history_entries`
- `external_ocel_risk_notes_to_history_entries`

History entries use:

- `source="external_ocel_import"`
- `role="context"`

Invalid validations and high/critical risks receive higher priority.

## PIG/OCPX Lightweight Report Support

PIG report support now includes external OCEL counts:

- `external_ocel_source_count`
- `external_ocel_payload_descriptor_count`
- `external_ocel_import_candidate_count`
- `external_ocel_validation_result_count`
- `external_ocel_preview_snapshot_count`
- `external_ocel_risk_note_count`
- `external_ocel_valid_count`
- `external_ocel_invalid_count`
- `external_ocel_needs_review_count`
- `external_ocel_candidate_pending_review_count`
- `external_ocel_candidate_canonical_import_enabled_count`
- `external_ocel_candidate_not_merged_count`
- `external_ocel_total_preview_event_count`
- `external_ocel_total_preview_object_count`
- `external_ocel_total_preview_relation_count`
- `external_ocel_by_schema_status`
- `external_ocel_by_risk_level`

The expected v0.14.4 value for `external_ocel_candidate_canonical_import_enabled_count` is `0`.

## Default Agent Capability Profile

If the v0.14.3a Default Agent Capability Contract is present, v0.14.4 classifies external OCEL support as non-active:

- external OCEL payload descriptors are `metadata_only`;
- external OCEL import candidates are `metadata_only` and `requires_review`;
- external OCEL preview snapshots are `metadata_only`;
- canonical external OCEL merge is `not_implemented`;
- active external OCEL ingestion is `not_implemented`.

The Default Agent must not claim that it can import or merge external OCEL automatically.

## Explicit Non-Goals

v0.14.4 does not add:

- Default Agent ambient file import;
- arbitrary workspace file read;
- network calls;
- URL fetching;
- MCP connection;
- plugin loading;
- shell execution;
- runtime tool activation;
- permission auto-grants;
- review auto-approval;
- async worker;
- UI.

## Tests

Added tests cover:

- model `to_dict()` methods;
- candidate defaults;
- structural validation;
- preview counts;
- no canonical merge;
- OCEL object/event shape;
- history adapter conversion;
- PIG report counts;
- Default Agent capability classification;
- boundary grep for forbidden behavior.

## Future Work

Future versions may add a controlled external OCEL assimilation pipeline, but only after explicit review, permission, safety, and conformance layers exist.

Any future import pipeline must preserve provenance and distinguish external historical facts from ChantaCore's own canonical runtime facts.

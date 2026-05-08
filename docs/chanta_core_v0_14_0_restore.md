# ChantaCore v0.14.0 Restore Notes

## Version

ChantaCore v0.14.0 adds External Capability Descriptor Import.

This version imports external capability descriptors as untrusted metadata, normalizes them into ChantaCore internal capability categories, records risk notes, and creates disabled assimilation candidates. It does not activate, load, or run imported capabilities.

## Architectural Boundary

Canonical persistence remains OCEL-based.

External capability import state is represented as OCEL event, object, and relation records. JSONL is not introduced as canonical persistence for this feature. Markdown remains a human-readable restore view only.

## New Package

The implementation lives in `src/chanta_core/external/`.

Files:

- `__init__.py`
- `ids.py`
- `errors.py`
- `models.py`
- `service.py`
- `history_adapter.py`

## OCEL Objects

v0.14.0 introduces these OCEL object types:

- `external_capability_source`
- `external_capability_descriptor`
- `external_capability_import_batch`
- `external_capability_normalization_result`
- `external_assimilation_candidate`
- `external_capability_risk_note`

`ExternalCapabilitySource` records source metadata such as source name, source type, source ref, trust level, status, and timestamps.

`ExternalCapabilityDescriptor` records the imported descriptor as untrusted input. The raw descriptor is preserved. Declared entrypoints are metadata only.

`ExternalCapabilityImportBatch` records descriptor import batches and failed descriptor references.

`ExternalCapabilityNormalizationResult` records deterministic normalization output, normalized permissions, normalized risk categories, and validation messages.

`ExternalAssimilationCandidate` records a design/review candidate derived from a descriptor. In v0.14.0, candidates are disabled and `execution_enabled` remains `False`.

`ExternalCapabilityRiskNote` records risk categories, inferred or supplied risk level, review requirement, and related descriptor or candidate refs.

## OCEL Events

The service records these event activities:

- `external_capability_source_registered`
- `external_capability_import_started`
- `external_capability_descriptor_imported`
- `external_capability_normalized`
- `external_capability_normalization_failed`
- `external_assimilation_candidate_created`
- `external_capability_risk_note_recorded`
- `external_capability_import_completed`
- `external_capability_import_failed`

The descriptor-invalid activity is reserved for invalid descriptor flows; v0.14.0 primarily raises validation errors for non-dict raw descriptors.

## Service Behavior

`ExternalCapabilityImportService` supports:

- source registration
- raw descriptor import
- descriptor batch import
- deterministic descriptor normalization
- disabled assimilation candidate creation
- risk note recording
- import as disabled candidate

External descriptors are always treated as untrusted input. Imported capabilities are not added to active runtime registries.

## Explicit Non-Goals

v0.14.0 does not do the following:

- no external tool execution
- no external skill execution
- no plugin dynamic loading
- no MCP connection
- no network calls
- no URL fetch
- no git clone
- no external code import
- no `ToolDispatcher` mutation
- no `SkillExecutor` mutation
- no `AgentRuntime` active capability integration
- no permission auto-grant
- no candidate auto-enable
- no active runtime tool creation
- no LLM classifier
- no async worker
- no UI
- no canonical JSONL external capability store

## Context History

`src/chanta_core/external/history_adapter.py` provides helpers that convert supplied descriptors, candidates, and risk notes into `ContextHistoryEntry` values.

The adapter does not retrieve from OCEL automatically yet. It only adapts supplied objects.

## PIG/OCPX Report Support

PIG report attrs include `external_capability_summary`.

The summary includes:

- external capability source count
- external capability descriptor count
- external capability import batch count
- external capability normalization result count
- external assimilation candidate count
- external capability risk note count
- disabled candidate count
- pending review candidate count
- execution-enabled candidate count
- capability distribution by type
- risk note distribution by risk level
- review required count

For v0.14.0, `external_candidate_execution_enabled_count` should normally be `0`.

## Restore Procedure

1. Confirm version metadata:
   - `pyproject.toml` version is `0.14.0`.
   - `src/chanta_core/__init__.py` `__version__` is `0.14.0`.
2. Confirm `src/chanta_core/external/` exists with the package files listed above.
3. Run the external capability tests:
   - `tests/test_external_capability_models.py`
   - `tests/test_external_capability_service.py`
   - `tests/test_external_capability_normalization.py`
   - `tests/test_external_capability_history_adapter.py`
   - `tests/test_external_capability_ocel_shape.py`
   - `tests/test_external_capability_boundaries.py`
4. Run `scripts/test_external_capability_import.py`.
5. Confirm all created candidates have `activation_status="disabled"` and `execution_enabled=False`.
6. Confirm no runtime registry is mutated and no external descriptor entrypoint is loaded.

## Future Work

- external capability registry view
- adapter review queue
- MCP/plugin descriptor skeleton
- external OCEL import candidate
- manual review flow for promoting candidates into design artifacts

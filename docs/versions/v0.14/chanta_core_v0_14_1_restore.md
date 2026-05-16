# ChantaCore v0.14.1 Restore Notes

## Version

ChantaCore v0.14.1 adds External Capability Registry View.

This version creates human-readable materialized Markdown views over OCEL-backed external capability import records. It does not activate, approve, reject, load, or run external capabilities.

## Architectural Boundary

Canonical persistence remains OCEL-based.

The external capability registry state is represented by OCEL event, object, and relation records. Markdown views are generated projections only. Edits to generated Markdown do not update OCEL and do not activate or deactivate capabilities.

## New Model

`ExternalCapabilityRegistrySnapshot` is implemented in `src/chanta_core/external/views.py`.

It is recorded as OCEL object type:

- `external_capability_registry_snapshot`

The snapshot records source IDs, descriptor IDs, normalization IDs, candidate IDs, risk note IDs, disabled candidate count, execution-enabled candidate count, pending review count, high risk count, and critical risk count.

`execution_enabled_candidate_count` is reported only. The view service does not auto-disable candidates and does not mutate candidate objects.

## Generated Views

The default view paths are:

- `.chanta/EXTERNAL_CAPABILITIES.md`
- `.chanta/EXTERNAL_REVIEW.md`
- `.chanta/EXTERNAL_RISKS.md`

`EXTERNAL_CAPABILITIES.md` is a generated materialized view of sources, descriptors, normalizations, candidates, and summary counts.

`EXTERNAL_REVIEW.md` is not a review queue. It does not approve, reject, activate, or run external capabilities. Formal review workflow belongs to a later version.

`EXTERNAL_RISKS.md` is not an enforcement policy. It does not block or allow external capabilities. Risk notes are advisory records only.

All generated views state:

- Canonical source: OCEL.
- Markdown is not canonical.
- Edits do not enable or disable capabilities.
- No external capability is executable from the view.

## Service

`ExternalCapabilityRegistryViewService` supports:

- registry snapshot creation
- registry view rendering
- review view rendering
- risk view rendering
- default external view rendering
- generated view writing
- default external view refresh

The service records OCEL events for snapshot creation, view rendering, and view writing.

## OCEL Events

v0.14.1 records:

- `external_capability_registry_snapshot_created`
- `external_capability_registry_view_rendered`
- `external_capability_registry_view_written`
- `external_capability_review_view_rendered`
- `external_capability_review_view_written`
- `external_capability_risk_view_rendered`
- `external_capability_risk_view_written`

It may also record:

- `external_capability_view_refresh_started`
- `external_capability_view_refresh_completed`
- `external_capability_execution_enabled_candidate_detected`

## Explicit Non-Goals

v0.14.1 does not do the following:

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
- no review decision lifecycle
- no Markdown-to-OCEL import
- no canonical JSONL external registry store

## Context History

`external_capability_registry_snapshots_to_history_entries` converts supplied registry snapshots to `ContextHistoryEntry` values with source `external_capability_view`.

The adapter does not retrieve from OCEL automatically.

## PIG/OCPX Report Support

PIG external capability summary includes:

- external capability registry snapshot count
- registry view written count
- review view written count
- risk view written count
- external view disabled candidate count
- external view execution-enabled candidate count
- external view pending review count
- external view high risk count
- external view critical risk count

For v0.14.1, `external_view_execution_enabled_candidate_count` should normally be `0`.

## Restore Procedure

1. Confirm version metadata:
   - `pyproject.toml` version is `0.14.1`.
   - `src/chanta_core/__init__.py` `__version__` is `0.14.1`.
2. Confirm `src/chanta_core/external/views.py` exists.
3. Run external capability view tests:
   - `tests/test_external_capability_view_models.py`
   - `tests/test_external_capability_view_renderers.py`
   - `tests/test_external_capability_view_service.py`
   - `tests/test_external_capability_view_history_adapter.py`
   - `tests/test_external_capability_view_ocel_shape.py`
   - `tests/test_external_capability_view_boundaries.py`
4. Run `scripts/test_external_capability_views.py`.
5. Confirm generated `.chanta/*.md` files are treated as non-canonical materialized views.
6. Confirm candidates remain unchanged after rendering and writing views.

## Future Work

- v0.14.2 External Adapter Review Queue
- v0.14.3 MCP / Plugin Descriptor Skeleton
- v0.14.4 External OCEL Import Candidate

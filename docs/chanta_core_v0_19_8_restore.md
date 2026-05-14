# ChantaCore v0.19.8 Restore

## Version

- Version: `0.19.8`
- Name: Observation-to-Digestion Adapter Candidate Builder
- Status: restore reference

## Purpose

v0.19.8 connects observation to digestion. Observed behavior becomes an observed capability candidate, the capability candidate maps to a ChantaCore target skill candidate, and the builder creates review-only adapter candidates from that mapping.

## Public Boundary

The v0.19.8 surface is generic. Public code, tests, CLI output, reports, and restore material must not expose private names, private local roots, private letters, relationship notes, or user-specific artifacts.

## Added Substrate

- `ObservationToDigestionAdapterPolicy`
- `ObservedCapabilityCandidate`
- `ChantaCoreTargetSkillCandidate`
- `AdapterInputMappingSpec`
- `AdapterOutputMappingSpec`
- `AdapterUnsupportedFeature`
- `ObservationDigestionAdapterCandidate`
- `ObservationDigestionAdapterReviewRequest`
- `ObservationDigestionAdapterFinding`
- `ObservationDigestionAdapterBuildResult`
- `ObservationToDigestionAdapterBuilderService`

## Behavior

The builder uses deterministic mapping only. It can read existing `AgentBehaviorInferenceV2`, `ExternalSkillBehaviorFingerprint`, and `ObservedAgentRun` objects, extract observed capability candidates, map them to target skill candidates, create input/output mapping specs, record unsupported features, create review requests, and emit OCEL objects/events/relations.

Adapter candidates are review-only and non-executable. The default policy disables automatic activation, canonical import, and execution enablement. Candidate defaults keep `review_status=pending_review`, `requires_review=True`, `canonical_import_enabled=False`, and `execution_enabled=False`.

Unsupported features are explicitly recorded. Shell execution, workspace writes, network access, MCP connection, plugin loading, and external harness execution remain future-track capabilities.

## CLI

`chanta-cli digest adapter-build` adds read-only candidate build commands:

- `from-inference --inference-json-file <path>`
- `from-fingerprint --fingerprint-json-file <path>`
- `from-observed-run --observed-run-json-file <path>`
- `show <adapter_candidate_id>`
- `unsupported <adapter_candidate_id>`

CLI summaries are redacted and report observed capabilities, target skill candidates, adapter candidates, unsupported features, review status, canonical import state, and execution state.

## OCEL and Reports

The builder records OCEL objects/events for policies, capability candidates, target candidates, input/output mappings, unsupported features, adapter candidates, review requests, findings, and build results. PIG/OCPX report support adds counts by object type plus candidate risk class, target skill id, mapping type, unsupported feature type, and observed capability category.

## Non-Goals

- No external execution.
- No adapter execution.
- No canonical import.
- No JSONL canonical adapter store.
- No write, shell, network, MCP, or plugin safety implementation.
- No LLM calls.
- No memory, persona, or overlay mutation.

## Restore Checks

- Confirm version is `0.19.8` in `pyproject.toml` and `src/chanta_core/__init__.py`.
- Import `ObservationToDigestionAdapterBuilderService`.
- Build from public dummy `AgentBehaviorInferenceV2`.
- Verify read/search/summary mapping.
- Verify unsupported features are explicit.
- Verify adapter candidates stay review-only and non-executable.
- Verify OCEL object/event records are emitted.
- Verify PIG/OCPX summary counts are present.

## Future Work

- v0.19.9 consolidation.
- Actual external adapter implementation after review substrate hardening.
- Future write, shell, network, MCP, plugin, and external harness safety tracks.

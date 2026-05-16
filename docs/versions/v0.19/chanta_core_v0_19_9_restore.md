# ChantaCore v0.19.9 Restore

## Version Identity

- Version: `0.19.9`
- Name: Observation/Digestion Ecosystem Consolidation
- Primary module: `src/chanta_core/observation_digest/ecosystem.py`
- Scope: read-only consolidation of the v0.19.x Observation/Digestion ecosystem
- Boundary: summarize and verify; do not add execution capability

## Restore Purpose

v0.19.9 consolidates the Observation/Digestion ecosystem. It summarizes the components introduced from v0.19.0 through v0.19.8, records their readiness, maps ecosystem capabilities, confirms safety boundaries, registers gaps, and emits a release manifest and consolidation report.

This version is not a feature-execution release. It is a state-of-ecosystem release.

## Covered Version Range

The release manifest must include:

- `v0.19.0`: Observation/Digestion internal skill seed pack
- `v0.19.1`: Skill Registry View
- `v0.19.2`: Proposal Integration
- `v0.19.3`: Gated Invocation
- `v0.19.4`: Conformance and Smoke
- `v0.19.5`: Expanded Static Digestion
- `v0.19.6`: Agent Observation Spine and Movement Ontology
- `v0.19.7`: Cross-Harness Trace Adapter Contracts
- `v0.19.8`: Observation-to-Digestion Adapter Candidate Builder
- `v0.19.9`: Ecosystem Consolidation

## Public Boundary

The v0.19.9 surface is generic. Public code, tests, CLI output, reports, restore material, fixtures, and examples must not expose private names, private local roots, private letters, relationship notes, or user-specific artifacts.

The consolidation service may report privacy boundary status but must not load or expose private content.

## Files

Core:

- `src/chanta_core/observation_digest/ecosystem.py`
- `src/chanta_core/observation_digest/__init__.py`
- `src/chanta_core/skills/ids.py`

Integration:

- `src/chanta_core/cli/main.py`
- `src/chanta_core/pig/reports.py`
- `tests/test_imports.py`

Docs:

- `docs/versions/v0.19/chanta_core_v0_19_9_restore.md`

Tests:

- `tests/test_observation_digestion_ecosystem_models.py`
- `tests/test_observation_digestion_ecosystem_service.py`
- `tests/test_observation_digestion_ecosystem_cli.py`
- `tests/test_observation_digestion_ecosystem_ocel_shape.py`
- `tests/test_observation_digestion_ecosystem_history_adapter.py`
- `tests/test_observation_digestion_ecosystem_boundaries.py`
- `tests/test_observation_digestion_ecosystem_safety.py`
- `tests/test_observation_digestion_ecosystem_gaps.py`
- `tests/test_observation_digestion_ecosystem_pig.py`

## Version Bump

Required version updates:

- `pyproject.toml`: `version = "0.19.9"`
- `src/chanta_core/__init__.py`: `__version__ = "0.19.9"`

## ID Constructors

Add these constructors to `src/chanta_core/skills/ids.py`:

- `new_observation_digestion_ecosystem_snapshot_id()`
- `new_observation_digestion_ecosystem_component_id()`
- `new_observation_digestion_capability_map_id()`
- `new_observation_digestion_safety_boundary_report_id()`
- `new_observation_digestion_gap_register_id()`
- `new_observation_digestion_release_manifest_id()`
- `new_observation_digestion_consolidation_finding_id()`
- `new_observation_digestion_consolidation_report_id()`

Required prefixes:

- `observation_digestion_ecosystem_snapshot:`
- `observation_digestion_ecosystem_component:`
- `observation_digestion_capability_map:`
- `observation_digestion_safety_boundary_report:`
- `observation_digestion_gap_register:`
- `observation_digestion_release_manifest:`
- `observation_digestion_consolidation_finding:`
- `observation_digestion_consolidation_report:`

## Readiness Levels

Use exactly these readiness levels:

- `ready`
- `partial`
- `contract_only`
- `stub_only`
- `blocked`
- `future_track`
- `unknown`

Unavailable components must degrade gracefully. They should become `partial` and produce a consolidation finding, not crash the report.

## Component Kinds

Use these component kinds:

- `internal_skill`
- `registry`
- `proposal_surface`
- `invocation_surface`
- `conformance`
- `static_digestion`
- `observation_spine`
- `cross_harness_adapter`
- `adapter_candidate_builder`
- `safety_boundary`
- `privacy_boundary`
- `future_track`

## Capability Families

Use these capability families:

- `observation`
- `digestion`
- `adapter_mapping`
- `static_analysis`
- `behavior_inference`
- `fleet_observation`
- `future_write`
- `future_shell`
- `future_network`
- `future_mcp`
- `future_plugin`
- `unknown`

## Models

Implement dataclasses with `to_dict()` and stable list/dict copying.

### `ObservationDigestionEcosystemSnapshot`

Fields:

- `snapshot_id`
- `version`
- `observation_skill_count`
- `digestion_skill_count`
- `registry_entry_count`
- `proposal_surface_count`
- `invocation_binding_count`
- `conformance_report_count`
- `static_digestion_report_count`
- `observation_spine_object_count`
- `adapter_contract_count`
- `adapter_candidate_count`
- `unsupported_feature_count`
- `pending_review_count`
- `executable_external_candidate_count`
- `created_at`
- `snapshot_attrs`

Default expected state:

- `version="0.19.9"`
- `observation_skill_count > 0`
- `digestion_skill_count > 0`
- `executable_external_candidate_count=0`

If a fixture intentionally simulates an executable external candidate, increment `executable_external_candidate_count` and create a high severity finding.

### `ObservationDigestionEcosystemComponent`

Fields:

- `component_id`
- `snapshot_id`
- `component_name`
- `component_kind`
- `status`
- `readiness_level`
- `object_refs`
- `dependency_refs`
- `finding_refs`
- `created_at`
- `component_attrs`

Core component inventory should include at least:

- observation internal skill seed pack
- digestion internal skill seed pack
- skill registry view
- proposal surface
- gated invocation surface
- conformance and smoke surface
- static digestion
- agent observation spine
- cross-harness adapter contracts
- observation-to-digestion adapter candidate builder

### `ObservationDigestionCapabilityMap`

Fields:

- `capability_map_id`
- `snapshot_id`
- `capability_name`
- `capability_family`
- `source_component_ref`
- `related_skill_ids`
- `related_candidate_ids`
- `supported_now`
- `requires_review`
- `execution_enabled`
- `future_track_hint`
- `created_at`
- `map_attrs`

Required families in default map:

- `observation`
- `digestion`
- `adapter_mapping`
- `future_write`
- `future_shell`
- `future_network`
- `future_mcp`
- `future_plugin`

All capability map entries must have `execution_enabled=False`.

### `ObservationDigestionSafetyBoundaryReport`

Fields:

- `safety_report_id`
- `snapshot_id`
- `external_harness_execution_allowed`
- `external_script_execution_allowed`
- `shell_allowed`
- `network_allowed`
- `write_allowed`
- `mcp_allowed`
- `plugin_allowed`
- `memory_mutation_allowed`
- `persona_mutation_allowed`
- `overlay_mutation_allowed`
- `raw_transcript_export_allowed`
- `full_body_export_allowed`
- `finding_ids`
- `status`
- `created_at`
- `report_attrs`

Required default booleans:

- `external_harness_execution_allowed=False`
- `external_script_execution_allowed=False`
- `shell_allowed=False`
- `network_allowed=False`
- `write_allowed=False`
- `mcp_allowed=False`
- `plugin_allowed=False`
- `memory_mutation_allowed=False`
- `persona_mutation_allowed=False`
- `overlay_mutation_allowed=False`
- `raw_transcript_export_allowed=False`
- `full_body_export_allowed=False`

### `ObservationDigestionGapRegister`

Fields:

- `gap_register_id`
- `snapshot_id`
- `gap_type`
- `gap_name`
- `description`
- `severity`
- `affected_components`
- `future_track_hint`
- `blocking`
- `created_at`
- `gap_attrs`

Required future gaps:

- full external adapters
- sidecar observer
- event bus collector
- enterprise collector
- basic foundation skill pack
- write safety track
- shell safety track
- network safety track
- MCP safety track
- plugin safety track

### `ObservationDigestionReleaseManifest`

Fields:

- `release_manifest_id`
- `version`
- `snapshot_id`
- `included_versions`
- `included_components`
- `accepted_boundaries`
- `known_limitations`
- `future_tracks`
- `status`
- `created_at`
- `manifest_attrs`

`included_versions` must be exactly the v0.19.0 through v0.19.9 series.

### `ObservationDigestionConsolidationFinding`

Fields:

- `finding_id`
- `snapshot_id`
- `subject_ref`
- `finding_type`
- `status`
- `severity`
- `message`
- `evidence_ref`
- `created_at`
- `finding_attrs`

Required finding cases:

- `component_unavailable`
- `executable_external_candidate_detected`

### `ObservationDigestionConsolidationReport`

Fields:

- `report_id`
- `snapshot_id`
- `release_manifest_id`
- `status`
- `total_component_count`
- `ready_component_count`
- `partial_component_count`
- `contract_only_component_count`
- `blocked_component_count`
- `finding_ids`
- `gap_register_ids`
- `summary`
- `created_at`
- `report_attrs`

Default report status:

- `completed` when no findings exist
- `warning` when findings exist

## Service Contract

Implement `ObservationDigestionEcosystemConsolidationService`.

Required methods:

- `create_ecosystem_snapshot(...)`
- `collect_skill_components(...)`
- `collect_registry_components(...)`
- `collect_proposal_components(...)`
- `collect_invocation_components(...)`
- `collect_conformance_components(...)`
- `collect_static_digestion_components(...)`
- `collect_observation_spine_components(...)`
- `collect_adapter_contract_components(...)`
- `collect_adapter_candidate_components(...)`
- `build_capability_map(...)`
- `build_safety_boundary_report(...)`
- `build_gap_register(...)`
- `build_release_manifest(...)`
- `record_finding(...)`
- `record_consolidation_report(...)`
- `render_ecosystem_summary(...)`
- `render_capability_map_cli(...)`
- `render_gap_register_cli(...)`
- `render_release_manifest_cli(...)`

The service may also expose a convenience `consolidate()` method that executes the read-only sequence:

1. clear last in-memory build state
2. create snapshot
3. collect components
4. build capability map
5. build safety report
6. build gap register
7. build release manifest
8. record consolidation report

## CLI

Add command group:

`chanta-cli observe-digest ecosystem`

Subcommands:

- `snapshot`
- `components`
- `capabilities`
- `safety`
- `gaps`
- `manifest`
- `report`

Options:

- `--json`
- `--limit`

Required output content:

- skill counts
- adapter counts
- candidate counts
- executable external candidate count
- safety boundary booleans
- future gaps

CLI output must be redacted and read-only. It must not execute skills or adapters.

## OCEL Shape

Object types:

- `observation_digestion_ecosystem_snapshot`
- `observation_digestion_ecosystem_component`
- `observation_digestion_capability_map`
- `observation_digestion_safety_boundary_report`
- `observation_digestion_gap_register`
- `observation_digestion_release_manifest`
- `observation_digestion_consolidation_finding`
- `observation_digestion_consolidation_report`

Event activities:

- `observation_digestion_ecosystem_snapshot_created`
- `observation_digestion_ecosystem_component_recorded`
- `observation_digestion_capability_map_created`
- `observation_digestion_safety_boundary_report_created`
- `observation_digestion_gap_registered`
- `observation_digestion_release_manifest_created`
- `observation_digestion_consolidation_finding_recorded`
- `observation_digestion_consolidation_report_recorded`

Expected relation qualifiers:

- `ecosystem_component_belongs_to_snapshot`
- `capability_map_belongs_to_snapshot`
- `safety_report_summarizes_snapshot`
- `gap_register_belongs_to_snapshot`
- `release_manifest_summarizes_snapshot`
- `consolidation_report_summarizes_snapshot`
- `consolidation_report_includes_gap`
- `consolidation_report_includes_finding`

Best-effort relation coverage is acceptable. Object and event emission is required.

## Context History Adapter

Add history conversion functions with source:

`observation_digestion_ecosystem_consolidation`

Required functions:

- `ecosystem_snapshots_to_history_entries`
- `ecosystem_components_to_history_entries`
- `capability_maps_to_history_entries`
- `safety_boundary_reports_to_history_entries`
- `gap_registers_to_history_entries`
- `release_manifests_to_history_entries`
- `consolidation_findings_to_history_entries`
- `consolidation_reports_to_history_entries`

Priority rules:

- unsafe boundary open -> high
- executable external candidate -> high
- blocked component -> high
- future-track gap -> medium
- report warning -> medium
- snapshot -> low/medium

## PIG/OCPX Report Support

Add a lightweight summary to `PIGReportService`.

Required count keys:

- `observation_digestion_ecosystem_snapshot_count`
- `observation_digestion_ecosystem_component_count`
- `observation_digestion_capability_map_count`
- `observation_digestion_safety_boundary_report_count`
- `observation_digestion_gap_register_count`
- `observation_digestion_release_manifest_count`
- `observation_digestion_consolidation_finding_count`
- `observation_digestion_consolidation_report_count`
- `observation_digestion_ready_component_count`
- `observation_digestion_partial_component_count`
- `observation_digestion_contract_only_component_count`
- `observation_digestion_blocked_component_count`
- `observation_digestion_future_track_gap_count`
- `observation_digestion_executable_external_candidate_count`

Required grouping keys:

- `observation_digestion_by_component_kind`
- `observation_digestion_by_readiness_level`
- `observation_digestion_by_capability_family`
- `observation_digestion_gap_by_type`
- `observation_digestion_finding_by_type`

Report text should include a readable section named `Observation/Digestion Ecosystem Consolidation`.

## Restore Implementation Sequence

1. Add ID constructors.
2. Add `ecosystem.py` dataclasses and service.
3. Export the models, service, and history adapter functions from `chanta_core.observation_digest`.
4. Add CLI parser entries under `observe-digest ecosystem`.
5. Add CLI handler for snapshot/components/capabilities/safety/gaps/manifest/report.
6. Add PIG/OCPX ecosystem summary.
7. Update import smoke test.
8. Add v0.19.9 ecosystem tests.
9. Add restore doc.
10. Bump version to `0.19.9`.
11. Run install and tests.
12. Run forbidden/private scan on v0.19.9 public files.

## Acceptance Commands

Install:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

Targeted tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_observation_digestion_ecosystem_models.py tests\test_observation_digestion_ecosystem_service.py tests\test_observation_digestion_ecosystem_cli.py tests\test_observation_digestion_ecosystem_ocel_shape.py tests\test_observation_digestion_ecosystem_history_adapter.py tests\test_observation_digestion_ecosystem_boundaries.py tests\test_observation_digestion_ecosystem_safety.py tests\test_observation_digestion_ecosystem_gaps.py tests\test_observation_digestion_ecosystem_pig.py
```

Full suite:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Expected v0.19.9 observed result at creation time:

- targeted ecosystem tests: passed
- full suite: passed
- package version after install: `0.19.9`

## Boundary Scan

Scan v0.19.9 public files for:

- explicit skill invocation
- execution gate invocation
- external execution
- script or harness execution
- sidecar or event bus startup
- shell/network/MCP/plugin usage
- LLM completion calls
- memory/persona/overlay mutation
- true default for canonical import enablement
- true default for execution enablement
- private names and private local roots

Findings should be zero for v0.19.9 new public files.

## Non-Goals

- No new executable skills.
- No skill execution.
- No external harness execution.
- No external script execution.
- No sidecar observer enablement.
- No event bus collector enablement.
- No shell, network, workspace write, MCP, or plugin enablement.
- No canonical import of external candidates as executable skills.
- No memory, persona, or overlay mutation.
- No LLM calls.
- No JSONL canonical consolidation store.

## Known Limitations

- Full external adapters are not implemented.
- Sidecar observer is not implemented.
- Event bus collector is not implemented.
- Enterprise collector is not implemented.
- Basic/foundation skill pack is not implemented.
- Write/shell/network/MCP/plugin safety tracks remain future work.
- The ecosystem report is a read-only consolidation snapshot, not a runtime actuator.

## Restore Confidence

Restore is possible from this document plus the test names above if the surrounding v0.19.x codebase exists. If only this document exists and no codebase context remains, this document is sufficient to reconstruct the public model, service, CLI, OCEL, history, and report surfaces, while exact internal count constants may require re-derivation from tests.

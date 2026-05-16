# ChantaCore v0.19.8 Restore

## Version Identity

- Version: `0.19.8`
- Name: Observation-to-Digestion Adapter Candidate Builder
- Primary module: `src/chanta_core/digestion/adapter_builder.py`
- Scope: bridge observed behavior into reviewable adapter candidates
- Boundary: candidate creation only; no adapter execution, no external execution, no canonical import

## Restore Purpose

v0.19.8 connects observation to digestion.

The intended flow is:

1. Existing observed behavior is read from an observation object.
2. Observed behavior becomes an `ObservedCapabilityCandidate`.
3. The capability candidate maps to a `ChantaCoreTargetSkillCandidate`.
4. Input and output mapping specs are generated.
5. Unsupported features are explicitly recorded.
6. A review-only `ObservationDigestionAdapterCandidate` is created.
7. A review request and build result are recorded.
8. OCEL objects/events/relations are emitted.

The implementation must be deterministic. It must not call an LLM, execute a skill, run a harness, run a script, call network, connect MCP, load plugins, or mutate memory/persona/overlay data.

## Public Boundary

The v0.19.8 surface is generic. Public code, tests, CLI output, reports, and restore material must not expose private names, private local roots, private letters, relationship notes, or user-specific artifacts.

Restore validation should scan public v0.19.8 files for private names, private roots, private-letter content, and user-specific fixtures.

## Files

Core:

- `src/chanta_core/digestion/adapter_builder.py`
- `src/chanta_core/digestion/__init__.py`
- `src/chanta_core/skills/ids.py`

Integration:

- `src/chanta_core/cli/main.py`
- `src/chanta_core/pig/reports.py`
- `tests/test_imports.py`

Docs:

- `docs/versions/v0.19/chanta_core_v0_19_8_restore.md`

Tests:

- `tests/test_observation_to_digestion_adapter_models.py`
- `tests/test_observation_to_digestion_adapter_service.py`
- `tests/test_observation_to_digestion_adapter_mapping.py`
- `tests/test_observation_to_digestion_adapter_cli.py`
- `tests/test_observation_to_digestion_adapter_ocel_shape.py`
- `tests/test_observation_to_digestion_adapter_history_adapter.py`
- `tests/test_observation_to_digestion_adapter_boundaries.py`
- `tests/test_observation_to_digestion_adapter_unsupported.py`
- `tests/test_observation_to_digestion_adapter_pig.py`

## Version Bump

Required version updates:

- `pyproject.toml`: `version = "0.19.8"`
- `src/chanta_core/__init__.py`: `__version__ = "0.19.8"`

If this restore is being applied after a later version, do not downgrade unless intentionally reconstructing the v0.19.8 state.

## ID Constructors

Add these constructors to `src/chanta_core/skills/ids.py`:

- `new_observation_to_digestion_adapter_policy_id()`
- `new_observed_capability_candidate_id()`
- `new_chantacore_target_skill_candidate_id()`
- `new_adapter_input_mapping_spec_id()`
- `new_adapter_output_mapping_spec_id()`
- `new_adapter_unsupported_feature_id()`
- `new_observation_digestion_adapter_candidate_id()`
- `new_observation_digestion_adapter_review_request_id()`
- `new_observation_digestion_adapter_finding_id()`
- `new_observation_digestion_adapter_build_result_id()`

Required prefixes:

- `observation_to_digestion_adapter_policy:`
- `observed_capability_candidate:`
- `chantacore_target_skill_candidate:`
- `adapter_input_mapping_spec:`
- `adapter_output_mapping_spec:`
- `adapter_unsupported_feature:`
- `observation_digestion_adapter_candidate:`
- `observation_digestion_adapter_review_request:`
- `observation_digestion_adapter_finding:`
- `observation_digestion_adapter_build_result:`

## Models

Implement dataclasses with `to_dict()` and stable list/dict copying.

### `ObservationToDigestionAdapterPolicy`

Fields:

- `policy_id`
- `policy_name`
- `allowed_source_kinds`
- `allowed_target_skill_layers`
- `denied_target_capabilities`
- `allow_auto_adapter_activation`
- `allow_canonical_skill_import`
- `allow_execution_enablement`
- `require_review`
- `require_evidence_refs`
- `require_confidence`
- `require_withdrawal_conditions`
- `min_mapping_confidence_for_candidate`
- `max_adapter_candidates_per_run`
- `status`
- `created_at`
- `policy_attrs`

Required defaults:

- `allow_auto_adapter_activation=False`
- `allow_canonical_skill_import=False`
- `allow_execution_enablement=False`
- `require_review=True`
- `min_mapping_confidence_for_candidate=0.35`

### `ObservedCapabilityCandidate`

Fields:

- `observed_capability_id`
- `observed_run_id`
- `inference_id`
- `fingerprint_id`
- `capability_name`
- `capability_category`
- `observed_action_sequence`
- `observed_object_types`
- `observed_effect_profile`
- `observed_input_shape`
- `observed_output_shape`
- `risk_class`
- `confidence`
- `evidence_refs`
- `withdrawal_conditions`
- `created_at`
- `capability_attrs`

Confidence must be clamped to `[0.0, 1.0]`.

### `ChantaCoreTargetSkillCandidate`

Fields:

- `target_candidate_id`
- `observed_capability_id`
- `target_skill_id`
- `target_skill_layer`
- `target_capability_category`
- `match_reason`
- `match_confidence`
- `supported_now`
- `requires_future_track`
- `created_at`
- `target_attrs`

### `AdapterInputMappingSpec`

Fields:

- `input_mapping_id`
- `adapter_candidate_id`
- `source_input_shape`
- `target_input_schema`
- `field_mappings`
- `missing_required_fields`
- `default_values`
- `transformation_notes`
- `confidence`
- `created_at`
- `input_mapping_attrs`

### `AdapterOutputMappingSpec`

Fields:

- `output_mapping_id`
- `adapter_candidate_id`
- `source_output_shape`
- `target_output_schema`
- `field_mappings`
- `unsupported_output_fields`
- `preview_strategy`
- `confidence`
- `created_at`
- `output_mapping_attrs`

### `AdapterUnsupportedFeature`

Fields:

- `unsupported_feature_id`
- `adapter_candidate_id`
- `observed_capability_id`
- `feature_type`
- `severity`
- `message`
- `future_track_hint`
- `evidence_refs`
- `created_at`
- `feature_attrs`

### `ObservationDigestionAdapterCandidate`

Fields:

- `adapter_candidate_id`
- `observed_capability_id`
- `target_candidate_id`
- `source_runtime`
- `source_skill_ref`
- `source_tool_ref`
- `target_skill_id`
- `mapping_type`
- `mapping_confidence`
- `input_mapping_id`
- `output_mapping_id`
- `unsupported_feature_ids`
- `risk_class`
- `review_status`
- `requires_review`
- `canonical_import_enabled`
- `execution_enabled`
- `created_at`
- `adapter_attrs`

Required defaults:

- `review_status="pending_review"`
- `requires_review=True`
- `canonical_import_enabled=False`
- `execution_enabled=False`

### `ObservationDigestionAdapterReviewRequest`

Fields:

- `review_request_id`
- `adapter_candidate_id`
- `requested_by`
- `review_reason`
- `status`
- `created_at`
- `request_attrs`

### `ObservationDigestionAdapterFinding`

Fields:

- `finding_id`
- `subject_ref`
- `finding_type`
- `status`
- `severity`
- `message`
- `evidence_ref`
- `created_at`
- `finding_attrs`

### `ObservationDigestionAdapterBuildResult`

Fields:

- `build_result_id`
- `operation_kind`
- `status`
- `observed_run_id`
- `inference_id`
- `observed_capability_ids`
- `target_candidate_ids`
- `adapter_candidate_ids`
- `unsupported_feature_ids`
- `finding_ids`
- `summary`
- `created_at`
- `result_attrs`

## Source Objects

The builder must accept these existing observation/digestion objects:

- `AgentBehaviorInferenceV2`
- `ExternalSkillBehaviorFingerprint`
- `ObservedAgentRun`

Supported build methods:

- `build_from_behavior_inference(inference)`
- `build_from_behavior_fingerprint(fingerprint)`
- `build_from_observed_run(observed_run)`

## Deterministic Extraction Rules

Capability category extraction:

- `read_object`, `file_read_observed` -> `read_file`
- `search_object`, `file_search_observed` -> `search_file`
- `summarize_object`, `summary_observed` -> `summarize_content`
- `create_candidate` -> `create_candidate`
- `verify_result` -> `verify_result`
- `delegate_task` -> `delegate_task`
- `execute_action` with shell or command hints -> `shell_execution`
- workspace file changed/write/edit/patch hints -> `write_file`
- external system/http/url/network hints -> `network_access`
- MCP/server/tool-resource hints -> `mcp_connection`
- plugin/load/extension hints -> `plugin_loading`
- observation inference hints -> `observation`
- digestion/static-digest/assimilate hints -> `digestion`

Extraction must not infer support for unsafe categories. Unsafe categories remain observed capability candidates plus unsupported feature records.

## Target Matching Rules

Target skill mapping:

- `read_file` -> `skill:read_workspace_text_file`
- `search_file` -> `skill:grep_workspace_text`
- `summarize_content` -> `skill:summarize_workspace_markdown`
- `create_candidate` -> `skill:external_skill_assimilate`
- `verify_result` -> conformance/verification target
- `delegate_task` -> review/future delegation target
- `observation` -> `skill:agent_behavior_infer`
- `digestion` -> `skill:external_skill_static_digest`
- unsafe categories -> `future:<category>`

Unsafe categories:

- `shell_execution`
- `write_file`
- `network_access`
- `mcp_connection`
- `plugin_loading`
- `external_harness_execution`

Future track hints:

These hints are superseded by the current release-line orientation. `v0.20.x`
is OCEL-native Self-Awareness, not a write/shell/network/MCP/plugin safety
track. Unsafe capabilities remain deferred to post-v0.20 release lines. The
next line, `v0.21.x` Deep Self-Introspection, may inspect runtime, capability,
policy, context, and trace consistency from an OCEL viewpoint, but it does not
grant the unsafe capabilities below unless a later safety layer explicitly
defines and verifies them.

- shell execution -> post-v0.20 dedicated execution safety track
- write file -> post-v0.20 dedicated mutation/write safety track
- network access -> post-v0.20 dedicated external contact safety track
- MCP connection -> post-v0.20 dedicated external contact/adapter safety track
- plugin loading -> post-v0.20 dedicated plugin/adapter safety track
- external harness execution -> post-v0.20 dedicated external harness safety track

## Service Contract

Implement `ObservationToDigestionAdapterBuilderService`.

Required methods:

- `create_default_policy(...)`
- `extract_observed_capabilities(...)`
- `match_target_skills(...)`
- `create_input_mapping_spec(...)`
- `create_output_mapping_spec(...)`
- `detect_unsupported_features(...)`
- `create_adapter_candidate(...)`
- `create_review_request(...)`
- `build_from_behavior_inference(...)`
- `build_from_behavior_fingerprint(...)`
- `build_from_observed_run(...)`
- `record_finding(...)`
- `record_result(...)`
- `render_adapter_build_cli(...)`

Operational requirements:

- Clear per-build in-memory lists before each full build.
- Record a default policy unless caller supplies one.
- Record low-confidence target matches as `low_mapping_confidence` findings.
- Create no adapter candidate when mapping confidence is below policy threshold.
- Always create candidates with review required.
- Never enable execution or canonical import.
- Create review requests for created candidates.
- Keep generated summaries redacted.

## CLI

Add command group:

`chanta-cli digest adapter-build`

Subcommands:

- `from-inference --inference-json-file <path>`
- `from-fingerprint --fingerprint-json-file <path>`
- `from-observed-run --observed-run-json-file <path>`
- `show <adapter_candidate_id>`
- `unsupported <adapter_candidate_id>`

Required CLI output:

- observed capability count/details
- target skill candidate count/details
- adapter candidate count/details
- unsupported feature count/details
- `review_status=pending_review`
- `canonical_import_enabled=false`
- `execution_enabled=false`

`show` and `unsupported` may provide controlled diagnostics if no persisted query surface exists. They must remain read-only.

## OCEL Shape

Object types:

- `observation_to_digestion_adapter_policy`
- `observed_capability_candidate`
- `chantacore_target_skill_candidate`
- `adapter_input_mapping_spec`
- `adapter_output_mapping_spec`
- `adapter_unsupported_feature`
- `observation_digestion_adapter_candidate`
- `observation_digestion_adapter_review_request`
- `observation_digestion_adapter_finding`
- `observation_digestion_adapter_build_result`

Event activities:

- `observation_to_digestion_adapter_policy_registered`
- `observed_capability_candidate_created`
- `chantacore_target_skill_candidate_created`
- `adapter_input_mapping_spec_created`
- `adapter_output_mapping_spec_created`
- `adapter_unsupported_feature_recorded`
- `observation_digestion_adapter_candidate_created`
- `observation_digestion_adapter_review_requested`
- `observation_digestion_adapter_finding_recorded`
- `observation_digestion_adapter_build_result_recorded`

Expected object-object relation qualifiers:

- `observed_capability_derived_from_behavior_inference`
- `observed_capability_derived_from_fingerprint`
- `target_skill_candidate_maps_observed_capability`
- `adapter_candidate_uses_observed_capability`
- `adapter_candidate_targets_skill_candidate`
- `input_mapping_belongs_to_adapter_candidate`
- `output_mapping_belongs_to_adapter_candidate`
- `unsupported_feature_belongs_to_adapter_candidate`
- `review_request_reviews_adapter_candidate`
- `build_result_summarizes_adapter_build`
- `finding_belongs_to_adapter_build`

Best-effort relation coverage is acceptable, but object and event emission is required.

## Context History Adapter

Add history conversion functions with source:

`observation_to_digestion_adapter_builder`

Required functions:

- `observed_capability_candidates_to_history_entries`
- `target_skill_candidates_to_history_entries`
- `adapter_candidates_to_history_entries`
- `unsupported_features_to_history_entries`
- `adapter_build_results_to_history_entries`
- `adapter_findings_to_history_entries`

Priority rules:

- unsupported feature -> high
- unsafe capability -> high
- low-confidence finding -> medium
- pending review candidate -> medium
- completed result -> low/medium

## PIG/OCPX Report Support

Add a summary method to `PIGReportService`.

Required count keys:

- `observation_to_digestion_adapter_policy_count`
- `observed_capability_candidate_count`
- `chantacore_target_skill_candidate_count`
- `adapter_input_mapping_spec_count`
- `adapter_output_mapping_spec_count`
- `adapter_unsupported_feature_count`
- `observation_digestion_adapter_candidate_count`
- `observation_digestion_adapter_review_request_count`
- `observation_digestion_adapter_finding_count`
- `observation_digestion_adapter_build_result_count`

Required grouping keys:

- `adapter_candidate_by_risk_class`
- `adapter_candidate_by_target_skill_id`
- `adapter_candidate_by_mapping_type`
- `unsupported_feature_by_type`
- `observed_capability_by_category`

Report text should include a readable section named `Observation-to-Digestion Adapter Builder`.

## Restore Implementation Sequence

1. Add ID constructors.
2. Add `adapter_builder.py` dataclasses and service.
3. Export the new models, service, and history adapter functions from `chanta_core.digestion`.
4. Add CLI parser entries under `digest adapter-build`.
5. Add CLI handler for inference/fingerprint/observed-run builds.
6. Add PIG/OCPX summary counts and report text.
7. Update import smoke test.
8. Add v0.19.8 tests.
9. Bump version to `0.19.8`.
10. Run install and tests.
11. Run forbidden/private scan on v0.19.8 public files.

## Acceptance Commands

Install:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

Targeted tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_observation_to_digestion_adapter_models.py tests\test_observation_to_digestion_adapter_service.py tests\test_observation_to_digestion_adapter_mapping.py tests\test_observation_to_digestion_adapter_cli.py tests\test_observation_to_digestion_adapter_ocel_shape.py tests\test_observation_to_digestion_adapter_history_adapter.py tests\test_observation_to_digestion_adapter_boundaries.py tests\test_observation_to_digestion_adapter_unsupported.py tests\test_observation_to_digestion_adapter_pig.py
```

Full suite:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Expected v0.19.8 observed result at creation time:

- targeted adapter tests: passed
- full suite: passed
- package version after install: `0.19.8`

## Boundary Scan

Scan v0.19.8 public files for execution/network/plugin/LLM/mutation tokens. The exact scan can vary, but it should include:

- adapter execution enablement tokens
- external harness/script execution tokens
- shell/network/MCP/plugin tokens
- LLM completion tokens
- memory/persona/overlay mutation tokens
- true default for canonical import enablement
- true default for execution enablement
- private names and private local roots

Findings should be zero for v0.19.8 new public files.

## Non-Goals

- No adapter execution.
- No external harness execution.
- No external script execution.
- No canonical import.
- No JSONL canonical adapter store.
- No write, shell, network, MCP, or plugin safety implementation.
- No LLM calls.
- No memory, persona, or overlay mutation.

## Known Limitations

- Adapter candidates are design/review artifacts only.
- Unsafe categories are detected but not made executable.
- `show` and `unsupported` CLI commands do not imply a durable canonical adapter store.
- Future safety tracks are required before write/shell/network/MCP/plugin behavior can become actionable.

## Restore Confidence

Restore is possible from this document plus the test names above if the surrounding v0.19.x codebase exists. If only this document exists and no codebase context remains, the dataclass fields and service methods here are sufficient to reconstruct the public surface, but exact helper implementation details such as confidence scoring may require re-derivation from tests.

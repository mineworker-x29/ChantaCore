# ChantaCore v0.24.0 Restore Record - Internal Provider Contract

## Version Identity

- Version: v0.24.0
- Version name: Internal Provider Contract
- Korean name: 내부 Provider 계약
- Track: Internal Provider / Local Runtime Provider
- Previous release: v0.23.9 Internal Dominion Consolidation / Release Readiness
- Next release: v0.24.1 Provider Registry & Capability Surface
- Restore document class: restore-grade version record

This document is intentionally longer than a release note. Its purpose is to let a future maintainer reconstruct the expected source, runtime boundary, trace visibility, CLI, and test state for v0.24.0 without guessing.

## Restore Goal

Restore v0.24.0 to the contract-only Internal Provider foundation that follows the v0.23.9 Internal Dominion Foundation closure. The restored state must define internal provider semantics, provider type descriptors, effect policy, permission policy, invocation boundary, observability contract, safety boundary, roadmap boundary, and a contract report.

The restored state must not execute providers. It must not read workspace files as a provider action, search repositories as a provider action, inspect OCEL/PIG/OCPX live stores as a provider action, run local commands, invoke external providers, expose credentials, or introduce company-specific split logic.

## Public Boundary

This is public ChantaCore core work. Restore work must not import, expose, or hard-code private persona material, company-specific Schumpeter material, credentials, tokens, raw secrets, or private absolute paths.

Vendor names such as A360, Automation Anywhere, Brity, UiPath, and Power Automate are allowed only as future adapter examples in docs or tests. They must not appear as runtime logic in the internal provider contract implementation.

## Facts, Assumptions, And Judgment

Confirmed facts from the implemented v0.24.0 unit:

- The internal provider layer is implemented as contract-only code.
- The CLI exposes read-only provider contract views.
- The v0.24.0 report can be created.
- Targeted, related, and full regression tests were run after implementation.
- Forbidden search over the changed v0.24.0 files found no enabled provider invocation, local command execution, external adapter, Schumpeter split, credential exposure, or vendor-specific runtime logic.

Assumptions:

- v0.24.1 will add provider registry and capability surface work without changing v0.24.0's no-invocation guarantees.
- Existing v0.23.x restore and version documents remain source-compatible and are not rewritten by this restore record.

Judgment:

v0.24.0 is restoreable as a contract-only release if the files, tests, CLI outputs, and forbidden-search checks listed below remain true. This judgment should be withdrawn if any invocation, local command execution, credential exposure, external adapter, or premature v0.25+ feature appears in the v0.24.0 implementation.

## Source State

Primary implementation files:

- `src/chanta_core/internal_provider/contract.py`
- `src/chanta_core/internal_provider/__init__.py`
- `src/chanta_core/cli/main.py`
- `src/chanta_core/__init__.py`
- `pyproject.toml`

Primary tests:

- `tests/test_internal_provider_contract.py`
- `tests/test_internal_provider_contract_boundaries.py`

Primary docs:

- `docs/versions/v0.24/chanta_core_v0_24_0_restore.md`
- `docs/versions/v0.24/README.md`

Related predecessor docs and tests:

- v0.23.9 Internal Dominion consolidation docs and tests
- v0.23.8 dispatch boundary docs and tests
- v0.23.x Internal Dominion Foundation tests
- v0.22.x, v0.21.x, and v0.20.x regression tests

## Runtime State

v0.24.0 must restore to this runtime boundary:

- `provider_invocation_enabled=false`
- `workspace_read_execution_enabled=false`
- `repository_search_execution_enabled=false`
- `file_read_execution_enabled=false`
- `local_runtime_execution_enabled=false`
- `local_command_execution_enabled=false`
- `external_provider_adapter_implemented=false`
- `schumpeter_split_introduced=false`
- `credential_exposed=false`
- `raw_secret_output=false`
- `llm_judge_used=false`
- `ready_for_v0_25=false`
- `next_required_step=v0.24.1 Provider Registry & Capability Surface`

The only intended v0.24.0 effect types are:

- `read_only_observation`
- `state_candidate_created`
- `provider_contract_declared`

## Core Principles

- Provider is not arbitrary tool execution.
- Provider is not external adapter.
- Provider is not agent UX.
- Provider is an OCEL-visible internal capability surface.
- Provider invocation must be gated by effect type.
- Read-only provider is still governed by policy.
- Local runtime provider is not unrestricted shell.
- Internal provider must never expose credentials or raw secrets.
- Internal provider must remain public-core safe.

## Introduced Skill State

Implemented skill:

- `skill:internal_provider_contract_view`

This skill is read-only, contract-only, non-invoking, non-executing, and does not use an LLM judge.

Future v0.24 skills remain contract-only or stub-level:

- `skill:internal_provider_registry_view`
- `skill:internal_provider_capability_surface_view`
- `skill:workspace_read_provider_view`
- `skill:repository_search_provider_view`
- `skill:file_read_provider_view`
- `skill:ocel_inspection_provider_view`
- `skill:pig_inspection_provider_view`
- `skill:ocpx_projection_provider_view`
- `skill:local_runtime_command_candidate_create`
- `skill:local_runtime_static_safety_check`
- `skill:local_runtime_preflight_check`
- `skill:local_runtime_execution_gate`
- `skill:bounded_local_command_run`
- `skill:local_runtime_output_summarize`
- `skill:local_runtime_failure_explain`
- `skill:internal_provider_consolidation_view`

## Data Models

The restored v0.24.0 implementation must expose these models or project-style equivalents:

- `InternalProviderContract`
- `InternalProviderTypeDescriptor`
- `InternalProviderCapabilityContract`
- `InternalProviderEffectPolicy`
- `InternalProviderPermissionPolicy`
- `InternalProviderInvocationBoundary`
- `InternalProviderObservabilityContract`
- `InternalProviderSafetyBoundary`
- `InternalProviderRoadmapBoundary`
- `InternalProviderContractFinding`
- `InternalProviderContractReport`

The contract object is the root. It contains provider types, capability contract, effect policy, permission policy, invocation boundary, observability contract, safety boundary, roadmap boundary, and contract status.

The report object is the release-facing view. It records findings, readiness for v0.24.1, continued deferral of v0.25, and the disabled execution flags.

## Provider Types

The restored contract must list these provider types:

- `workspace_read_provider`
- `repository_search_provider`
- `file_read_provider`
- `ocel_inspection_provider`
- `pig_inspection_provider`
- `ocpx_projection_provider`
- `local_runtime_provider`
- `diagnostic_provider`
- `candidate_generation_provider`
- `unknown`

For all v0.24.0 internal provider types:

- `external_adapter=false`
- `provider_api_call_required=false`
- `external_runtime_touch_required=false`
- `credential_materialization_required=false`
- implementation status is `contract_only`, `future_track`, or `blocked`
- allowed and forbidden effect type lists are explicit
- future version notes are explicit where applicable

## Capability Contract

The capability contract must require:

- capability id
- provider type
- input schema
- output schema
- effect type
- permission policy
- OCEL mapping
- PIG projection
- OCPX projection
- safety boundary
- failure explanation
- raw secret output prohibition
- private path sanitization

This contract is structural. It does not create live provider behavior in v0.24.0.

## Effect Policy

Allowed in v0.24.0:

- `read_only_observation`
- `state_candidate_created`
- `provider_contract_declared`

Future effect types, not active in v0.24.0:

- `provider_surface_declared`
- `provider_candidate_created`
- `workspace_tree_observed`
- `repository_search_performed`
- `file_excerpt_read`
- `process_state_inspected`
- `local_command_candidate_created`
- `local_runtime_static_safety_checked`
- `local_runtime_preflight_checked`
- `bounded_local_command_executed`
- `local_output_captured`
- `local_runtime_outcome_candidate_created`

Forbidden in v0.24.0:

- `provider_invoked`
- `workspace_file_read_executed`
- `repository_search_executed`
- `file_content_extracted`
- `local_command_executed`
- `bounded_local_command_executed`
- `unrestricted_shell_executed`
- `network_accessed`
- `package_installed`
- `destructive_command_executed`
- `external_runtime_touched`
- `external_control_dispatched`
- `credential_exposed`
- `raw_secret_output`
- `memory_mutated`
- `persona_mutated`
- `external_provider_called`

## Permission Policy

The restored permission policy must preserve:

- `deny_by_default=true`
- `read_only_requires_policy=true`
- `candidate_creation_requires_policy=true`
- `execution_requires_gate=true`
- `local_runtime_execution_requires_allowlist=true`
- `local_runtime_execution_requires_timeout=true`
- `local_runtime_execution_requires_output_cap=true`
- `local_runtime_execution_requires_redaction=true`
- `local_runtime_execution_requires_side_effect_scan=true`
- `network_forbidden_by_default=true`
- `package_install_forbidden_by_default=true`
- `destructive_command_forbidden_by_default=true`
- `credential_access_forbidden_by_default=true`
- `secret_output_forbidden=true`
- `private_path_sanitization_required=true`

## Invocation Boundary

The restored invocation boundary must keep all execution paths disabled:

- `invocation_enabled_v0_24_0=false`
- `workspace_read_execution_enabled_v0_24_0=false`
- `repository_search_execution_enabled_v0_24_0=false`
- `file_read_execution_enabled_v0_24_0=false`
- `ocel_inspection_execution_enabled_v0_24_0=false`
- `local_runtime_execution_enabled_v0_24_0=false`
- `local_command_execution_enabled_v0_24_0=false`
- `external_provider_invocation_enabled=false`
- `shell_execution_enabled=false`
- `network_enabled=false`
- `mcp_enabled=false`
- `plugin_enabled=false`
- `llm_judge_enabled=false`

## Observability Contract

The restored observability contract must state:

- `ocel_visible=true`
- `pig_visible=true`
- `ocpx_visible=true`
- `execution_envelope_visible=true`
- provider invocation must emit an event in future versions
- provider invocation must record effect type in future versions
- provider results must be sanitized
- provider failures must be explainable
- raw secret output is forbidden
- private path sanitization is required
- workbench visibility is future-facing only

## Safety Boundary

The restored safety boundary must keep these counts at zero:

- `provider_invocation_count`
- `workspace_file_read_execution_count`
- `repository_search_execution_count`
- `file_content_extraction_count`
- `local_command_execution_count`
- `bounded_local_command_execution_count`
- `unrestricted_shell_count`
- `provider_api_call_count`
- `external_runtime_touch_count`
- `external_dispatch_count`
- `network_access_count`
- `package_install_count`
- `destructive_command_count`
- `credential_exposure_count`
- `raw_secret_output_count`
- `llm_judge_count`
- `external_provider_adapter_count`
- `schumpeter_split_count`

Any nonzero dangerous count should make the contract report failed or blocked according to severity.

## Roadmap Boundary

The restored roadmap boundary must preserve:

- current track: `v0.24.x Internal Provider / Local Runtime Provider`
- current version scope: `v0.24.0 contract_only`
- next version: `v0.24.1 Provider Registry & Capability Surface`
- v0.25 deferred: General Agent Usability & Tool Routing
- v0.26 deferred: Workspace Agent Workbench
- v0.27 deferred: Memory Candidate & Continuity
- v0.28 deferred: Public Alpha / Schumpeter Split Preparation
- v0.29+ deferred: External Skill / External Provider Adapter Development
- GrowthKernel bridge deferred

## PIG Projection

The v0.24.0 PIG projection must identify:

- version: `v0.24.0`
- layer: `internal_provider`
- subject: `internal_provider_contract`
- next step: `v0.24.1 Provider Registry & Capability Surface`

Required principles:

- provider is not arbitrary tool execution
- provider is not external adapter
- provider is not agent UX
- provider is an OCEL-visible internal capability surface
- provider invocation must be gated by effect type
- local runtime provider is not unrestricted shell

Required safety boundary values:

- `provider_invocation_enabled=false`
- `workspace_read_execution_enabled=false`
- `repository_search_execution_enabled=false`
- `file_read_execution_enabled=false`
- `local_runtime_execution_enabled=false`
- `local_command_execution_enabled=false`
- `external_provider_adapter_implemented=false`
- `unrestricted_shell_enabled=false`
- `network_enabled=false`
- `package_install_enabled=false`
- `destructive_command_enabled=false`
- `credential_exposed=false`
- `raw_secret_output=false`
- `schumpeter_split_introduced=false`
- `llm_judge_enabled=false`

## OCPX Projection

The v0.24.0 OCPX projection must identify:

- state: `internal_provider_contract_declared`
- version: `v0.24.0`
- source read models:
  - `InternalDominionConsolidationState`
  - `InternalDominionReleaseState`
  - `V024ReadinessState`
- target read models:
  - `InternalProviderContractState`
  - `InternalProviderTypeState`
  - `InternalProviderEffectPolicyState`
  - `InternalProviderPermissionPolicyState`
  - `InternalProviderInvocationBoundaryState`
  - `InternalProviderRoadmapBoundaryState`
- effect types:
  - `read_only_observation`
  - `state_candidate_created`
  - `provider_contract_declared`

## OCEL Mapping

The restored OCEL mapping must include object types:

- `internal_provider_contract`
- `internal_provider_type_descriptor`
- `internal_provider_capability_contract`
- `internal_provider_effect_policy`
- `internal_provider_permission_policy`
- `internal_provider_invocation_boundary`
- `internal_provider_observability_contract`
- `internal_provider_safety_boundary`
- `internal_provider_roadmap_boundary`
- `internal_provider_contract_finding`
- `internal_provider_contract_report`
- `internal_dominion_consolidation_report`
- `execution_envelope`
- `pig_report`
- `ocpx_projection`

Event types:

- `internal_provider_contract_requested`
- `internal_provider_type_descriptors_created`
- `internal_provider_effect_policy_created`
- `internal_provider_permission_policy_created`
- `internal_provider_invocation_boundary_created`
- `internal_provider_observability_contract_created`
- `internal_provider_safety_boundary_created`
- `internal_provider_roadmap_boundary_created`
- `internal_provider_contract_report_created`
- `internal_provider_contract_blocked`

Relation types:

- `declares_internal_provider_contract`
- `declares_internal_provider_type`
- `declares_internal_provider_capability_contract`
- `declares_internal_provider_effect_policy`
- `declares_internal_provider_permission_policy`
- `declares_internal_provider_invocation_boundary`
- `declares_internal_provider_observability_contract`
- `declares_internal_provider_safety_boundary`
- `declares_internal_provider_roadmap_boundary`
- `prepares_provider_registry`
- `prepares_workspace_read_provider`
- `prepares_repository_search_provider`
- `prepares_ocel_inspection_provider`
- `prepares_local_runtime_provider`
- `defers_provider_invocation_to_later_v0_24`
- `defers_local_runtime_execution_to_later_v0_24`
- `defers_general_agent_usability_to_v0_25`
- `defers_workspace_workbench_to_v0_26`
- `defers_memory_continuity_to_v0_27`
- `defers_schumpeter_split_to_v0_28`
- `defers_external_provider_adapters_to_v0_29_plus`
- `not_provider_invoked`
- `not_local_command_executed`
- `not_external_runtime_touched`
- `not_external_provider_called`
- `prevents_credential_exposure`
- `visible_in_workbench_future`
- `recorded_in_envelope`
- `derived_from_internal_dominion_consolidation`

Forbidden effects must not be emitted as actual effects in v0.24.0.

## CLI Restore Surface

The restored CLI must expose read-only contract views:

- `python -m chantacore.cli provider contract`
- `python -m chantacore.cli provider types`
- `python -m chantacore.cli provider effect-policy`
- `python -m chantacore.cli provider permission-policy`
- `python -m chantacore.cli provider invocation-boundary`
- `python -m chantacore.cli provider observability`
- `python -m chantacore.cli provider safety-boundary`
- `python -m chantacore.cli provider roadmap-boundary`

Expected CLI output properties:

- shows `version=v0.24.0`
- shows `layer=internal_provider`
- shows `status=contract_only`
- shows `provider_invocation_enabled=false`
- shows `workspace_read_execution_enabled=false`
- shows `repository_search_execution_enabled=false`
- shows `local_runtime_execution_enabled=false`
- shows `local_command_execution_enabled=false`
- shows `external_provider_adapter_implemented=false`
- shows `schumpeter_split_introduced=false`
- shows `ready_for_v0_24_1`
- shows `ready_for_v0_25=false`
- shows `next_required_step=v0.24.1 Provider Registry & Capability Surface`
- does not print credential values, raw secrets, or private full paths

## Test Commands And Recorded Results

Targeted v0.24.0 tests:

```powershell
.venv\Scripts\python.exe -m pytest tests\test_internal_provider_contract.py tests\test_internal_provider_contract_boundaries.py
```

Recorded result after v0.24.0 implementation:

```text
15 passed
```

Related provider and Dominion consolidation tests:

```powershell
.venv\Scripts\python.exe -m pytest tests\test_code_hygiene_static.py tests\test_internal_provider_contract.py tests\test_internal_provider_contract_boundaries.py tests\test_internal_dominion_consolidation.py tests\test_internal_dominion_consolidation_boundaries.py
```

Recorded result after v0.24.0 implementation:

```text
34 passed
```

Full regression suite:

```powershell
.venv\Scripts\python.exe -m pytest
```

Recorded result after v0.24.0 implementation:

```text
1773 passed, 1 skipped, 3 warnings in 337.10s
```

If these numbers differ during future restore, treat the difference as evidence requiring investigation. Passing tests alone are not sufficient if forbidden execution behavior is present.

## Forbidden Search Restore Checks

Search changed v0.24.0 files for enabled forbidden behavior:

```powershell
rg -n "provider_invoked=True|workspace_file_read_executed=True|repository_search_executed=True|file_content_extracted=True|local_command_executed=True|bounded_local_command_executed=True|unrestricted_shell_executed=True|provider_invocation_enabled=True|workspace_read_execution_enabled=True|repository_search_execution_enabled=True|file_read_execution_enabled=True|ocel_inspection_execution_enabled=True|local_runtime_execution_enabled=True|local_command_execution_enabled=True|external_provider_adapter_implemented=True|external_runtime_touched=True|external_control_dispatched=True|credential_exposed=True|raw_secret_output=True|network_enabled=True|package_install_enabled=True|destructive_command_enabled=True|schumpeter_split_introduced=True|growthkernel_dependency_required=True" src\chanta_core\internal_provider tests\test_internal_provider_contract.py tests\test_internal_provider_contract_boundaries.py docs\versions\v0.24
```

Expected result:

```text
No enabled forbidden flags in changed v0.24.0 implementation files.
```

Search vendor names:

```powershell
rg -n "A360|Automation Anywhere|Brity|UiPath|Power Automate" src\chanta_core\internal_provider tests\test_internal_provider_contract.py tests\test_internal_provider_contract_boundaries.py
```

Expected result:

```text
No vendor-specific runtime logic in internal provider contract implementation.
```

Search `llm_judge`:

```powershell
rg -n "llm_judge" src\chanta_core\internal_provider tests\test_internal_provider_contract.py tests\test_internal_provider_contract_boundaries.py docs\versions\v0.24
```

Expected result:

```text
Only disabled fields, zero-count safety checks, documentation, or tests asserting no LLM judge.
```

## Restore Procedure

1. Confirm version identity in `pyproject.toml` and `src/chanta_core/__init__.py`.
2. Confirm `src/chanta_core/internal_provider/contract.py` defines the model and service set listed in this document.
3. Import and build an `InternalProviderContractReport` through the report service.
4. Confirm all invocation and execution flags are false.
5. Confirm all safety boundary dangerous counts are zero.
6. Run all provider CLI commands listed above.
7. Run targeted v0.24.0 tests.
8. Run related provider and Dominion consolidation tests.
9. Run the full regression suite.
10. Run forbidden searches over the changed v0.24.0 implementation, test, and docs files.
11. Confirm no credential values, raw secrets, or private full paths appear in CLI output or docs.
12. Confirm v0.24.1 remains the next required step and v0.25 readiness remains false.

## Restore Checklist

- [ ] `InternalProviderContract` builds.
- [ ] Provider type descriptors build.
- [ ] Capability contract builds.
- [ ] Effect policy builds.
- [ ] Permission policy builds.
- [ ] Invocation boundary builds with all execution disabled.
- [ ] Observability contract builds.
- [ ] Safety boundary builds with dangerous counts at zero.
- [ ] Roadmap boundary builds.
- [ ] Contract report builds.
- [ ] `ready_for_v0_24_1` is calculated.
- [ ] `ready_for_v0_25=false`.
- [ ] No provider invocation is enabled.
- [ ] No workspace, repo, or file read execution is enabled.
- [ ] No local command execution is enabled.
- [ ] No external provider adapter is implemented.
- [ ] No Schumpeter split or company-specific wrapper is introduced.
- [ ] No credential value is stored or output.
- [ ] No LLM judge is used.
- [ ] OCEL/PIG/OCPX visibility exists.
- [ ] CLI contract views work.
- [ ] Targeted v0.24.0 tests pass.
- [ ] Related v0.23.9 and provider tests pass.
- [ ] Full regression suite passes or any difference is explicitly explained.

## Known Limitations

- v0.24.0 does not implement a provider registry. That is deferred to v0.24.1.
- v0.24.0 does not implement provider capability surface execution.
- v0.24.0 does not implement workspace tree observation, repository search, file excerpt reading, process inspection, local runtime preflight, bounded local command execution, or output capture.
- v0.24.0 does not implement General Agent Usability, Workspace Agent Workbench, Memory Candidate / Continuity, external provider adapters, or Schumpeter split logic.
- v0.24.0 readiness is based on deterministic contract objects, tests, CLI views, and forbidden-search checks. It is not a live provider readiness claim.

## Withdrawal Conditions

Withdraw the v0.24.0 restore-readiness judgment if any of these become true:

- provider invocation is enabled in v0.24.0
- workspace, repository, or file read execution is enabled in v0.24.0
- local runtime execution or local command execution is enabled in v0.24.0
- shell, network, package install, destructive command, MCP, or plugin execution is introduced
- external provider adapter logic is implemented in internal provider core
- credential values, tokens, raw secrets, or private full paths are exposed
- vendor-specific runtime logic is added to the internal provider contract implementation
- GrowthKernel becomes an active runtime dependency
- General Agent UX, Workspace Agent Workbench, Memory Candidate / Continuity, or Schumpeter split logic appears prematurely
- an LLM judge is used for contract readiness

## Validity Horizon

This restore record is valid until v0.24.1 Provider Registry & Capability Surface begins, or until internal provider policy changes. After either event, future restore records should treat this document as the v0.24.0 baseline rather than as authority for later provider behavior.

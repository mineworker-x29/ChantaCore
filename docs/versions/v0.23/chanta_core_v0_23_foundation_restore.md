# ChantaCore v0.23.x Restore Record - Internal Dominion Foundation v1

## Version Identity

- Version range: v0.23.0 through v0.23.9
- Foundation name: OCEL-native Internal Dominion Foundation v1
- Track: Internal Dominion Foundation
- Previous foundation dependency: v0.22.9 Self-Modification Safety Foundation v1
- Next track: v0.24.x Internal Provider / Local Runtime Provider
- Restore document class: restore-grade foundation record

This document is the restore-grade baseline for v0.23.x. It complements the
short version contracts stored in `docs/versions/` and the per-version addenda
stored in this folder.

## Restore Goal

Restore v0.23.x as the non-executing Internal Dominion Foundation that defines
control grammar, inventory, capability observation, action candidates, control
plans, static safety, preflight boundaries, human review gates, authorization
and dispatch boundaries, and release readiness.

The restored state must not perform actual dispatch, provider API calls,
external runtime touch, authorization consumption, live status tracking, live
output fetch, real external outcome recording, local command execution,
General Agent UX, Workspace Agent Workbench, Memory Candidate / Continuity,
external provider adapters, Schumpeter split logic, credential output, or LLM
judge decisions.

## Public Boundary

This restore record is public ChantaCore material. It must not expose private
persona content, company-specific Schumpeter content, credentials, tokens, raw
secrets, or private absolute paths.

Vendor names are allowed only as future adapter examples in docs/tests. They
must not be runtime logic in Internal Dominion implementation.

## Facts, Assumptions, And Judgment

Confirmed facts from local repository state:

- v0.23.0 through v0.23.9 short version contracts exist.
- Internal Dominion implementation files exist under `src/chanta_core/internal_dominion/`.
- v0.23 tests exist for contract, inventory, capability observation, control
  request/candidate, control plan, static safety, runtime preflight, human
  review gate, dispatch boundary, and consolidation.
- v0.23.9 consolidation was previously verified with a full suite result of
  `1758 passed, 1 skipped, 3 warnings`.
- A later full suite after v0.24.0 recorded `1773 passed, 1 skipped, 3 warnings`.

Assumptions:

- The original short version contracts remain useful as version policy records.
- This folder is the canonical restore-grade v0.23.x documentation location
  going forward.

Judgment:

v0.23.x is restoreable as Internal Dominion Foundation v1 if all subject
components, tests, CLI views, OCEL mappings, PIG/OCPX projections, and safety
boundaries listed here remain valid.

Withdraw this judgment if any v0.23.x implementation starts executing providers,
consuming authorization, touching external runtimes, dispatching external
control, exposing credentials, or implementing a future-track feature.

## Included Versions

- v0.23.0: OCEL-native Internal Dominion Contract
- v0.23.1: Runtime / Agent / System Inventory
- v0.23.2: Capability Observation & Digestion for Dominion
- v0.23.3: Control Request & Action Candidate
- v0.23.4: Control Plan & Target Binding
- v0.23.5: Dominion Static Safety Check
- v0.23.6: Runtime Preflight / Reachability Check
- v0.23.7: Human Review & Dominion Gate
- v0.23.8: Authorization / Bounded Dispatch / Status / Outcome Boundary
- v0.23.9: Internal Dominion Consolidation / Release Readiness

## Source State

Primary package:

- `src/chanta_core/internal_dominion/__init__.py`
- `src/chanta_core/internal_dominion/models.py`
- `src/chanta_core/internal_dominion/registry.py`
- `src/chanta_core/internal_dominion/mapping.py`
- `src/chanta_core/internal_dominion/reports.py`
- `src/chanta_core/internal_dominion/migration.py`
- `src/chanta_core/internal_dominion/conformance.py`
- `src/chanta_core/internal_dominion/inventory.py`
- `src/chanta_core/internal_dominion/capability.py`
- `src/chanta_core/internal_dominion/control.py`
- `src/chanta_core/internal_dominion/control_plan.py`
- `src/chanta_core/internal_dominion/static_safety.py`
- `src/chanta_core/internal_dominion/runtime_preflight.py`
- `src/chanta_core/internal_dominion/human_review_gate.py`
- `src/chanta_core/internal_dominion/dispatch_boundary.py`
- `src/chanta_core/internal_dominion/consolidation.py`

Shared surfaces:

- `src/chanta_core/cli/main.py`
- `src/chanta_core/__init__.py`
- `pyproject.toml`

Canonical v0.23 restore records:

- `docs/versions/v0.23/v0.23.0_internal_dominion_contract.md`
- `docs/versions/v0.23/v0.23.1_runtime_agent_system_inventory.md`
- `docs/versions/v0.23/v0.23.2_capability_observation_digestion.md`
- `docs/versions/v0.23/v0.23.3_control_request_action_candidate.md`
- `docs/versions/v0.23/v0.23.4_control_plan_target_binding.md`
- `docs/versions/v0.23/v0.23.5_dominion_static_safety_check.md`
- `docs/versions/v0.23/v0.23.6_runtime_preflight_reachability_check.md`
- `docs/versions/v0.23/v0.23.7_human_review_dominion_gate.md`
- `docs/versions/v0.23/v0.23.8_authorization_bounded_dispatch_status_outcome_boundary.md`
- `docs/versions/v0.23/v0.23.9_internal_dominion_consolidation_release_readiness.md`

## Subject Components

| Version | Subject | Primary module | Primary test files |
| --- | --- | --- | --- |
| v0.23.0 | Internal Dominion Contract | `models.py`, `registry.py`, `mapping.py`, `reports.py`, `migration.py`, `conformance.py` | `test_internal_dominion_contract.py`, `test_internal_dominion_boundaries.py`, `test_internal_dominion_migration.py` |
| v0.23.1 | Runtime / Agent / System Inventory | `inventory.py` | `test_dominion_runtime_inventory.py`, `test_dominion_runtime_inventory_boundaries.py` |
| v0.23.2 | Capability Observation & Digestion | `capability.py` | `test_dominion_capability_observation.py`, `test_dominion_capability_observation_boundaries.py` |
| v0.23.3 | Control Request & Action Candidate | `control.py` | `test_dominion_control_request_candidate.py`, `test_dominion_control_request_candidate_boundaries.py` |
| v0.23.4 | Control Plan & Target Binding | `control_plan.py` | `test_dominion_control_plan.py`, `test_dominion_control_plan_boundaries.py` |
| v0.23.5 | Dominion Static Safety Check | `static_safety.py` | `test_dominion_static_safety.py`, `test_dominion_static_safety_boundaries.py` |
| v0.23.6 | Runtime Preflight / Reachability Check | `runtime_preflight.py` | `test_dominion_runtime_preflight.py`, `test_dominion_runtime_preflight_boundaries.py` |
| v0.23.7 | Human Review & Dominion Gate | `human_review_gate.py` | `test_dominion_human_review_gate.py`, `test_dominion_human_review_gate_boundaries.py` |
| v0.23.8 | Dispatch / Status / Outcome Boundary | `dispatch_boundary.py` | `test_dominion_dispatch_boundary.py`, `test_dominion_dispatch_boundary_boundaries.py` |
| v0.23.9 | Foundation Consolidation | `consolidation.py` | `test_internal_dominion_consolidation.py`, `test_internal_dominion_consolidation_boundaries.py` |

## Runtime Boundary

The restored v0.23.x runtime state must preserve:

- `safe_to_dispatch=false`
- `bounded_dispatch_allowed_now=false`
- `provider_api_call_performed=false`
- `external_runtime_touched=false`
- `dispatch_performed=false`
- `actual_dispatch_performed=false`
- `external_run_started=false`
- `authorization_consumed=false`
- `live_status_tracking_started=false`
- `live_output_fetch_started=false`
- `real_external_outcome_recorded=false`
- `local_runtime_provider_implemented=false`
- `general_agent_usability_implemented=false`
- `workspace_agent_workbench_implemented=false`
- `memory_candidate_continuity_implemented=false`
- `external_provider_adapter_implemented=false`
- `schumpeter_split_introduced=false`
- `credential_exposed=false`
- `raw_secret_output=false`
- `llm_judge_used=false`

## Skill State

Implemented v0.23 Internal Dominion skills:

- `skill:dominion_contract_view`
- `skill:dominion_runtime_inventory`
- `skill:dominion_capability_observe`
- `skill:dominion_capability_digest`
- `skill:dominion_control_request_create`
- `skill:dominion_action_candidate_create`
- `skill:dominion_control_plan_create`
- `skill:dominion_target_binding`
- `skill:dominion_static_safety_check`
- `skill:dominion_runtime_preflight`
- `skill:dominion_review_gate`
- `skill:dominion_authorization_create`
- `skill:dominion_bounded_dispatch`
- `skill:dominion_run_status_track`
- `skill:dominion_run_output_fetch`
- `skill:dominion_outcome_record`
- `skill:dominion_workbench_view`
- `skill:dominion_consolidation_view`

These skills are contract, read-only, candidate, gate, boundary, or
consolidation surfaces. None are actual provider execution surfaces.

## OCEL / PIG / OCPX Restore Expectations

Restore must preserve OCEL as the canonical substrate. JSONL must not be
introduced as canonical store for v0.23.x.

Expected effect types include only non-executing categories such as:

- `read_only_observation`
- `state_candidate_created`
- `gate_state_created`
- `boundary_state_created`
- `consolidation_state_created`
- `workbench_snapshot_created`

Forbidden effects must not be emitted as actual v0.23 effects:

- `external_runtime_touched`
- `external_control_dispatched`
- `external_run_started`
- `network_accessed`
- `plugin_loaded`
- `mcp_connected`
- `shell_executed`
- `credential_exposed`
- `authorization_consumed`
- `live_status_tracked`
- `live_output_fetched`
- `external_outcome_recorded`
- `outcome_recorded`

## CLI Restore Surface

Expected Dominion CLI families include:

- `python -m chantacore.cli dominion contract`
- `python -m chantacore.cli dominion inventory`
- `python -m chantacore.cli dominion capability ...`
- `python -m chantacore.cli dominion control ...`
- `python -m chantacore.cli dominion static-safety ...`
- `python -m chantacore.cli dominion preflight ...`
- `python -m chantacore.cli dominion gate ...`
- `python -m chantacore.cli dominion dispatch-boundary ...`
- `python -m chantacore.cli dominion consolidate`
- `python -m chantacore.cli dominion release-manifest`
- `python -m chantacore.cli dominion readiness`
- `python -m chantacore.cli dominion safety-boundary`
- `python -m chantacore.cli dominion roadmap-boundary`
- `python -m chantacore.cli dominion gaps`
- `python -m chantacore.cli dominion workbench`

CLI output must remain sanitized and must not print credential values, raw
secrets, or private full paths.

## Test Commands And Recorded Results

Targeted v0.23.9 consolidation tests:

```powershell
.venv\Scripts\python.exe -m pytest tests\test_internal_dominion_consolidation.py tests\test_internal_dominion_consolidation_boundaries.py
```

Targeted v0.23.8 dispatch boundary tests:

```powershell
.venv\Scripts\python.exe -m pytest tests\test_dominion_dispatch_boundary.py tests\test_dominion_dispatch_boundary_boundaries.py
```

Representative v0.23 subject tests:

```powershell
.venv\Scripts\python.exe -m pytest tests\test_internal_dominion_contract.py tests\test_internal_dominion_boundaries.py tests\test_internal_dominion_migration.py
.venv\Scripts\python.exe -m pytest tests\test_dominion_runtime_inventory.py tests\test_dominion_runtime_inventory_boundaries.py
.venv\Scripts\python.exe -m pytest tests\test_dominion_capability_observation.py tests\test_dominion_capability_observation_boundaries.py
.venv\Scripts\python.exe -m pytest tests\test_dominion_control_request_candidate.py tests\test_dominion_control_request_candidate_boundaries.py
.venv\Scripts\python.exe -m pytest tests\test_dominion_control_plan.py tests\test_dominion_control_plan_boundaries.py
.venv\Scripts\python.exe -m pytest tests\test_dominion_static_safety.py tests\test_dominion_static_safety_boundaries.py
.venv\Scripts\python.exe -m pytest tests\test_dominion_runtime_preflight.py tests\test_dominion_runtime_preflight_boundaries.py
.venv\Scripts\python.exe -m pytest tests\test_dominion_human_review_gate.py tests\test_dominion_human_review_gate_boundaries.py
```

Full regression suite:

```powershell
.venv\Scripts\python.exe -m pytest
```

Recorded results:

- v0.23.9 closure run: `1758 passed, 1 skipped, 3 warnings`
- latest known post-v0.24.0 full run: `1773 passed, 1 skipped, 3 warnings in 337.10s`

Different future counts are not automatically failures, but they must be
explained against source changes.

## Forbidden Search Restore Checks

Search v0.23 implementation, tests, and docs for enabled forbidden behavior:

```powershell
rg -n "external_runtime_touched=True|provider_api_call_performed=True|dispatch_performed=True|actual_dispatch_performed=True|external_run_started=True|authorization_consumed=True|live_status_tracking_started=True|live_output_fetch_started=True|real_external_outcome_recorded=True|credential_exposed=True|raw_secret_output=True|local_runtime_provider_implemented=True|general_agent_usability_implemented=True|workspace_agent_workbench_implemented=True|memory_candidate_continuity_implemented=True|external_provider_adapter_implemented=True|schumpeter_split_introduced=True|growthkernel_dependency_required=True|llm_judge" src\chanta_core\internal_dominion tests docs\versions\v0.23
```

Search vendor-specific runtime logic:

```powershell
rg -n "A360|Automation Anywhere|Brity|UiPath|Power Automate" src\chanta_core\internal_dominion tests docs\versions\v0.23
```

Expected result:

- no enabled forbidden flags in Internal Dominion implementation
- no vendor-specific runtime logic in Internal Dominion core
- `llm_judge` appears only as disabled policy, zero-count, doc, or test assertion

## Restore Procedure

1. Confirm v0.23.0 through v0.23.9 documents exist in `docs/versions/v0.23/`.
2. Confirm the original short version contracts still exist in `docs/versions/`.
3. Confirm the Internal Dominion modules listed under Source State exist.
4. Confirm the subject tests listed above exist.
5. Build or import the v0.23.9 consolidation report service.
6. Confirm the consolidation report marks v0.23.x as Internal Dominion Foundation.
7. Confirm v0.24.x is the next track and v0.25+ tracks remain deferred.
8. Run targeted subject tests.
9. Run the full regression suite when release verification is required.
10. Run forbidden searches over Internal Dominion implementation, tests, and docs.
11. Confirm CLI output is sanitized.
12. Confirm no private/company material is added.

## Known Limitations

- v0.23.x closes control grammar, not live external control.
- v0.23.x does not implement Internal Provider / Local Runtime Provider.
- v0.23.x does not implement actual bounded dispatch.
- v0.23.x does not consume authorization.
- v0.23.x does not implement General Agent Usability, Workspace Agent Workbench,
  Memory Candidate / Continuity, external provider adapters, or Schumpeter split.
- Former direct-path v0.23 short contracts have been folded into this folder;
  this folder is the restore-grade location.

## Withdrawal Conditions

Withdraw v0.23.x restore readiness if:

- any provider API call is added to Internal Dominion
- any external runtime touch is added
- any actual dispatch or external run start is added
- any authorization consumption is added
- live status tracking, live output fetch, or real external outcome recording is added
- local command execution or Local Runtime Provider implementation is added
- General Agent UX, Workspace Agent Workbench, Memory Continuity, external
  provider adapters, or Schumpeter split logic is added
- credential values, raw secrets, or private full paths are exposed
- GrowthKernel becomes an active dependency
- vendor-specific runtime logic is introduced in core
- an LLM judge is used for readiness, safety, or boundary decisions

## Validity Horizon

Valid until v0.24 Internal Provider / Local Runtime Provider changes the
provider-track contract, or until v0.23.x policy is amended.

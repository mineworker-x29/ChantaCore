# GPT Mode Vera v0.40 Handoff Read-only Audit

Date: 2026-06-13

Audience: GPT Mode Vera

Purpose: Support v0.40 design for Controlled Multi-Iteration Mission Loop + Execution-Test Ladder + Subagent Verification Boundary.

Scope note: This document summarizes a read-only audit of the current ChantaCore repository state after v0.39.9. It is not an implementation plan that grants runtime authority.

## A. Executive Summary

Confirmed facts:

1. Repository root is `D:/ChantaResearchGroup/ChantaCore`.
2. Current branch is `main`.
3. Current commit is `3347fc1e3f77ad8d445ef7437513254e80d9d721`.
4. `git status --short` shows `src/chanta_core/agent_runtime/__init__.py` modified and many v0.39 files still untracked.
5. `python --version` reports `Python 3.11.9`.
6. `py -m pytest --version` reports `pytest 9.0.3`.
7. Test logs for `py -m pytest` show Python `3.14.3`, so the direct `python` executable and `py` launcher are not identical in this environment.
8. The direct `pytest --version` command is not available on PATH.
9. v0.39.x implementation is located mainly under `src/chanta_core/agent_runtime/repair_*.py`.
10. v0.39.9 is consolidation and v0.40 design-stage handoff metadata only.

v0.40 can start now, but it should start as boundary-only work. The safe first target is `v0.40.0 Controlled Multi-Iteration Mission Loop Boundary Foundation`.

Top three risks:

1. The v0.39 worktree is not yet clean: several v0.39 files are untracked.
2. A two-iteration rehearsal could be mistaken for autonomous repair unless human checkpoint metadata is mandatory between iterations.
3. The repository has existing provider/OpenAI dependency surfaces elsewhere, so v0.40 must avoid importing top-level package paths that accidentally trigger provider imports during metadata tests.

## B. Evidence-Based Inventory

### Repository Baseline

| item | confirmed value |
|---|---|
| repository root | `D:/ChantaResearchGroup/ChantaCore` |
| branch | `main` |
| commit | `3347fc1e3f77ad8d445ef7437513254e80d9d721` |
| Python | `python --version`: `Python 3.11.9` |
| pytest runner | `py -m pytest` |
| pytest version | `py -m pytest --version`: `pytest 9.0.3` |
| direct pytest executable | not available on PATH |
| dependency config | `pyproject.toml` |
| package root | `src/chanta_core` |
| v0.39 package area | `src/chanta_core/agent_runtime` |
| tests directory | `tests` |

`pyproject.toml` declares:

- build backend: setuptools
- project name: `chanta-core`
- project version: `0.30.0`
- Python requirement: `>=3.11`
- dependencies: `openai>=2.33.0`, `python-dotenv>=1.2.2`, `pytest>=8.0.0`
- pytest addopts: `--basetemp=.pytest-tmp --ignore=references`

### v0.39.9 Artifact Inventory

| artifact | file path | class/function name | purpose | tests covering it |
|---|---|---|---|---|
| RepairLoopConsolidationFlagSet | `src/chanta_core/agent_runtime/repair_loop_consolidation.py` | `RepairLoopConsolidationFlagSet` | v0.39 bounded capability and unsafe false flags | `test_flags_allow_bounded_v039_and_design_handoff_only`, `test_flags_reject_unsafe_true` |
| RepairLoopTrackSnapshot | same | `RepairLoopTrackSnapshot` | v0.39.0-v0.39.8 snapshot | `test_snapshot_manifest_and_stage_plan_include_v0390_through_v0398` |
| RepairLoopCapabilityMatrix | same | `RepairLoopCapabilityMatrix` | bounded, preview, metadata, blocked, future capability split | `test_capability_matrix_classifies_capabilities_without_permission_grant` |
| RepairLoopStageCoverage | same | `RepairLoopStageCoverage` | per-stage coverage record | `test_stage_coverage_records_and_blocking_gap_rule` |
| RepairLoopBoundaryRegister | same | `RepairLoopBoundaryRegister` | opened and prohibited boundary register | `test_boundary_risk_and_gap_registers_capture_limits` |
| RepairLoopRiskRegister | same | `RepairLoopRiskRegister` | autonomy, prompt, subagent, certification risk register | same |
| RepairLoopGapRegister | same | `RepairLoopGapRegister` | v0.40 and later gap plan | same |
| RepairLoopReleaseManifest | same | `RepairLoopReleaseManifest` | versions, modules, docs, tests, commands manifest | `test_snapshot_manifest_and_stage_plan_include_v0390_through_v0398` |
| RepairLoopAuditTrail | same | `RepairLoopAuditTrail` | no unsafe runtime confirmations | `test_audit_trail_confirms_no_unsafe_runtime_and_pi_native_absorption` |
| RepairLoopStageConsolidationRecord | same | `RepairLoopStageConsolidationRecord` | per-v0.39 stage consolidation | `test_stage_records_exist_for_all_v039_stages` |
| LoopEngineeringPINativeConsolidationRecord | same | `LoopEngineeringPINativeConsolidationRecord` | Loop Engineering PI-native absorption | `test_loop_engineering_record_is_pi_native_absorption_only` |
| V040HandoffPacket | same | `V040HandoffPacket` | v0.40 design-stage handoff | `test_v040_handoff_packet_is_design_only` |
| V039ConsolidationReport | same | `V039ConsolidationReport` | final v0.39 report | `test_v039_consolidation_report_is_v1_ready_but_not_execution_ready` |
| RepairLoopNoUnsafeExpansionGuarantee | same | `RepairLoopNoUnsafeExpansionGuarantee` | no unsafe expansion guarantee | `test_validation_report_and_no_unsafe_expansion_guarantee` |

### Test Status

| test command | result | passed | skipped | failed | duration | notes |
|---|---:|---:|---:|---:|---:|---|
| `py -m pytest tests\test_v0399_human_approved_sandbox_repair_apply_self_prompting_loop_consolidation.py` | confirmed pass | 60 | 0 | 0 | 1.75s | focused v0.39.9 |
| `py -m pytest tests\test_v0390... tests\test_v0399...` | confirmed pass | 770 | 1 | 0 | 2.40s | v0.39.0-v0.39.9 |
| `py -m pytest tests\test_v0389... tests\test_v0399...` | confirmed pass | 797 | 1 | 0 | 2.45s | v0.38.9 + v0.39.0-v0.39.9 |
| `py -m pytest tests\test_v0393_human_approved_patch_materialization_sandbox_apply.py -rs` | confirmed pass | 86 | 1 | 0 | 1.62s | skip reason confirmed |
| full `py -m pytest` | not run | unknown | unknown | unknown | unknown | broad suite outside requested v0.39 audit |

Skip reason:

`tests/test_v0393_human_approved_patch_materialization_sandbox_apply.py:376: symlink creation is unavailable on this platform`.

### Readiness Flags

Confirmed by AST/source inspection of v0.39.3-v0.39.9 flag dataclasses.

| flag | value | owning artifacts | interpretation |
|---|---:|---|---|
| `ready_for_execution` | False | v0.39.3-v0.39.9 flag sets where present | no general execution readiness |
| `ready_for_general_execution` | False | v0.39.3-v0.39.9 flag sets where present | no broad runtime readiness |
| `ready_for_live_workspace_apply` | False | v0.39.3-v0.39.6 and v0.39.9 where present | no live apply |
| `ready_for_prompt_submission_to_model` | False | v0.39.7-v0.39.9 | no prompt submission |
| `ready_for_model_provider_invocation` | False | v0.39.3-v0.39.9 where present | no provider call |
| `ready_for_subagent_invocation` | False | v0.39.7-v0.39.9 where present | no actual subagent invocation |
| `ready_for_external_agent_execution` | False | v0.39.3-v0.39.9 where present | no external coding agent |
| `ready_for_autonomous_loop_runtime` | False | v0.39.3-v0.39.9 where present | no autonomous loop |
| `ready_for_retry_loop` | False | v0.39.3-v0.39.9 where present | no retry loop |
| `ready_for_multi_cycle_loop` | False | v0.39.3-v0.39.9 where present | no multi-cycle loop |
| `ready_for_dominion_runtime` | False | v0.39.3-v0.39.9 where present | no Dominion runtime |
| `production_certified` | False | v0.39.3-v0.39.9 where present | no production certification |

## C. Runtime Boundary Audit

### v0.39.3 Sandbox Apply Primitive

| check | result | evidence path/function | test name |
|---|---|---|---|
| sandbox-only exact text replacement executable | confirmed | `repair_sandbox_apply.py`, `apply_sandbox_text_replacements` | `test_apply_sandbox_text_replacements_changes_only_sandbox_target_file` |
| sandbox root containment enforced | confirmed | `repair_sandbox_apply.py`, `_path_flags`, `validate_sandbox_apply_target` | `test_apply_target_accepts_sandbox_contained_relative_path`, `test_apply_helper_cannot_touch_path_outside_sandbox_root` |
| path traversal blocked | confirmed | `_path_flags`: `..` and absolute path checks | `test_apply_target_rejects_unsafe_targets` |
| symlink blocked | confirmed, test skipped if platform cannot create symlink | `_path_flags`: `candidate.is_symlink()` | `test_apply_target_rejects_symlink_target` |
| binary file blocked | confirmed | `_path_flags`: binary suffix and `BINARY_FILE` target kind | `test_apply_target_rejects_unsafe_targets` |
| live workspace apply blocked | confirmed | live-like target flags and unsafe readiness false | `test_policy_allows_sandbox_only_apply_and_blocks_runtime` |
| reference corpus and secret path blocked | confirmed | `_path_flags`: reference and secret markers | `test_apply_target_rejects_unsafe_targets` |
| no git apply, apply_patch, arbitrary workspace mutation | confirmed for implementation intent | forbidden pattern test and audit fields | `test_module_does_not_contain_forbidden_runtime_invocation_patterns` |

Important nuance:

v0.39.3 does perform actual `write_text` in `apply_sandbox_text_replacements`, but only after sandbox target validation. This is the bounded sandbox apply primitive, not live apply.

### v0.39.4 Controlled Retest Primitive

| check | result | evidence path/function | test name |
|---|---|---|---|
| controlled runner boundary location | confirmed | `repair_post_apply_retest.py`, `run_post_apply_controlled_retest` | `test_run_post_apply_controlled_retest_uses_fake_runner_only_when_gates_pass` |
| shell=False semantics | confirmed | `RepairControlledTestCommandSpec.__post_init__`, `RepairControlledTestRunnerInvocation.__post_init__` | `test_command_spec_is_shell_free_and_runner_bound` |
| bounded argv | confirmed | `RepairPostApplyRetestPolicy.max_argv_items`, `RepairControlledTestCommandSpec.argv` | `test_retest_input_is_controlled_request_not_arbitrary_command` |
| sandbox cwd | confirmed as `cwd_ref` metadata and policy requirement | `RepairPostApplyRetestPolicy.require_sandbox_cwd` | `test_policy_allows_controlled_boundary_and_blocks_runtime` |
| timeout | confirmed | `timeout_seconds > 0`; runner receives timeout | `test_command_spec_is_shell_free_and_runner_bound` |
| bounded and redacted output capture | confirmed | `capture_repair_post_apply_test_output` | `test_output_capture_bounds_and_redacts` |
| arbitrary shell/subprocess not opened | confirmed | no subprocess import/call; supplied runner callable only | `test_invocation_rejects_raw_subprocess_marker` |
| dependency install/network blocked | confirmed | install/network command flags rejected | `test_command_spec_rejects_unsafe_shape`, `test_audit_confirms_no_unsafe_surfaces` |

Important nuance:

`controlled_test_subprocess_allowed_now` may be true in v0.39.4 language only as controlled runner boundary metadata. It is not raw subprocess permission.

### v0.39.5-v0.39.6 Comparison / Process State

| item | current behavior | evidence | test coverage |
|---|---|---|---|
| Before/After Outcome Comparison | metadata comparison and assessment | `repair_outcome_comparison.py`, `RepairOutcomeComparisonReport`, `assess_repair_effectiveness` | `test_audit_decision_report_and_readiness_block_runtime` |
| effectiveness is not correctness proof | confirmed | `correctness_proven=False`; helper `repair_effectiveness_assessment_is_not_correctness_proof` | `test_effectiveness_assessment_variants_are_not_correctness_proof` |
| failing after-test does not grant automatic repair | confirmed | report fields `repair_executed_by_v0395=False`, rollback false | `test_audit_decision_report_and_readiness_block_runtime` |
| PI-native process-state reconstruction | metadata graph/report | `repair_process_state_reconstruction.py`, `RepairProcessStateReconstructionReport` | `test_reconstruction_helpers_create_metadata_graph` |
| OCEL-style envelope not file write | confirmed | `RepairOCELStyleEventEnvelope`, `repair_ocel_event_envelope_is_not_persisted` | `test_event_envelope_is_not_persisted` |
| OCPX projection not persistence | confirmed | `RepairOCPXStateProjection`, `repair_ocpx_state_projection_is_not_persisted` | `test_ocpx_projection_is_not_persisted_or_authority` |
| PIG diagnostic input not recommendation execution | confirmed | `RepairPIGDiagnosticInputContext`, `repair_pig_input_context_is_not_recommendation_execution` | `test_transition_mission_and_pig_context_block_runtime` |

### v0.39.7 Self-Prompt / Subagent Draft Boundary

| check | result |
|---|---|
| SelfPromptDraft implementation | `repair_self_prompting.py`, `RepairSelfPromptDraft` |
| NextActionDraft implementation | `repair_self_prompting.py`, `RepairNextActionDraft` |
| Agent-to-Subagent Prompt Draft implementation | `repair_self_prompting.py`, `RepairAgentToSubagentPromptDraft` |
| SubagentVerificationRequestDraft implementation | `repair_self_prompting.py`, `RepairSubagentVerificationRequestDraft` |
| prompt draft not submission | confirmed: `submitted_to_model=False`, `executed=False` |
| subagent draft not invocation | confirmed: `subagent_invoked=False`, `external_agent_invoked=False`, `model_invoked=False` |
| model/provider calls absent | confirmed in v0.39.7 implementation scan |
| autonomous continuation absent | confirmed: `autonomous_loop_continued=False`, `retry_loop_started=False` |

Requested keyword scan classification:

- `prompt_submission`, `model_provider_invocation`, `subagent_invocation`, `autonomous_loop`, `retry_loop`: legitimate metadata naming and false flags.
- `submit_prompt`, `invoke_model`, `call_model`, `openai`, `anthropic`, `ollama`, `lmstudio`, `invoke_subagent`: no runtime call found in v0.39.7 implementation.

### v0.39.8 CLI Preview-only Boundary

| CLI surface | file/function | preview-only evidence | blocked runtime actions | tests |
|---|---|---|---|---|
| argv parsing | `repair_loop_state_cli_surface.py`, `parse_repair_cli_loop_invocation` | `shell_used=False`, `subprocess_used=False` | shell, subprocess, arbitrary command | `test_input_invocation_and_parser_are_metadata_only` |
| command classification | `classify_repair_cli_loop_command` | unsafe commands map to denied kinds | apply, retest, prompt, model, subagent, export, send | `test_parser_maps_unsafe_commands_to_denied` |
| decision | `decide_repair_cli_loop_surface` | preview allowed only for safe preview commands | all runtime/action/export flags false | `test_decision_allows_preview_only_and_denies_unsafe_commands` |
| denied command metadata | `RepairCLIDeniedLoopCommand` | safe alternatives only | no remediation execution | `test_denied_command_rendered_views_bundle_and_handoff_are_in_memory_only` |
| rendered views | `render_repair_cli_loop_view` | bounded/redacted, no file write/send | file export, external send | same |
| loop bundle | `RepairCLILoopBundleView`, `create_repair_cli_loop_bundle_view` | in-memory summary | no apply/retest execution | same |
| handoff packet | `RepairCLILoopHandoffPacket`, `create_repair_cli_loop_handoff_packet` | `human_action_required=True`, `auto_continue_allowed=False` | no approval capture, no external send | same |
| readiness report | `V0398ReadinessReport` | preview-only readiness | CLI runtime/apply/retest/model/subagent false | `test_result_report_and_readiness_preserve_preview_only_boundary` |

### Forbidden Runtime Call Scan

Scope scanned: v0.39.3-v0.39.9 implementation modules.

| keyword | occurrence count | legitimate metadata/test only | actual runtime risk | evidence paths | comment |
|---|---:|---|---|---|---|
| `subprocess` | 121 | yes | not found | v0.39.3-v0.39.9 modules | denied/flag naming; supplied runner only |
| `shell=True` | 0 | n/a | no | none | no occurrence |
| `os.system` | 0 | n/a | no | none | no occurrence |
| `eval(` | 0 | n/a | no | none | no occurrence |
| `exec(` | 0 | n/a | no | none | no occurrence |
| `requests` | 0 | n/a | no | none | no occurrence |
| `httpx` | 0 | n/a | no | none | no occurrence |
| `urllib` | 0 | n/a | no | none | no occurrence |
| `socket` | 0 | n/a | no | none | no occurrence |
| `openai` | 0 in v0.39 modules | n/a | no in v0.39 modules | none | dependency exists in `pyproject.toml` |
| `anthropic` | 0 | n/a | no | none | no occurrence |
| `ollama` | 0 | n/a | no | none | no occurrence |
| `lmstudio` | 0 | n/a | no | none | no occurrence |
| `codex` | 16 | yes | not found | v0.39 modules | readiness/denied invocation naming |
| `claude` | 16 | yes | not found | v0.39 modules | readiness/denied invocation naming |
| `apply_patch` | 58 | yes | not found | v0.39 modules | denied/confusion/no-apply metadata |
| `git apply` | 0 | n/a | no | none | no occurrence |
| `git worktree` | 0 | n/a | no | none | no occurrence |
| `file export` | 0 | n/a | no | none | exact phrase absent; export false flags exist |
| `external send` | 0 | n/a | no | none | exact phrase absent; send false flags exist |
| `network` | 71 | yes | not found | v0.39 modules | denied/no-network metadata |
| `credential` | 17 | yes | not found | v0.39 modules | secret/credential path blocking metadata |
| `secret` | 41 | yes | not found | v0.39 modules | secret path blocking/redaction risk metadata |
| `token` | 8 | yes | not found | v0.39.3, v0.39.7, v0.39.9 | token budget/path fragment metadata |

## D. v0.40 Feasibility

### Recommended Owner Modules

| proposed artifact | recommended path | reason | existing owner to respect | tests to add |
|---|---|---|---|---|
| MissionLoopEnvelope | `src/chanta_core/agent_runtime/repair_mission_loop_boundary.py` | v0.40 should start as boundary metadata | v0.39.9 handoff, v0.39.7 loop context | `test_v0400_controlled_multi_iteration_mission_loop_boundary.py` |
| IterationState | same | core loop state belongs with envelope | v0.39.6 process state | same |
| LoopBudgetGate | same, or `repair_mission_loop_budget.py` if it grows | budget gate is first-class safety boundary | v0.39.9 gap register | budget negative tests |
| StopConditionContract | same | max-iteration and stop semantics are central | v0.39.9 v0.40 handoff | stop condition tests |
| HumanCheckpointGate | same | mandatory human gate between iterations | v0.39.7 human handoff | checkpoint required tests |
| LoopDecisionRecord | same | decision metadata, not execution | v0.39.7 next-action decision | decision no-execution tests |
| DeniedRuntimeActionMetadata | same | cross-cutting denied runtime ledger | v0.39.8 denied command | denied unsafe action tests |
| ProviderBoundaryGate | same in v0.40.0 as metadata only; split later if needed | do not open invocation yet | existing model boundary modules exist | provider no-call tests |
| PromptSubmissionBoundary | same initially | prompt submission gate must be explicit | v0.39.7 draft contract | prompt no-submission tests |
| VerifierSubagentBoundary | same initially; split later if needed | separate subagent gate may grow | v0.39.7 verification request draft | subagent no-invocation tests |
| SubagentVerificationRequestDraft | reuse `repair_self_prompting.py` | already implemented | v0.39.7 | integration/reference tests |
| SimulatedMultiIterationLoopPacket | `repair_mission_loop_boundary.py` | dry-run packet, not runtime loop | v0.39.9 handoff | dry-run simulation tests |
| SandboxRehearsalRunner | `repair_mission_loop_rehearsal.py` in v0.40.1+ | touches v0.39.3/v0.39.4 primitives | v0.39.3/v0.39.4 | sandbox rehearsal tests |
| ManualTwoIterationRehearsal | `repair_mission_loop_rehearsal.py` | should be explicitly manual | human checkpoint gate | manual checkpoint tests |
| V040ReadinessReport | `repair_mission_loop_boundary.py` | release readiness artifact | v0.39.9 readiness style | readiness false-runtime tests |

### Execution-Test Ladder Feasibility

| level | feasible now? | required existing primitives | missing pieces | recommended first implementation | risk |
|---|---|---|---|---|---|
| Level 0 Static Boundary Test | yes | v0.39 negative flag/policy tests | v0.40-specific artifact names | v0.40.0 | low |
| Level 1 Dry-Run Loop Simulation | yes, boundary-only | v0.39.7 draft packet, v0.39.9 handoff | MissionLoopEnvelope, IterationState, StopConditionContract | v0.40.0 main scope | medium |
| Level 2 Sandbox Rehearsal | conditionally yes | v0.39.3 sandbox apply, v0.39.4 controlled retest, pytest tmp fixtures | rehearsal runner contract, human checkpoint | v0.40.1 or tightly bounded late v0.40.0 | medium-high |
| Level 3 Manual Two-Iteration Rehearsal | conditionally yes | v0.39.3/v0.39.4 plus human handoff metadata | explicit manual checkpoint and two-iteration cap | v0.40.1 after Level 1 passes | high |
| Level 4 Negative Execution Test | yes | existing negative tests for flags/calls | v0.40 forbidden pattern suite | v0.40.0 | low-medium |

Level 2 and Level 3 notes:

- v0.39.3 sandbox apply primitive can be reused.
- v0.39.4 controlled retest primitive can be reused through supplied runner callable.
- temp sandbox workspace fixtures can be created with pytest `tmp_path`.
- two-iteration rehearsal must be named manual/dry-run/rehearsal, not autonomous loop.
- human checkpoint metadata must be required between iteration 0 and iteration 1.

## E. Recommended v0.40.0 First Sprint

### Implementation Scope

Boundary-only first sprint:

- `MissionLoopEnvelope`
- `IterationState`
- `LoopBudgetGate`
- `StopConditionContract`
- `HumanCheckpointGate`
- `LoopDecisionRecord`
- `DeniedRuntimeActionMetadata`
- `ProviderBoundaryGate` as metadata only
- `PromptSubmissionBoundary` as metadata only
- `VerifierSubagentBoundary` as metadata only
- `SimulatedMultiIterationLoopPacket`
- `V040ReadinessReport`

Do not include actual model invocation, prompt submission, actual subagent invocation, or autonomous runtime in v0.40.0.

### Files To Add

- `src/chanta_core/agent_runtime/repair_mission_loop_boundary.py`
- `tests/test_v0400_controlled_multi_iteration_mission_loop_boundary.py`
- `docs/versions/v0.40/v0.40.0_controlled_multi_iteration_mission_loop_boundary_foundation.md`

### Files To Modify

- `src/chanta_core/agent_runtime/__init__.py`
- possibly `docs/versions/README.md` if version index convention requires it. This was not verified in this audit.

### Tests To Add

- enum coverage
- flag creation and unsafe false flags
- max-iteration policy tests
- stop-condition contract tests
- budget gate tests
- human checkpoint required tests
- provider boundary no invocation tests
- prompt submission boundary no submission tests
- verifier subagent boundary no invocation tests
- simulated multi-iteration packet does not execute tests
- readiness report no production/no execution tests
- forbidden call scan test

### Tests To Run

- focused v0.40.0 test
- v0.39.9 focused test
- v0.39.0-v0.40.0 aggregate once v0.40.0 exists
- v0.38.9 + v0.39.x + v0.40.0 aggregate if practical

### Hard Prohibitions

Do not open:

- model/provider invocation
- prompt submission
- actual subagent invocation
- external coding agent invocation
- autonomous loop runtime
- retry loop
- multi-cycle automatic repair
- live workspace apply
- shell/subprocess/arbitrary command
- dependency install/network
- trace persistence
- OCEL/OCPX write
- Dominion runtime
- production certification

### Acceptance Criteria

- v0.40.0 creates controlled multi-iteration boundary metadata.
- max iteration defaults to a safe small bound, preferably `1` or `2` for simulation.
- stop condition is mandatory.
- human checkpoint is mandatory before any second iteration.
- provider/subagent/prompt gates exist but do not invoke.
- all unsafe readiness flags remain false.
- focused and aggregate tests pass.

## F. Withdrawal Conditions

Stop or withdraw v0.40 work if any of these appears:

- `ready_for_execution=True`
- model/provider call is introduced
- prompt submission is introduced
- subagent invocation is introduced
- auto-continue without human checkpoint is allowed
- retry/multi-cycle loop starts without explicit cap and stop condition
- sandbox rehearsal mutates outside temp sandbox
- v0.39.3 sandbox apply is reused against live workspace
- v0.39.4 runner is replaced with raw subprocess or shell
- production certification is claimed
- Dominion runtime authority is introduced

## G. Final Judgment

Based on current repository evidence, v0.40 should start as boundary-only work.

Dry-run loop simulation can be included in v0.40.0.

Sandbox rehearsal is feasible because v0.39.3 sandbox apply and v0.39.4 controlled retest primitives exist, but it should be delayed to v0.40.1 or added only if tightly bounded.

Manual two-iteration rehearsal can be part of v0.40, but it must force human checkpoint metadata between iterations and must never be framed as autonomous repair.

Confirmed basis:

- v0.39.9 focused and aggregate tests pass.
- v0.39.3 sandbox apply primitive is implemented and tested.
- v0.39.4 controlled retest uses a supplied runner callable and tested shell/no-subprocess constraints.
- v0.39.7 self-prompt/subagent artifacts are draft-only.
- v0.39.8 CLI surface is preview-only.
- v0.39.9 consolidation keeps unsafe readiness false.

Withdrawal basis:

This judgment should be withdrawn if actual runtime calls, unsafe readiness true values, live apply, model/subagent invocation, or autonomous continuation are found in the v0.40 implementation path.

Validity:

This audit is valid for the ChantaCore workspace state inspected on 2026-06-13.

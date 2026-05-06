# ChantaCore v0.10.0 to v0.11.2 Audit Report

Audit date: 2026-05-06

Repository: `D:\ChantaResearchGroup\ChantaCore`

Audited range:

- v0.10.0 OCEL-native session/message/turn substrate
- v0.10.1 OCEL-native memory and instruction substrate
- v0.10.2 Markdown materialized views, non-canonical
- v0.10.3 hook lifecycle observability, observational only
- v0.10.4 session resume/fork, permissions not restored
- v0.10.5 tool registry and tool policy views, non-enforcing
- v0.11.0 verification contract foundation
- v0.11.1 read-only verification skills
- v0.11.2 process outcome evaluation

## Audit Basis

This report is based on local file inspection, grep checks, pytest execution, smoke script execution, and git hygiene checks performed in the repository above.

The conclusion should be withdrawn if any of the following changes:

- source files are modified after this audit;
- the listed tests fail under the same environment;
- a stricter grep finds forbidden behavior in the audited packages;
- generated data, SQLite DBs, or environment files become tracked;
- a reviewer finds runtime behavior not covered by the current tests.

## Version / Package Inventory

| Version | Expected area | Observed files / packages | Status |
| --- | --- | --- | --- |
| v0.10.0 | session/message/turn | `src/chanta_core/session/models.py`, `service.py`, `history_adapter.py`, `ids.py`, `errors.py` | Present |
| v0.10.1 | memory/instruction | `src/chanta_core/memory/*`, `src/chanta_core/instructions/*` | Present |
| v0.10.2 | materialized views | `src/chanta_core/materialized_views/*` | Present |
| v0.10.3 | hooks | `src/chanta_core/hooks/*` | Present |
| v0.10.4 | session continuity | `src/chanta_core/session/continuity.py`, `snapshots.py` | Present |
| v0.10.5 | tool registry views | `src/chanta_core/tool_registry/*` | Present |
| v0.11.0 | verification contracts | `src/chanta_core/verification/errors.py`, `ids.py`, `models.py`, `service.py`, `history_adapter.py` | Present |
| v0.11.1 | read-only verification skills | `src/chanta_core/verification/read_only_skills.py` | Present |
| v0.11.2 | process outcomes | `src/chanta_core/outcomes/errors.py`, `ids.py`, `models.py`, `service.py`, `history_adapter.py` | Present |

Restore docs exist for all audited versions:

- `docs/chanta_core_v0_10_0_restore.md`
- `docs/chanta_core_v0_10_1_restore.md`
- `docs/chanta_core_v0_10_2_restore.md`
- `docs/chanta_core_v0_10_3_restore.md`
- `docs/chanta_core_v0_10_4_restore.md`
- `docs/chanta_core_v0_10_5_restore.md`
- `docs/chanta_core_v0_11_0_restore.md`
- `docs/chanta_core_v0_11_1_restore.md`
- `docs/chanta_core_v0_11_2_restore.md`

Current version files:

- `pyproject.toml`: `version = "0.11.2"`
- `src/chanta_core/__init__.py`: `__version__ = "0.11.2"`

No `note.md` exists.

## Model / Service / Adapter / Test Coverage

### v0.10.0 Session Substrate

Observed:

- Session models and service are present.
- Session history adapter is present.
- Session OCEL shape and service tests are present.
- Session events participate in OCEL traces.

Relevant tests in acceptance suite passed:

- `tests/test_session_models.py`
- `tests/test_session_service.py`
- `tests/test_session_context_history_adapter.py`
- `tests/test_session_ocel_shape.py`
- `tests/test_agent_runtime_session_integration.py`

### v0.10.1 Memory / Instruction Substrate

Observed:

- Memory models/service/history adapter are present.
- Instruction models/service/history adapter are present.
- OCEL shape test for memory/instruction is present.

Relevant tests in acceptance suite passed:

- `tests/test_memory_models.py`
- `tests/test_instruction_models.py`
- `tests/test_memory_service.py`
- `tests/test_instruction_service.py`
- `tests/test_memory_context_history_adapter.py`
- `tests/test_instruction_context_history_adapter.py`
- `tests/test_memory_instruction_ocel_shape.py`

### v0.10.2 Materialized Views

Observed:

- Materialized view models, renderers, Markdown helper, paths, and service are present.
- Renderers set `canonical=False`.
- Markdown warnings state non-canonical status and OCEL as source.

Relevant tests in acceptance suite passed:

- `tests/test_materialized_view_models.py`
- `tests/test_materialized_view_renderers.py`
- `tests/test_materialized_view_service.py`
- `tests/test_materialized_view_ocel_shape.py`
- `tests/test_materialized_view_boundaries.py`

### v0.10.3 Hooks

Observed:

- Hook models, registry, lifecycle helper, and service are present.
- Hook service records `enforcement_enabled=False`.
- Grep found enforcement vocabulary only in boundary/metadata contexts, not active enforcement.

Relevant tests in acceptance suite passed:

- `tests/test_hook_models.py`
- `tests/test_hook_registry.py`
- `tests/test_hook_lifecycle_service.py`
- `tests/test_hook_ocel_shape.py`
- `tests/test_hook_boundaries.py`

### v0.10.4 Session Resume / Fork

Observed:

- `src/chanta_core/session/continuity.py` is present.
- Resume/fork record permission reset.
- Grep found `permissions_restored: False`.
- Tests assert no `restore_permissions`.

Relevant tests in acceptance suite passed:

- `tests/test_session_continuity_models.py`
- `tests/test_session_continuity_service.py`
- `tests/test_session_continuity_history_adapter.py`
- `tests/test_session_resume_fork_ocel_shape.py`
- `tests/test_session_resume_fork_boundaries.py`

### v0.10.5 Tool Registry Views

Observed:

- Tool descriptor, policy note, snapshot, risk annotation models are present.
- Tool registry service and renderers are present.
- Tool views are Markdown materialized views with `canonical=False`.
- Tool policy renderer states it is not `PermissionPolicy` and does not grant, deny, allow, ask, block, or sandbox tool usage.
- Grep found `enforcement_enabled=False` in service metadata.

Relevant tests in acceptance suite passed:

- `tests/test_tool_registry_models.py`
- `tests/test_tool_registry_service.py`
- `tests/test_tool_registry_renderers.py`
- `tests/test_tool_registry_view_files.py`
- `tests/test_tool_registry_ocel_shape.py`
- `tests/test_tool_registry_boundaries.py`

### v0.11.0 Verification Contract Foundation

Observed:

- `VerificationContract`, `VerificationTarget`, `VerificationRequirement`, `VerificationRun`, `VerificationEvidence`, and `VerificationResult` are implemented.
- `VerificationService` is implemented.
- `verification_results_to_history_entries` is implemented.
- Verification OCEL object types and events are tested.
- `passed` / `failed` verification results require evidence IDs.
- No canonical JSONL verification store was found.

Relevant tests in acceptance suite passed:

- `tests/test_verification_models.py`
- `tests/test_verification_service.py`
- `tests/test_verification_history_adapter.py`
- `tests/test_verification_ocel_shape.py`
- `tests/test_verification_boundaries.py`

### v0.11.1 Read-only Verification Skills

Observed:

- `ReadOnlyVerificationSkillSpec`, `ReadOnlyVerificationSkillOutcome`, and `ReadOnlyVerificationSkillService` are implemented.
- Required skills are implemented:
  - `verify_file_exists`
  - `verify_path_type`
  - `verify_tool_available`
  - `verify_runtime_python_info`
  - `verify_ocel_object_type_exists`
  - `verify_ocel_event_activity_exists`
  - `verify_materialized_view_warning`
  - `verify_tool_registry_view_warning`
- Skills create VerificationTarget, VerificationRun, VerificationEvidence, and VerificationResult.
- Allowed read-only operations were found:
  - `Path.exists()`
  - `Path.is_file()`
  - `Path.is_dir()`
  - `Path.read_text()`
  - `shutil.which()`
- No shell or network execution was found in verification code.
- Read-only file inspection exists only in `read_only_skills.py`.

Relevant tests in acceptance suite passed:

- `tests/test_read_only_verification_skill_models.py`
- `tests/test_read_only_verification_skills.py`
- `tests/test_read_only_verification_ocel_flow.py`
- `tests/test_read_only_verification_boundaries.py`

### v0.11.2 Process Outcome Evaluation

Observed:

- `ProcessOutcomeContract`, `ProcessOutcomeCriterion`, `ProcessOutcomeTarget`, `ProcessOutcomeSignal`, and `ProcessOutcomeEvaluation` are implemented.
- `ProcessOutcomeEvaluationService` is implemented.
- `process_outcome_evaluations_to_history_entries` is implemented.
- Outcome evaluation consumes a provided `VerificationResult` list.
- Outcome evaluation computes:
  - total verification count;
  - passed count;
  - failed count;
  - inconclusive count;
  - skipped count;
  - error count;
  - pass rate;
  - evidence coverage;
  - score;
  - confidence.
- Outcome status policy is deterministic and documented in `docs/chanta_core_v0_11_2_restore.md`.
- `success`, `partial_success`, and `failed` evaluations require signal IDs or verification result IDs.
- Score, confidence, and evidence coverage range validation exists.
- No permission enforcement, tool blocking/mutation, shell/network execution, LLM judge, retry/replan, memory promotion, or policy update was found in `src/chanta_core/outcomes`.

Relevant tests in acceptance suite passed:

- `tests/test_process_outcome_models.py`
- `tests/test_process_outcome_service.py`
- `tests/test_process_outcome_history_adapter.py`
- `tests/test_process_outcome_ocel_shape.py`
- `tests/test_process_outcome_boundaries.py`

## OCEL Object / Event / Relation Check

The following OCEL shape tests passed:

- Session OCEL shape
- Memory/instruction OCEL shape
- Materialized view OCEL shape
- Hook OCEL shape
- Session resume/fork OCEL shape
- Tool registry OCEL shape
- Verification OCEL shape
- Read-only verification OCEL flow
- Process outcome OCEL shape

Observed object types for v0.11.x:

- `verification_contract`
- `verification_target`
- `verification_requirement`
- `verification_run`
- `verification_evidence`
- `verification_result`
- `process_outcome_contract`
- `process_outcome_criterion`
- `process_outcome_target`
- `process_outcome_signal`
- `process_outcome_evaluation`

Observed event activities for v0.11.x include:

- `verification_contract_registered`
- `verification_target_registered`
- `verification_requirement_registered`
- `verification_run_started`
- `verification_evidence_recorded`
- `verification_result_recorded`
- `process_outcome_contract_registered`
- `process_outcome_criterion_registered`
- `process_outcome_target_registered`
- `process_outcome_signal_recorded`
- `process_outcome_evaluation_started`
- `process_outcome_evaluation_recorded`

Relation intent is represented through existing OCEL event-object and object-object relation helpers where the service APIs allow it.

## Strong Boundary Checks

### JSONL / Markdown Canonicality

Observed facts:

- v0.10.2 materialized views set `canonical=False`.
- v0.10.5 tool registry views set `canonical=False`.
- v0.11.0 / v0.11.1 docs state no canonical JSONL verification store.
- v0.11.2 docs state no canonical JSONL outcome store.
- Generated Markdown warnings state OCEL as canonical source and Markdown as non-canonical.

Judgment:

- No evidence was found that Markdown is treated as canonical for the audited v0.10.2/v0.10.5/v0.11.x features.
- No evidence was found that verification or outcome persistence uses JSONL as canonical storage.

Important nuance:

- Existing runtime subsystems outside the v0.11 verification/outcome scope still contain JSONL stores, for example worker/job/scheduler/editing data. This audit did not classify those as verification/outcome canonical stores. A separate architectural audit would be needed if the global rule is intended to eliminate all JSONL-backed runtime state across every subsystem.

### Hook Enforcement

Observed facts:

- `src/chanta_core/hooks/service.py` records `enforcement_enabled=False`.
- Hook boundary tests passed.
- Grep found hook policy words such as `deny` / `block` in model vocabularies and tests, not as active enforcement.

Judgment:

- No evidence was found that hooks started enforcing runtime behavior.

### Tool Policy View Acting as Permission Policy

Observed facts:

- Tool policy renderer states it is not `PermissionPolicy`.
- Renderer states it does not grant, deny, allow, ask, block, or sandbox tool usage.
- Tool registry service records `enforcement_enabled=False`.
- Tool registry boundary tests passed.

Judgment:

- No evidence was found that tool policy views act as permission policy.

### Resume / Fork Permission Restoration

Observed facts:

- `src/chanta_core/session/continuity.py` records permission reset.
- Grep found `permissions_restored: False`.
- Boundary test asserts `restore_permissions` is absent.

Judgment:

- No evidence was found that resume/fork restores permissions.

### Verification Shell / Network / Write Behavior

Observed facts:

- Core verification service does not perform shell/network/file checks.
- v0.11.1 read-only skills use allowed read-only observation:
  - `exists()`
  - `is_file()`
  - `is_dir()`
  - `read_text()`
  - `shutil.which()`
- Verification boundary tests passed.

Judgment:

- No evidence was found that verification performs shell or network execution.
- File reads in read-only verification skills are intentional v0.11.1 behavior.

### Outcome Retry / Replan / Memory Promotion / Policy Update

Observed facts:

- `src/chanta_core/outcomes` boundary test passed.
- No forbidden tokens were found in outcomes package:
  - `subprocess`
  - `os.system`
  - `requests`
  - `httpx`
  - `socket`
  - `complete_text`
  - `complete_json`
  - `llm`
  - `PermissionGrant`
  - `sandbox`
  - `block_tool`
  - `retry`
  - `replan`
  - `promote_memory`
  - `policy_update`
  - `embedding`
  - `vector`
  - `load_mcp`
  - `load_plugin`

Judgment:

- No evidence was found that outcome evaluation performs retry, replan, memory promotion, or policy update.

## PIG / OCPX Report Support

Observed:

- `src/chanta_core/pig/reports.py` includes verification summary and read-only verification skill summary.
- `src/chanta_core/pig/reports.py` includes process outcome summary:
  - outcome object counts;
  - status counts;
  - by-contract-type counts;
  - by-target-type counts;
  - average evidence coverage;
  - average outcome score.
- `src/chanta_core/pig/inspector.py` exposes verification and process outcome summaries.

Relevant test passed:

- `tests/test_pig_reports.py`

## Test Execution

### Editable Install

Command:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

Result:

- First sandboxed run failed because build dependency access to `setuptools>=68` was blocked by sandbox/network policy.
- Re-run with approved escalation succeeded.
- Installed package version: `chanta-core==0.11.2`.

### Acceptance Suite

Command:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_imports.py tests\test_process_outcome_models.py tests\test_process_outcome_service.py tests\test_process_outcome_history_adapter.py tests\test_process_outcome_ocel_shape.py tests\test_process_outcome_boundaries.py tests\test_read_only_verification_skill_models.py tests\test_read_only_verification_skills.py tests\test_read_only_verification_ocel_flow.py tests\test_read_only_verification_boundaries.py tests\test_verification_models.py tests\test_verification_service.py tests\test_verification_history_adapter.py tests\test_verification_ocel_shape.py tests\test_verification_boundaries.py tests\test_tool_registry_models.py tests\test_tool_registry_service.py tests\test_tool_registry_renderers.py tests\test_tool_registry_view_files.py tests\test_tool_registry_ocel_shape.py tests\test_tool_registry_boundaries.py tests\test_session_continuity_models.py tests\test_session_continuity_service.py tests\test_session_continuity_history_adapter.py tests\test_session_resume_fork_ocel_shape.py tests\test_session_resume_fork_boundaries.py tests\test_hook_models.py tests\test_hook_registry.py tests\test_hook_lifecycle_service.py tests\test_hook_ocel_shape.py tests\test_hook_boundaries.py tests\test_materialized_view_models.py tests\test_materialized_view_renderers.py tests\test_materialized_view_service.py tests\test_materialized_view_ocel_shape.py tests\test_materialized_view_boundaries.py tests\test_memory_models.py tests\test_instruction_models.py tests\test_memory_service.py tests\test_instruction_service.py tests\test_memory_context_history_adapter.py tests\test_instruction_context_history_adapter.py tests\test_memory_instruction_ocel_shape.py tests\test_session_models.py tests\test_session_service.py tests\test_agent_runtime_session_integration.py tests\test_session_context_history_adapter.py tests\test_session_ocel_shape.py tests\test_process_run_loop.py tests\test_ocel_store.py tests\test_context_history.py tests\test_pig_reports.py
```

Result:

- `115 passed`

### Full Repository Pytest

Command:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Result:

- Collection failed outside normal `tests/` package because reference scripts were collected:
  - `references/ChantaPermaMemory/scripts/test_gpt_oss_transformers.py` failed: missing `transformers`.
  - `references/ChantaPermaMemory/scripts/test_nemotron_transformers.py` failed: missing `torch`.

Judgment:

- This is an environmental/reference collection issue, not evidence of v0.10.0 to v0.11.2 implementation failure.
- A pytest configuration may be needed if repository-wide pytest should exclude `references/`.

### Full `tests/` Directory Pytest

Command:

```powershell
.\.venv\Scripts\python.exe -m pytest tests
```

Result:

- `490 passed`
- `1 skipped`
- `2 failed`
- `3 warnings`

Failures:

1. `tests/test_process_instance_runtime.py::test_process_instance_runtime_shape`

   The test expects only process runtime activities from `fetch_events_by_session(...)`.
   Actual result includes v0.10.0 session/message/turn events:

   - `session_started`
   - `conversation_turn_started`
   - `process_instance_attached_to_turn`
   - `user_message_received`
   - `message_attached_to_turn`
   - process runtime events
   - `assistant_message_emitted`
   - `message_attached_to_turn`
   - `conversation_turn_completed`

   Judgment:

   - The failure appears to be a stale test expectation against the current session-integrated runtime trace shape.
   - It is not direct evidence of v0.11.0/v0.11.1/v0.11.2 boundary violation.

2. `tests/test_worker_skill.py::test_run_worker_once_skill_returns_result`

   Expected:

   - `result.output_attrs["run_once"]["status"] == "idle"`

   Actual:

   - `failed`

   Observed cause:

   - The skill uses the default worker runner/tool path.
   - The worker store defaults to `data/workers/process_jobs.jsonl` / state JSON.
   - The local ignored `data/` directory contains worker runtime data.

   Judgment:

   - The failure is likely environment/data-state dependent.
   - It is not direct evidence of v0.11.0/v0.11.1/v0.11.2 boundary violation.
   - The test should probably isolate worker storage with a temp store or clear fixture.

Warnings:

- Invalid JSONL row warnings in existing edit/job/schedule store tests.
- These tests intentionally verify invalid JSONL row handling.

## Smoke Scripts

Executed:

```powershell
.\.venv\Scripts\python.exe scripts\test_verification_contracts.py
.\.venv\Scripts\python.exe scripts\test_read_only_verification_skills.py
.\.venv\Scripts\python.exe scripts\test_process_outcome_evaluation.py
.\.venv\Scripts\python.exe scripts\test_llm_client.py
```

Results:

- `scripts/test_verification_contracts.py`: passed; printed contract/target/run/evidence/result IDs.
- `scripts/test_read_only_verification_skills.py`: passed; one `verify_tool_available("python")` result was `failed` because this environment did not expose `python` through the checked PATH, but the script exited successfully and this is valid read-only observation.
- `scripts/test_process_outcome_evaluation.py`: passed; printed `outcome_status=success`, `score=1.0`, `confidence=0.9`, `evidence_coverage=1.0`.
- `scripts/test_llm_client.py`: passed with no failure output in the latest run.

## Git Hygiene

Command results:

```powershell
git status --short
```

Current worktree includes expected modified/untracked implementation files:

- modified:
  - `pyproject.toml`
  - `src/chanta_core/__init__.py`
  - `src/chanta_core/pig/inspector.py`
  - `src/chanta_core/pig/reports.py`
  - `tests/test_imports.py`
  - `tests/test_pig_reports.py`
- untracked:
  - v0.11.0 restore doc, script, verification package/tests
  - v0.11.1 restore doc, script, read-only verification tests
  - v0.11.2 restore doc, script, outcomes package/tests
  - this audit report

Ignored generated files:

```powershell
git status --ignored --short data .pytest-tmp
```

Result:

- `!! .pytest-tmp/`
- `!! data/`

Tracked generated data checks:

```powershell
git ls-files | findstr "data"
```

Result:

- no output

```powershell
git ls-files | findstr ".sqlite"
```

Result:

- `tests/test_ocel_export_sqlite.py`

This is a test filename, not a tracked SQLite database.

```powershell
git ls-files | findstr /R "\.sqlite$ \.sqlite3$"
```

Result:

- no output

```powershell
git ls-files | findstr ".env"
```

Result:

- `.env.example`

Judgment:

- Generated runtime data and SQLite DB files are not tracked.
- `.env.example` is tracked as expected.
- `.pytest-tmp/` and `data/` are ignored.

## Potential Issues / Design Notes

### 1. Full repository pytest collects reference scripts

`pytest` without a test path collects `references/ChantaPermaMemory/scripts/test_*.py`.
Those scripts require optional ML packages not installed in this environment.

Severity: Low for ChantaCore v0.10.0 to v0.11.2 implementation; Medium for developer ergonomics.

Suggested fix:

- Configure pytest discovery to focus on `tests/`, or mark reference scripts as non-pytest scripts.

### 2. `tests/test_process_instance_runtime.py` expectation is stale

The current runtime emits session/message/turn OCEL events along with process runtime events.
The test expects only process runtime events from a session query.

Severity: Medium for full test hygiene; Low for v0.11.0 to v0.11.2 feature scope.

Suggested fix:

- Filter expected process activities in the test, or update the expected sequence to include session/message events.

### 3. `tests/test_worker_skill.py` uses default ignored runtime data

The test expects worker runner idle state, but the default worker store reads `data/workers`.
Local ignored data can make the worker claim and fail a persisted queued job.

Severity: Medium for deterministic test hygiene; Low for v0.11.0 to v0.11.2 feature scope.

Suggested fix:

- Inject a temp worker store/runner into the skill execution path, or isolate `data/workers` during the test.

### 4. JSONL exists in older non-audited runtime stores

JSONL-backed stores exist in worker/scheduler/editing-related subsystems.

Severity: Unknown for global architecture until scope is clarified.

Reasoning:

- The audit target specifically checked v0.10.0 to v0.11.2 canonicality promises for session/message/memory/instruction/hook/session-continuity/tool-registry/verification/outcomes.
- Verification and outcome layers do not introduce canonical JSONL stores.
- If the principle is interpreted globally across all runtime subsystems, worker/scheduler/editing stores need a separate migration or explicit exemption.

## Audit Conclusion

Based on the inspected files, boundary greps, passing acceptance suite, and smoke script results, the v0.10.0 to v0.11.2 implementation matches the stated architectural direction for the audited features: OCEL remains canonical for the targeted session, memory, instruction, hook, continuity, tool-registry view, verification, and outcome layers; Markdown remains non-canonical; verification read-only skills stay observational; and outcome evaluation is deterministic and evidence-based.

The implementation is not completely clean under unrestricted `pytest` execution: repository-wide collection is polluted by reference scripts, and full `tests/` has two failing tests that appear to be stale or environment-state dependent rather than v0.11.x boundary violations. These should be fixed before claiming the entire repository test suite is green.

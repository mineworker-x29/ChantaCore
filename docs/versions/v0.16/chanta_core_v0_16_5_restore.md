# ChantaCore v0.16.5 Restore Notes

Version: 0.16.5

Name: Personal Runtime Smoke Tests

## Restore Goal

ChantaCore v0.16.5 adds a generic Personal Runtime Smoke Test layer. The layer checks whether prompt-facing Personal Mode, Personal Overlay, Personal Runtime Binding, and Personal Conformance artifacts behave coherently under deterministic local smoke cases.

The smoke test layer is diagnostic only. It records scenarios, cases, runs, observations, assertions, and results. It does not call an LLM by default, execute tools, activate modes, import sources, grant permissions, or mutate runtime behavior.

The restoration target is a public, generic framework for checking Personal Runtime prompt-facing boundary behavior without embedding private persona material or making personal text authoritative over runtime capability truth.

## Implemented Files

Primary implementation:

- `src/chanta_core/persona/personal_smoke_test.py`
- `src/chanta_core/persona/history_adapter.py`
- `src/chanta_core/persona/__init__.py`
- `src/chanta_core/persona/ids.py`
- `src/chanta_core/pig/reports.py`

Tests:

- `tests/test_personal_smoke_test_models.py`
- `tests/test_personal_smoke_test_service.py`
- `tests/test_personal_smoke_test_ocel_shape.py`
- `tests/test_personal_smoke_test_history_adapter.py`
- `tests/test_personal_smoke_test_boundaries.py`
- `tests/test_pig_reports.py`

Restore document:

- `docs/versions/v0.16/chanta_core_v0_16_5_restore.md`

## Product Boundary

The public ChantaCore surface remains generic. The public concepts are Personal Directory, Personal Source, Personal Profile, Personal Overlay, Personal Projection, Personal Mode, Personal Runtime Binding, Personal Conformance, and Personal Runtime Smoke Test.

The smoke test framework may verify that prompt-facing text respects declared boundaries. It must not make personal claims authoritative over runtime capability truth. The actual runtime capability profile remains the source of truth for execution.

## Public API / Model Surface

`PersonalSmokeTestScenario` defines a smoke test scenario. It records scenario name, type, optional target Personal Mode/Profile/Binding references, lifecycle status, privacy flag, and metadata.

`PersonalSmokeTestCase` defines one prompt-facing case. It records input prompt, expected behavior, required claims, forbidden claims, expected mode, and expected runtime kind.

`PersonalSmokeTestRun` records one deterministic smoke run over a scenario and a set of cases.

`PersonalSmokeTestObservation` records static observed output and optional observed prompt blocks, mode, runtime kind, and capability metadata.

`PersonalSmokeTestAssertion` records one assertion over an observation. Assertions cover required claims, forbidden claims, mode match, runtime kind match, capability boundary checks, overlay boundary checks, and prompt bounds.

`PersonalSmokeTestResult` summarizes a run. It records passed, failed, warning, and skipped assertion IDs plus optional score and confidence values bounded to `0.0..1.0`.

Public service:

- `PersonalRuntimeSmokeTestService`

Public helper methods on the service:

- `create_scenario`
- `create_case`
- `start_run`
- `record_observation`
- `record_assertion`
- `record_result`
- `complete_run`
- `fail_run`
- `skip_run`
- `run_cases_against_static_outputs`
- `create_default_boundary_smoke_cases`
- `evaluate_smoke_test_result`
- `render_prompt_smoke_context`

## Service Behavior

`PersonalRuntimeSmokeTestService` provides:

- scenario creation;
- case creation;
- run lifecycle recording;
- observation and assertion recording;
- result calculation;
- deterministic static-output smoke execution;
- default boundary smoke case creation;
- prompt smoke context rendering for inspection.

All default behavior is local and deterministic. Static outputs are supplied by the caller or tests. The service does not call an LLM, execute tools, use shell access, use network access, connect external plugins, or activate runtime modes.

The service records smoke artifacts as OCEL objects/events through `TraceService`. It is a diagnostic service, not a runtime executor.

## Persistence and Canonical State

Smoke test artifacts are OCEL-recorded diagnostic records. They are not canonical persona source, not canonical Personal Directory content, and not runtime activation state.

Canonical runtime capability truth remains outside the smoke test layer. A passing smoke test can show that a prompt-facing output respects declared boundaries, but it cannot grant filesystem, shell, network, MCP, plugin, or local runtime powers.

Markdown restore notes remain human-readable restore aids only.

## Runtime Integration

v0.16.5 does not add active runtime integration. The smoke test service can render a bounded prompt smoke context from supplied loadout, runtime binding, and overlay blocks, but it does not attach that context to `AgentRuntime`, mutate `ChatService`, or select a Personal Mode for live execution.

`ChatService` remains a thin wrapper around `AgentRuntime`. The major prompt/runtime integration surface remains `AgentRuntime`, which owns session context projection, persona projection, Personal Overlay prompt attachment, capability decision surface attachment, and `ProcessRunLoop` integration.

Existing skill selection remains explicit/fallback/decision-assisted through `ProcessRunLoop`; v0.16.5 does not introduce autonomous multi-step natural-language tool orchestration.

## Default Smoke Cases

The default boundary cases use generic Personal Mode and runtime names:

- mode self-report: the output should name the current mode and role boundary without claiming unavailable access;
- capability boundary: the output should deny ambient filesystem access and refer to explicit skills or runtime capability bindings;
- external/manual handoff runtime boundary: the output should not claim local repository or test execution;
- local runtime boundary: the output should distinguish explicit skills from ambient capabilities;
- overlay boundary: the output should not claim reading excluded correspondence areas.

The default cases contain only public-safe dummy text and generic mode names.

## Explicit Non-goals and Boundaries

v0.16.5 deliberately does not add:

- live model smoke execution;
- active Personal Mode switching;
- Personal Directory source import;
- canonical persona import;
- capability grants;
- permission grants;
- workspace file reads;
- workspace writes;
- shell execution;
- network calls;
- MCP connection;
- plugin loading;
- natural-language automatic skill routing;
- child runtime or subagent execution;
- private persona names, private local roots, or private correspondence bodies in public fixtures.

The smoke test layer must keep `model_call_used=False`, `tool_execution_used=False`, `runtime_activation_used=False`, and `permission_grants_created=False` for default deterministic runs.

## Assertion Semantics

Required claims pass when the expected claim text appears in the observed output.

Forbidden claims pass when the claim text is absent. If a forbidden claim appears, the assertion fails.

Mode and runtime-kind assertions compare supplied observed metadata against case expectations.

External chat and manual handoff runtimes are checked for local repository and local test execution claims.

Unavailable capability assertions check that capabilities marked as metadata-only, unavailable, or not implemented are not claimed as executable in the observed text.

## OCEL Shape

New OCEL object types:

- `personal_smoke_test_scenario`
- `personal_smoke_test_case`
- `personal_smoke_test_run`
- `personal_smoke_test_observation`
- `personal_smoke_test_assertion`
- `personal_smoke_test_result`

New OCEL events:

- `personal_smoke_test_scenario_created`
- `personal_smoke_test_case_created`
- `personal_smoke_test_run_started`
- `personal_smoke_test_observation_recorded`
- `personal_smoke_test_assertion_recorded`
- `personal_smoke_test_result_recorded`
- `personal_smoke_test_run_completed`
- `personal_smoke_test_run_failed`
- `personal_smoke_test_run_skipped`

Relations connect cases to scenarios, runs to scenarios and cases, observations and assertions to runs and cases, and results to runs.

Expected relation qualifiers:

- case belongs to scenario;
- run uses scenario;
- run includes case;
- observation belongs to run;
- observation observes case;
- assertion belongs to run;
- assertion checks case;
- result belongs to run.

## Context History

Three adapters project smoke test artifacts into context history:

- `personal_smoke_test_scenarios_to_history_entries`
- `personal_smoke_test_assertions_to_history_entries`
- `personal_smoke_test_results_to_history_entries`

Failed assertions and failed results receive high priority. Needs-review results receive medium/high priority. Passing entries remain lower priority.

## PIG / OCPX Reporting

The Persona Projection section of the PIG report now includes lightweight Personal Smoke Test counts:

- scenario, case, run, observation, assertion, and result counts;
- passed, failed, and needs-review result counts;
- failed and warning assertion counts;
- scenario counts by type;
- average smoke test score when available.

The report remains diagnostic and does not expose private paths or source bodies.

## Test Coverage

Model tests cover:

- smoke scenario, case, run, observation, assertion, and result construction;
- score and confidence bounds;
- dictionary serialization.

Service tests cover:

- scenario and case creation;
- deterministic static-output pass/fail behavior;
- forbidden claim detection;
- external/manual handoff runtime boundary checks;
- unavailable capability claim checks;
- default boundary smoke case creation;
- prompt smoke context rendering.

OCEL tests cover smoke object/event emission and relation shape.

History adapter tests cover priority assignment for failed, warning, needs-review, and passing smoke artifacts.

Boundary tests cover public-safe dummy content and ensure the smoke layer does not introduce live model calls, tool execution, runtime activation, private names, or private correspondence bodies.

PIG report tests cover Personal Smoke Test counts and status summaries.

## Restore Procedure

1. Restore or inspect the package version:

```powershell
Select-String -Path pyproject.toml -Pattern 'version = "0.16.5"'
```

2. Verify the smoke test implementation imports:

```powershell
.\.venv\Scripts\python.exe -c "from chanta_core.persona import PersonalRuntimeSmokeTestService; print(PersonalRuntimeSmokeTestService.__name__)"
```

3. Run the targeted v0.16.5 smoke test subset:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_personal_smoke_test_models.py tests\test_personal_smoke_test_service.py tests\test_personal_smoke_test_ocel_shape.py tests\test_personal_smoke_test_history_adapter.py tests\test_personal_smoke_test_boundaries.py
```

4. Run the PIG report regression that includes Personal Smoke Test counts:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_pig_reports.py
```

5. Run the full suite:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

6. Confirm public generic boundary language:

```powershell
rg -n "model_call_used.*True|tool_execution_used.*True|runtime_activation_used.*True|permission_grants_created.*True" src tests docs
```

7. Confirm no configured private persona names or private local roots are introduced into public files. Keep project-specific private search terms outside public restore docs, then run the local private-term scan against public files:

```powershell
rg -n "<PRIVATE_TERM_PATTERN>" src tests docs README.md pyproject.toml
```

## Restore Checklist

After restoring this version, verify:

- package version is `0.16.5`;
- `PersonalRuntimeSmokeTestService` imports from `chanta_core.persona`;
- model, service, OCEL, history adapter, boundary, and PIG tests exist;
- default boundary smoke cases are created;
- static output assertions pass and fail deterministically;
- forbidden capability claims fail;
- external/manual handoff runtime outputs cannot claim local test execution;
- arbitrary filesystem access claims fail;
- excluded correspondence reading claims fail in dummy smoke cases;
- PIG report includes Personal Smoke Test counts;
- `ChatService` is documented as a thin wrapper, not the owner of major prompt/runtime integration;
- `AgentRuntime` remains the integration owner for persona projection, Personal Overlay, capability decision surface, session context projection, and process run integration;
- existing skill selection is explicit/fallback/decision-assisted, not autonomous multi-step tool orchestration;
- tests pass with public-safe dummy content only.

## Known Limitations

- No CLI command exposes Personal Runtime smoke testing yet.
- No local private overlay smoke runner is included in the public repository.
- No live-model smoke execution is supported by default.
- Smoke assertions are deterministic string/metadata checks; they are not semantic model evaluations.
- A passing smoke run does not prove that every future generated answer will respect the same boundary.
- No Personal Mode prompt activation is introduced here.
- No explicit skill invocation surface is introduced here.

## Future Work

Likely next steps:

- optional read-only CLI smoke command;
- optional local private overlay smoke runner outside the public repository;
- controlled live-model smoke tests only when explicitly enabled;
- richer prompt projection smoke fixtures for user-managed Personal Directories.
- Personal Runtime CLI / local config surface;
- Personal Mode prompt-context activation that still grants no capabilities;
- explicit skill invocation surface with capability decision references;
- read-only execution gate after explicit skill invocation semantics are stable.

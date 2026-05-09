# ChantaCore v0.16.5 Restore Notes

Version: 0.16.5

Name: Personal Runtime Smoke Tests

## Purpose

ChantaCore v0.16.5 adds a generic Personal Runtime Smoke Test layer. The layer checks whether prompt-facing Personal Mode, Personal Overlay, Personal Runtime Binding, and Personal Conformance artifacts behave coherently under deterministic local smoke cases.

The smoke test layer is diagnostic only. It records scenarios, cases, runs, observations, assertions, and results. It does not call an LLM by default, execute tools, activate modes, import sources, grant permissions, or mutate runtime behavior.

## Product Boundary

The public ChantaCore surface remains generic. The public concepts are Personal Directory, Personal Source, Personal Profile, Personal Overlay, Personal Projection, Personal Mode, Personal Runtime Binding, Personal Conformance, and Personal Runtime Smoke Test.

The smoke test framework may verify that prompt-facing text respects declared boundaries. It must not make personal claims authoritative over runtime capability truth. The actual runtime capability profile remains the source of truth for execution.

## Added Models

`PersonalSmokeTestScenario` defines a smoke test scenario. It records scenario name, type, optional target Personal Mode/Profile/Binding references, lifecycle status, privacy flag, and metadata.

`PersonalSmokeTestCase` defines one prompt-facing case. It records input prompt, expected behavior, required claims, forbidden claims, expected mode, and expected runtime kind.

`PersonalSmokeTestRun` records one deterministic smoke run over a scenario and a set of cases.

`PersonalSmokeTestObservation` records static observed output and optional observed prompt blocks, mode, runtime kind, and capability metadata.

`PersonalSmokeTestAssertion` records one assertion over an observation. Assertions cover required claims, forbidden claims, mode match, runtime kind match, capability boundary checks, overlay boundary checks, and prompt bounds.

`PersonalSmokeTestResult` summarizes a run. It records passed, failed, warning, and skipped assertion IDs plus optional score and confidence values bounded to `0.0..1.0`.

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

## Default Smoke Cases

The default boundary cases use generic Personal Mode and runtime names:

- mode self-report: the output should name the current mode and role boundary without claiming unavailable access;
- capability boundary: the output should deny ambient filesystem access and refer to explicit skills or runtime capability bindings;
- external/manual handoff runtime boundary: the output should not claim local repository or test execution;
- local runtime boundary: the output should distinguish explicit skills from ambient capabilities;
- overlay boundary: the output should not claim reading excluded correspondence areas.

The default cases contain only public-safe dummy text and generic mode names.

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

## Restore Checklist

After restoring this version, verify:

- package version is `0.16.5`;
- `PersonalRuntimeSmokeTestService` imports from `chanta_core.persona`;
- default boundary smoke cases are created;
- static output assertions pass and fail deterministically;
- forbidden capability claims fail;
- external/manual handoff runtime outputs cannot claim local test execution;
- arbitrary filesystem access claims fail;
- excluded correspondence reading claims fail in dummy smoke cases;
- PIG report includes Personal Smoke Test counts;
- tests pass with public-safe dummy content only.

## Future Work

Likely next steps:

- optional read-only CLI smoke command;
- optional local private overlay smoke runner outside the public repository;
- controlled live-model smoke tests only when explicitly enabled;
- richer prompt projection smoke fixtures for user-managed Personal Directories.

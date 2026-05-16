# ChantaCore v0.12.3 Restore Notes

Version: v0.12.3
Name: ChantaCore v0.12.3 - Shell/Network Risk Pre-Sandbox

This document is intended to be enough to restore the v0.12.3 work from a damaged
or partially reverted tree. It records scope, files, public APIs, OCEL shape,
boundary decisions, tests, and known limitations.

## Restore Goal

v0.12.3 adds a non-enforcing, OCEL-native pre-sandbox recording layer for shell
command and network access risk. It does not block, mutate, execute, or call out.
It records process-intelligence data before any future enforcement layer exists.

The canonical state is OCEL:

- OCEL events
- OCEL objects
- OCEL event-object relations
- OCEL object-object relations

JSONL is not canonical for shell/network risk state.
Markdown is not canonical; this file is only a human-readable restore aid.

## Files Added Or Modified

Primary implementation:

- `src/chanta_core/sandbox/shell_network.py`
- `src/chanta_core/sandbox/ids.py`
- `src/chanta_core/sandbox/errors.py`
- `src/chanta_core/sandbox/history_adapter.py`
- `src/chanta_core/sandbox/__init__.py`

Report/read-model integration:

- `src/chanta_core/pig/reports.py`
- `src/chanta_core/pig/inspector.py`

Script:

- `scripts/test_shell_network_pre_sandbox.py`

Tests:

- `tests/test_shell_network_pre_sandbox_models.py`
- `tests/test_shell_network_pre_sandbox_analysis.py`
- `tests/test_shell_network_pre_sandbox_service.py`
- `tests/test_shell_network_pre_sandbox_history_adapter.py`
- `tests/test_shell_network_pre_sandbox_ocel_shape.py`
- `tests/test_shell_network_pre_sandbox_boundaries.py`
- `tests/test_imports.py`
- `tests/test_pig_reports.py`

Version/doc:

- `pyproject.toml`
- `src/chanta_core/__init__.py`
- `docs/versions/v0.12/chanta_core_v0_12_3_restore.md`

## IDs

The ID helpers live in `src/chanta_core/sandbox/ids.py`.

Required helpers and prefixes:

- `new_shell_command_intent_id()` -> `shell_command_intent:...`
- `new_network_access_intent_id()` -> `network_access_intent:...`
- `new_shell_network_risk_assessment_id()` -> `shell_network_risk_assessment:...`
- `new_shell_network_pre_sandbox_decision_id()` -> `shell_network_pre_sandbox_decision:...`
- `new_shell_network_risk_violation_id()` -> `shell_network_risk_violation:...`

The implementation uses `uuid4()` like nearby sandbox ID helpers.

## Errors

The error hierarchy is in `src/chanta_core/sandbox/errors.py`.

Required classes:

- `ShellNetworkRiskError`
- `ShellCommandIntentError`
- `NetworkAccessIntentError`
- `ShellNetworkRiskAssessmentError`
- `ShellNetworkPreSandboxDecisionError`
- `ShellNetworkRiskViolationError`

All shell/network errors inherit from `SandboxError` through
`ShellNetworkRiskError`.

## Core Models

All models are frozen dataclasses in `src/chanta_core/sandbox/shell_network.py`
and expose `to_dict()`.

### ShellCommandIntent

Fields:

- `intent_id`
- `command_text`
- `shell_type`
- `cwd`
- `requester_type`
- `requester_id`
- `session_id`
- `turn_id`
- `process_instance_id`
- `permission_request_id`
- `session_permission_resolution_id`
- `workspace_write_decision_id`
- `reason`
- `created_at`
- `intent_attrs`

Allowed `shell_type` values:

- `bash`
- `powershell`
- `cmd`
- `python`
- `unknown`
- `other`

### NetworkAccessIntent

Fields:

- `intent_id`
- `url`
- `host`
- `port`
- `protocol`
- `method`
- `requester_type`
- `requester_id`
- `session_id`
- `turn_id`
- `process_instance_id`
- `permission_request_id`
- `session_permission_resolution_id`
- `reason`
- `created_at`
- `intent_attrs`

No DNS lookup is done. URL parsing is structural only.

### ShellNetworkRiskAssessment

Fields:

- `assessment_id`
- `intent_kind`
- `intent_id`
- `risk_level`
- `risk_categories`
- `detected_tokens`
- `detected_targets`
- `summary`
- `confidence`
- `created_at`
- `assessment_attrs`

Allowed `intent_kind` values:

- `shell_command`
- `network_access`

Allowed `risk_level` values:

- `unknown`
- `low`
- `medium`
- `high`
- `critical`

Important risk categories:

- `read_only`
- `filesystem_write`
- `destructive_filesystem`
- `shell_execution`
- `network_access`
- `credential_exposure`
- `exfiltration_risk`
- `privilege_change`
- `process_control`
- `package_install`
- `remote_code_execution`
- `unknown`
- `other`

`confidence`, when present, must be in `[0.0, 1.0]`.

### ShellNetworkRiskViolation

Fields:

- `violation_id`
- `intent_kind`
- `intent_id`
- `assessment_id`
- `violation_type`
- `severity`
- `description`
- `created_at`
- `violation_attrs`

Important violation types:

- `destructive_command`
- `outside_workspace_write_risk`
- `network_access_risk`
- `credential_exposure_risk`
- `exfiltration_risk`
- `privilege_change_risk`
- `package_install_risk`
- `remote_code_execution_risk`
- `unknown_or_unparsed_intent`
- `other`

### ShellNetworkPreSandboxDecision

Fields:

- `decision_id`
- `intent_kind`
- `intent_id`
- `assessment_id`
- `decision`
- `decision_basis`
- `risk_level`
- `violation_ids`
- `confidence`
- `reason`
- `enforcement_enabled`
- `created_at`
- `decision_attrs`

Allowed decisions:

- `allow_recommended`
- `deny_recommended`
- `needs_review`
- `inconclusive`
- `error`

Important rule:

- `enforcement_enabled` must be `False`.

If this field can become true, the v0.12.3 boundary has been violated.

## Service

The service is `ShellNetworkRiskPreSandboxService`.

Constructor:

- `trace_service: TraceService | None = None`
- `ocel_store: OCELStore | None = None`

Key methods:

- `create_shell_command_intent(...)`
- `create_network_access_intent(...)`
- `record_risk_assessment(...)`
- `record_risk_violation(...)`
- `record_pre_sandbox_decision(...)`
- `assess_shell_command_intent(intent=...)`
- `assess_network_access_intent(intent=...)`
- `evaluate_shell_command_intent(intent=...)`
- `evaluate_network_access_intent(intent=...)`

The evaluation methods are deterministic wrappers:

1. Record/evaluate the intent.
2. Build a deterministic assessment.
3. Create violation objects for high-risk categories where applicable.
4. Record an advisory pre-sandbox decision with `enforcement_enabled=False`.
5. Persist all state through OCEL.

No method should execute a command, call a network API, call an LLM, mutate a
runtime tool call, or write files except through normal OCEL persistence.

## Deterministic Shell Analysis

Shell command analysis is lexical and structural.

Expected behavior:

- Uses parsing/tokenization helpers such as `shlex` where possible.
- Detects destructive filesystem patterns.
- Detects filesystem write-like patterns.
- Detects command execution and remote execution patterns.
- Detects network-capable command tokens such as curl-like or wget-like use.
- Detects package install patterns.
- Detects credential-looking tokens.
- Detects exfiltration-looking patterns.
- Assigns risk level deterministically from detected categories.

It does not execute the command and does not inspect live filesystem effects.

## Deterministic Network Analysis

Network access analysis is structural.

Expected behavior:

- Parses URL/host/protocol/port where provided.
- Records unknown or malformed targets as risk data.
- Treats network access as a risk category to be reviewed.
- Does not perform DNS lookup.
- Does not open sockets.
- Does not call `requests`, `httpx`, browser APIs, or subprocess network tools.

## OCEL Object Types

The following object types must exist when records are created:

- `shell_command_intent`
- `network_access_intent`
- `shell_network_risk_assessment`
- `shell_network_pre_sandbox_decision`
- `shell_network_risk_violation`

Object attrs should include each model's `to_dict()` content plus stable
presentation fields such as `object_key` and `display_name` when available.

## OCEL Event Activities

Required event activities:

- `shell_command_intent_created`
- `network_access_intent_created`
- `shell_network_risk_assessment_recorded`
- `shell_network_pre_sandbox_evaluated`
- `shell_network_pre_sandbox_decision_recorded`
- `shell_network_risk_violation_recorded`

Event attrs must keep these boundary markers:

- `source_runtime = "chanta_core"`
- `observability_only = True`
- `shell_network_pre_sandbox_only = True`
- `runtime_effect = False`
- `enforcement_enabled = False`

## OCEL Relations

Expected relation intent:

- intent objects relate to session/process/turn where identifiers are provided.
- assessment relates to its intent.
- violation relates to its intent and assessment.
- decision relates to its intent, assessment, and violations.
- permission request and session permission resolution IDs are preserved by
  relation when provided.
- workspace write sandbox decision references are preserved for shell command
  intents when provided.

Exact relation qualifiers may follow the existing helper style, but object
centric recovery must be possible from OCEL alone.

## ContextHistory Adapter

The history adapter additions live in
`src/chanta_core/sandbox/history_adapter.py`.

Required helpers:

- `shell_command_intents_to_history_entries`
- `network_access_intents_to_history_entries`
- `shell_network_risk_assessments_to_history_entries`
- `shell_network_pre_sandbox_decisions_to_history_entries`
- `shell_network_risk_violations_to_history_entries`

Expected history entry behavior:

- `source = "shell_network_pre_sandbox"` for risk/decision/violation records.
- `role = "context"`.
- refs include intent, assessment, decision, violation, session, process, and
  permission IDs where available.
- higher risk and denial/review recommendations get higher priority.

The adapter must operate on supplied objects only. It must not query OCEL
automatically.

## PIG/OCPX Report Support

PIG report support was extended in `src/chanta_core/pig/reports.py`.

The lightweight report summary should expose:

- `shell_command_intent_count`
- `network_access_intent_count`
- `shell_network_risk_assessment_count`
- `shell_network_pre_sandbox_decision_count`
- `shell_network_risk_violation_count`
- shell risk level counts
- network risk level counts
- pre-sandbox decision counts
- violation type counts
- event activity counts for created/recorded/evaluated events

`src/chanta_core/pig/inspector.py` should include the same summary under
`shell_network_pre_sandbox_summary`.

No conformance scoring or enforcement logic belongs to v0.12.3.

## Public Imports

`src/chanta_core/sandbox/__init__.py` must export:

- `ShellCommandIntent`
- `NetworkAccessIntent`
- `ShellNetworkRiskAssessment`
- `ShellNetworkPreSandboxDecision`
- `ShellNetworkRiskViolation`
- `ShellNetworkRiskPreSandboxService`
- shell/network history adapter helpers

`tests/test_imports.py` should import these symbols.

## Script

`scripts/test_shell_network_pre_sandbox.py` is a local smoke script.

It should:

- create the service
- record a shell command intent
- assess/evaluate it
- record a network access intent
- assess/evaluate it
- print IDs and decisions

It must not require LM Studio.
It must not execute shell/network actions.

## Boundary Tests

`tests/test_shell_network_pre_sandbox_boundaries.py` should verify that the
implementation does not contain active execution paths.

Forbidden behavior:

- command execution
- network call
- DNS lookup
- LLM classifier
- file write outside OCEL persistence
- `ToolDispatcher` mutation
- `AgentRuntime` enforcement gate
- `enforcement_enabled=True`

Boundary tests may mention forbidden terms as test strings. The implementation
must not use them as active behavior.

## Acceptance Tests

Run targeted tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_shell_network_pre_sandbox_models.py tests\test_shell_network_pre_sandbox_analysis.py tests\test_shell_network_pre_sandbox_service.py tests\test_shell_network_pre_sandbox_history_adapter.py tests\test_shell_network_pre_sandbox_ocel_shape.py tests\test_shell_network_pre_sandbox_boundaries.py
```

Run broader acceptance with later v0.13 tests when available:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_imports.py tests\test_pig_reports.py
```

As of the v0.13.1 restore pass, the full local suite result was:

- `563 passed`
- `1 skipped`
- `3 warnings`

The warnings were expected invalid JSONL-row warnings in unrelated store tests.

## Git Hygiene

Runtime outputs must remain ignored:

- `data/`
- `.pytest-tmp/`
- `*.sqlite`
- `*.sqlite3`
- `.env`
- `.env.*` except `.env.example`
- `.venv/`
- `__pycache__/`
- `*.pyc`
- `src/chanta_core.egg-info/`

Observed hygiene during v0.13.1 restore pass:

- `data/` ignored
- `.pytest-tmp/` ignored
- tracked `.sqlite` match was only `tests/test_ocel_export_sqlite.py`
- tracked `.env` match was only `.env.example`

## Non-Goals

v0.12.3 intentionally does not implement:

- active shell sandbox enforcement
- active network sandbox enforcement
- runtime blocking
- permission inheritance or mutation
- tool dispatch modification
- LLM risk classification
- external policy engines
- UI

Future versions may use these records for policy or conformance, but this
version only records deterministic pre-sandbox evidence.

# ChantaCore v0.12.2 Restore

## Version

ChantaCore v0.12.2 - Workspace Write Sandbox.

## Purpose

v0.12.2 adds the OCEL-native workspace write sandbox foundation.

This release records workspace roots, write boundaries, write intents, sandbox
decisions, and violations. The decision policy is deterministic and path-based.
It evaluates whether an intended write target is inside a workspace root and
whether it matches protected or denied write boundaries.

The canonical source remains OCEL event/object/relation records. No canonical
JSONL sandbox store is introduced. Markdown tool policy or sandbox notes remain
human-readable materialized views only and are not source of truth.

## Added Package

The release adds `src/chanta_core/sandbox/`:

- `__init__.py`
- `ids.py`
- `errors.py`
- `models.py`
- `service.py`
- `history_adapter.py`

## Models

The active workspace write sandbox models are:

- `WorkspaceRoot`
- `WorkspaceWriteBoundary`
- `WorkspaceWriteIntent`
- `WorkspaceWriteSandboxDecision`
- `WorkspaceWriteSandboxViolation`

They are represented in OCEL with object types:

- `workspace_root`
- `workspace_write_boundary`
- `workspace_write_intent`
- `workspace_write_sandbox_decision`
- `workspace_write_sandbox_violation`

`WorkspaceWriteIntent` is only an intent record. It does not execute the
operation.

`WorkspaceWriteSandboxDecision` always records `enforcement_enabled=False` in
v0.12.2. Decisions do not block runtime behavior.

## Path Helpers

The service exposes deterministic path helpers:

- `normalize_path(...)`
- `is_path_inside_root(...)`
- `is_same_or_child_path(...)`

The helpers use `pathlib.Path`, `resolve(strict=False)`, and `relative_to`-style
containment. They do not require target paths to exist and do not use naive
string prefix checks as the sole containment rule.

## Service

`WorkspaceWriteSandboxService` records workspace write sandbox facts through
`TraceService` and `OCELStore`.

It supports:

- registering, updating, and deprecating workspace roots;
- registering, updating, and deprecating write boundaries;
- creating write intent records;
- recording violations;
- recording decisions;
- evaluating a write intent from a provided root and boundaries.

The service records OCEL events such as:

- `workspace_root_registered`
- `workspace_root_updated`
- `workspace_root_deprecated`
- `workspace_write_boundary_registered`
- `workspace_write_boundary_updated`
- `workspace_write_boundary_deprecated`
- `workspace_write_intent_created`
- `workspace_write_sandbox_evaluated`
- `workspace_write_sandbox_decision_recorded`
- `workspace_write_sandbox_violation_recorded`

## Decision Policy

Resolution is deterministic:

- no workspace root -> `inconclusive`, basis `no_workspace_root`;
- target outside workspace -> outside-workspace violation and `denied`;
- target inside protected boundary -> protected-path violation and `denied`;
- target inside denied boundary -> denied-path violation and `denied`;
- target inside workspace with no denying boundary -> `allowed`.

All decisions record `enforcement_enabled=False`.

## Boundary

v0.12.2 remains a guard-model/read-model layer.

This release does not implement:

- actual file writes;
- file creation, editing, deletion, path move, or permission mutation;
- ToolDispatcher active gate;
- AgentRuntime active gate;
- tool blocking;
- tool input or output mutation;
- shell sandbox;
- network sandbox;
- shell execution;
- network calls;
- LLM classifier;
- automatic permission grant application;
- automatic denial from verification or outcome evaluation;
- Markdown-as-sandbox source behavior;
- canonical JSONL sandbox persistence;
- external connector, MCP, plugin, or marketplace sandbox loading;
- async runtime;
- UI.

## Context Projection

The sandbox history adapter exposes:

- `workspace_write_intents_to_history_entries(...)`
- `workspace_write_sandbox_decisions_to_history_entries(...)`
- `workspace_write_sandbox_violations_to_history_entries(...)`

Entries use `source="workspace_write_sandbox"` and preserve refs for intent,
decision, violation, workspace root, session, turn, process, permission request,
and session permission resolution IDs.

Violations and denied decisions receive higher priority than allowed decisions.

## PIG / OCPX Reporting

PIG reports include lightweight workspace write sandbox counts:

- workspace root count
- workspace write boundary count
- workspace write intent count
- workspace write sandbox decision count
- workspace write sandbox violation count
- allowed / denied / needs review / inconclusive / error counts
- outside workspace violation count
- protected path violation count
- denied path violation count

This is reporting only. It is not runtime enforcement or conformance failure.

## Restore Checklist

- `src/chanta_core/sandbox/` exists.
- Workspace write sandbox models expose `to_dict()`.
- Path containment helpers use resolved paths and structural containment.
- `enforcement_enabled` remains false.
- `WorkspaceWriteSandboxService` emits OCEL records.
- Inside-workspace intent resolves allowed.
- Outside-workspace intent resolves denied with violation.
- Protected or denied boundary resolves denied with violation.
- No workspace root resolves inconclusive.
- No file write occurs.
- No ToolDispatcher or AgentRuntime active gate is introduced.
- No shell/network sandbox is introduced.
- No LLM classifier is introduced.
- No Markdown sandbox source is introduced.
- No canonical sandbox JSONL store is introduced.

## Restore / Verification Commands

Representative tests:

```powershell
.\.venv\Scripts\python.exe -m pytest `
  tests\test_imports.py `
  tests\test_workspace_write_sandbox_models.py `
  tests\test_workspace_write_sandbox_path_helpers.py `
  tests\test_workspace_write_sandbox_service.py `
  tests\test_workspace_write_sandbox_history_adapter.py `
  tests\test_workspace_write_sandbox_ocel_shape.py `
  tests\test_workspace_write_sandbox_boundaries.py `
  tests\test_pig_reports.py
```

Full test suite:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Smoke script:

```powershell
.\.venv\Scripts\python.exe scripts\test_workspace_write_sandbox.py
```

## Remaining Limitations

- No active write enforcement yet.
- No ToolDispatcher gate yet.
- No shell/network risk pre-sandbox yet.
- No active sandbox integration with AgentRuntime yet.
- No UI.

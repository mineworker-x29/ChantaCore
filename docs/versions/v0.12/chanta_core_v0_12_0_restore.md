# ChantaCore v0.12.0 Restore

## Version

ChantaCore v0.12.0 - Permission Scope & Grant Model.

## Purpose

ChantaCore v0.12.0 adds the OCEL-native permission model foundation.

This release defines permission scopes, requests, decisions, grants, denials,
and policy notes as records. It does not enforce them. It creates the
object-centric audit substrate that later permission enforcement layers can
reference.

The canonical source remains OCEL event/object/relation records. No canonical
JSONL permission store is introduced. Markdown tool policy views remain
human-readable materialized views only and are not used as permission source of
truth.

## Added Package

The release adds `src/chanta_core/permissions/`:

- `__init__.py`
- `ids.py`
- `errors.py`
- `models.py`
- `service.py`
- `history_adapter.py`

## Models

The new permission package defines `PermissionScope`, `PermissionRequest`,
`PermissionDecision`, `PermissionGrant`, `PermissionDenial`, and
`PermissionPolicyNote`. These are persisted as OCEL objects and connected to
permission lifecycle events.

They are represented in OCEL with object types:

- `permission_scope`
- `permission_request`
- `permission_decision`
- `permission_grant`
- `permission_denial`
- `permission_policy_note`

`PermissionScope` records a named permission boundary:

- scope name and type
- target type and ref
- allowed and denied operation lists
- risk level
- status and timestamps
- attrs

`PermissionRequest` records a requested operation:

- request type
- requester metadata
- target type and ref
- operation
- optional scope ID
- risk level and reason
- session, turn, and process refs
- tool descriptor ref
- verification result refs
- process outcome evaluation refs

`PermissionDecision` records a decision value only. It validates confidence when
provided. It does not affect runtime behavior in v0.12.0.

`PermissionGrant` and `PermissionDenial` are inert records. Their OCEL object
attributes include an inert marker for v0.12.0.

`PermissionPolicyNote` records informational or review-oriented notes. It
rejects policy note types that imply active enforcement, automatic allow/deny,
automatic blocking, or sandbox behavior.

## Service

`PermissionModelService` records permission facts through `TraceService` and
`OCELStore`.

It supports:

- registering, updating, and deprecating scopes;
- creating requests;
- marking requests pending;
- cancelling and expiring requests;
- recording decisions;
- recording grants;
- revoking and expiring grants;
- recording denials;
- registering, updating, and deprecating policy notes.

The service records OCEL events such as:

- `permission_scope_registered`
- `permission_scope_updated`
- `permission_scope_deprecated`
- `permission_request_created`
- `permission_request_marked_pending`
- `permission_request_cancelled`
- `permission_request_expired`
- `permission_decision_recorded`
- `permission_grant_recorded`
- `permission_grant_revoked`
- `permission_grant_expired`
- `permission_denial_recorded`
- `permission_policy_note_registered`
- `permission_policy_note_updated`
- `permission_policy_note_deprecated`

The service is append-oriented and observational. It does not prompt the user,
does not call an LLM classifier, and does not apply decisions or grants to the
runtime.

## OCEL Relations

The permission service records best-effort object-centric relations where the
current OCEL APIs allow them:

- request uses scope
- decision decides request
- grant grants request
- denial denies request
- policy note describes scope
- request targets a tool descriptor
- request references verification results
- request references process outcome evaluations
- request belongs to session, turn, or process context
- grants and denials can belong to a session

These relations are trace facts only. They are not runtime permission checks.

## Record-only Boundary

This release is record-only. `PermissionDecision` does not affect runtime
behavior. `PermissionGrant` and `PermissionDenial` are inert records in v0.12.0.
They do not allow, block, alter, or cancel tool calls.

No runtime enforcement exists yet. No tool blocking exists yet. No sandbox
exists yet. No LLM classifier is used. Markdown tool policy views are not a
permission source of truth. No canonical JSONL permission store is introduced.

This release does not implement:

- runtime enforcement;
- active `ToolDispatcher` gates;
- tool blocking;
- tool input or output mutation;
- workspace write sandbox;
- shell sandbox;
- network sandbox;
- LLM permission classifier;
- automatic grant application;
- automatic denial from process outcomes;
- hook enforcement;
- Markdown-as-permission source behavior;
- canonical JSONL permission persistence;
- external connectors, MCP, plugin, or marketplace permission loading;
- async runtime;
- UI;
- external dependencies.

## Context Projection

The permission history adapter converts provided permission objects into
prompt-facing `ContextHistoryEntry` values:

- `permission_requests_to_history_entries(...)`
- `permission_decisions_to_history_entries(...)`
- `permission_grants_to_history_entries(...)`
- `permission_denials_to_history_entries(...)`

Entries use `source="permission"` and preserve relevant refs:

- request ID
- decision ID
- grant ID
- denial ID
- scope ID
- session ID
- turn ID
- process instance ID
- tool descriptor ID
- verification result IDs
- outcome evaluation IDs

Denials and pending requests receive higher priority. Grants remain context
records only and are not treated as executable authority.

## PIG / OCPX Reporting

PIG reports include lightweight permission model counts:

- permission scope count
- permission request count
- permission decision count
- permission grant count
- permission denial count
- permission policy note count
- permission requests by type
- permission requests by operation
- decision allow / deny / ask / defer counts
- active grant count

This is reporting only. It is not conformance failure, runtime enforcement, or
permission evaluation.

## Restore Checklist

- `src/chanta_core/permissions/` exists.
- All permission models expose `to_dict()`.
- ID helpers use stable permission prefixes.
- Confidence validation is active for permission decisions.
- Forbidden policy note types are rejected.
- `PermissionModelService` emits OCEL records.
- OCEL object types for scopes, requests, decisions, grants, denials, and policy
  notes are used.
- Grant, denial, and decision records are inert in v0.12.0.
- Permission history adapters exist.
- PIG report exposes permission counts.
- No runtime enforcement is introduced.
- No tool blocking or tool mutation is introduced.
- No sandbox is introduced.
- No LLM classifier is introduced.
- No Markdown permission source is introduced.
- No canonical permission JSONL store is introduced.

## Restore / Verification Commands

Representative tests:

```powershell
.\.venv\Scripts\python.exe -m pytest `
  tests\test_imports.py `
  tests\test_permission_models.py `
  tests\test_permission_model_service.py `
  tests\test_permission_history_adapter.py `
  tests\test_permission_ocel_shape.py `
  tests\test_permission_boundaries.py `
  tests\test_process_outcome_models.py `
  tests\test_process_outcome_service.py `
  tests\test_pig_reports.py
```

Full test suite:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Smoke script:

```powershell
.\.venv\Scripts\python.exe scripts\test_permission_model.py
```

## Remaining Limitations

- v0.12.1 session-scoped permission enforcement
- v0.12.2 workspace write sandbox
- v0.12.3 shell/network risk pre-sandbox
- later UI and review workflow support

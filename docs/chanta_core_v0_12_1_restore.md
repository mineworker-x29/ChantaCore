# ChantaCore v0.12.1 Restore

## Version

ChantaCore v0.12.1 - Session-scoped Permission.

## Purpose

v0.12.1 adds the OCEL-native session-scoped permission read-model.

The release introduces session permission context, snapshot, and resolution
records. These records describe what permission grants, denials, and pending
requests are visible for a single session. They do not enforce runtime
behavior.

The canonical source remains OCEL event/object/relation records. No canonical
JSONL permission store is introduced. Markdown tool policy views remain
human-readable materialized views only and are not permission source of truth.

## Added File

The release adds:

- `src/chanta_core/permissions/session.py`

The existing permission package remains the base object model:

- `src/chanta_core/permissions/models.py`
- `src/chanta_core/permissions/service.py`
- `src/chanta_core/permissions/history_adapter.py`

## Models

The active session permission models are:

- `SessionPermissionContext`
- `SessionPermissionSnapshot`
- `SessionPermissionResolution`

They are represented in OCEL with object types:

- `session_permission_context`
- `session_permission_snapshot`
- `session_permission_resolution`

`SessionPermissionContext` records the session ID, lifecycle status, active
scope IDs, active grant IDs, active denial IDs, and pending request IDs.

`SessionPermissionSnapshot` records a point-in-time session read-model:

- active grants
- active denials
- pending requests
- expired grants
- revoked grants
- optional summary

`SessionPermissionResolution` records the deterministic resolution of one
permission request from caller-provided grants and denials. It stores:

- resolved decision
- resolution basis
- matched grant IDs
- matched denial IDs
- expired grant IDs
- confidence
- reason
- `enforcement_enabled=False`

`enforcement_enabled` must remain false in v0.12.1.

## Service

`SessionPermissionService` builds session-scoped read-model records on top of
`PermissionModelService`.

It supports:

- creating a session permission context;
- updating a session permission context read-model;
- resetting a context without copying parent grants;
- closing a context;
- creating a session-scoped permission request;
- attaching a grant to a session;
- attaching a denial to a session;
- revoking a session grant;
- expiring session grants;
- building a session snapshot;
- resolving a permission request from provided session grants and denials.

The service records OCEL events such as:

- `session_permission_context_created`
- `session_permission_context_updated`
- `session_permission_context_reset`
- `session_permission_context_closed`
- `session_permission_request_created`
- `session_permission_request_resolved`
- `session_permission_grant_attached`
- `session_permission_grant_revoked`
- `session_permission_grant_expired`
- `session_permission_denial_attached`
- `session_permission_snapshot_created`
- `session_permission_resolution_recorded`

Optional non-inheritance observations may include:

- `session_permission_non_inheritance_recorded`
- `session_permission_resume_reset_observed`
- `session_permission_fork_reset_observed`

## Resolution Policy

Resolution is deterministic and advisory.

For a given session and request:

- a matching denial in the same session resolves to `deny` with
  `resolution_basis="matching_denial"`;
- otherwise a matching active grant in the same session resolves to `allow`
  with `resolution_basis="matching_grant"`;
- otherwise a matching expired grant resolves to `ask` with
  `resolution_basis="expired_grant"`;
- otherwise no match resolves to `ask` with `resolution_basis="no_match"`.

Matching requires:

- target type equality
- target ref equality
- operation equality
- session ID equality

Grants from other sessions are ignored. Expired grants do not allow. Denials
are session-scoped and do not apply across sessions.

## Resume / Fork Boundary

Session resume and fork do not inherit permission grants.

`reset_context(...)` creates a reset session permission context with empty grant,
denial, and pending request lists. If a parent session ID is provided, the record
marks that parent grants were not copied.

## OCEL Relations

The session permission service records best-effort object-centric relations
where current OCEL APIs allow them:

- context belongs to session
- context includes grants, denials, and requests
- snapshot belongs to session and context
- resolution resolves request
- resolution uses grants or denials
- resolution belongs to session

These relations are trace facts only. They are not runtime permission checks.

## Boundary

v0.12.1 remains a read-model/advisory layer.

This release does not implement:

- ToolDispatcher active gate;
- AgentRuntime active gate;
- tool blocking;
- tool input or output mutation;
- workspace write sandbox;
- shell sandbox;
- network sandbox;
- LLM permission classifier;
- automatic grant application to runtime;
- automatic denial from verification or outcome evaluation;
- permission inheritance across resume or fork;
- Markdown-as-permission source behavior;
- canonical JSONL permission persistence;
- external connector, MCP, plugin, or marketplace permission loading;
- async runtime;
- UI.

## Context Projection

The permission history adapter now also exposes:

- `session_permission_contexts_to_history_entries(...)`
- `session_permission_snapshots_to_history_entries(...)`
- `session_permission_resolutions_to_history_entries(...)`

Entries use `source="session_permission"` and preserve refs for context,
snapshot, resolution, session, request, matched grant, matched denial, and
expired grant IDs.

Deny and ask resolutions receive higher priority than allow resolutions.

## PIG / OCPX Reporting

PIG reports include lightweight session permission counts:

- session permission context count
- session permission snapshot count
- session permission resolution count
- resolution allow / deny / ask / inconclusive counts
- session active grant count
- session expired grant count
- session revoked grant count
- session denial count
- session pending permission request count

This is reporting only. It is not enforcement or conformance failure.

## Restore Checklist

- `src/chanta_core/permissions/session.py` exists.
- Session permission models expose `to_dict()`.
- Session permission ID helpers use stable prefixes.
- `enforcement_enabled` remains false.
- `SessionPermissionService` records OCEL events.
- Session permission object types are used.
- Matching same-session grant resolves allow.
- Matching same-session denial resolves deny.
- No match resolves ask.
- Expired grants do not allow.
- Other-session grants are ignored.
- Reset context does not copy parent grants.
- Session permission history adapters exist.
- PIG report exposes session permission counts.
- No runtime enforcement is introduced.
- No tool blocking or mutation is introduced.
- No sandbox is introduced.
- No LLM classifier is introduced.
- No canonical permission JSONL store is introduced.

## Restore / Verification Commands

Representative tests:

```powershell
.\.venv\Scripts\python.exe -m pytest `
  tests\test_imports.py `
  tests\test_session_permission_models.py `
  tests\test_session_permission_service.py `
  tests\test_session_permission_history_adapter.py `
  tests\test_session_permission_ocel_shape.py `
  tests\test_session_permission_boundaries.py `
  tests\test_permission_models.py `
  tests\test_permission_model_service.py `
  tests\test_pig_reports.py
```

Full test suite:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Smoke script:

```powershell
.\.venv\Scripts\python.exe scripts\test_session_permission.py
```

## Remaining Limitations

- No ToolDispatcher active gate yet.
- No workspace write sandbox yet.
- No shell/network risk pre-sandbox yet.
- No active enforcement yet.
- No UI.

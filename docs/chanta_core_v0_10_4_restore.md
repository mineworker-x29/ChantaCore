# ChantaCore v0.10.4 Restore

## Version

ChantaCore v0.10.4 - Session Resume / Fork.

## Purpose

v0.10.4 adds OCEL-native session continuity. Resume and fork operations create
read-model snapshots from OCEL-native session, turn, and message records, then
record continuity events back into OCEL.

The release does not replay a canonical JSONL transcript. Markdown materialized
views are not resume sources. Permission grants and approval state are not
restored; every resume/fork records a `session_permissions_reset` safety marker.

## Added Files

The release extends `src/chanta_core/session/`:

- `snapshots.py`
- `continuity.py`

It also extends:

- `ids.py`
- `errors.py`
- `history_adapter.py`
- `__init__.py`

## Models

`SessionContextSnapshot` records prompt-facing continuity context:

- snapshot ID
- source session ID
- snapshot type
- max turn/message limits
- included turn IDs
- included message IDs
- process instance IDs
- summary
- context entries
- attrs

`SessionResumeRequest` and `SessionResumeResult` describe resume inputs and
outputs. `SessionResumeResult.permission_reset` is `True`.

`SessionForkRequest` and `SessionForkResult` describe fork inputs and outputs.
`SessionForkResult.permission_reset` is `True` and includes both parent and
child session IDs.

## SessionContinuityService

`SessionContinuityService` provides:

- `build_session_context_snapshot(...)`
- `resume_session(...)`
- `fork_session(...)`
- `session_context_snapshot_to_history_entries(...)`

`build_session_context_snapshot(...)` prefers OCEL session view reconstruction
through `OCPXLoader` and can also accept explicit `SessionMessage` and
`ConversationTurn` objects. It does not read a JSONL transcript and does not
mutate canonical messages.

`resume_session(...)`:

1. records `session_resume_requested`;
2. builds a `resume` snapshot;
3. records `session_context_snapshot_created`;
4. records `session_context_reconstructed`;
5. records `session_permissions_reset`;
6. records `session_resumed`;
7. returns `SessionResumeResult(permission_reset=True)`.

It does not create a new session and does not restore grants or approvals.

`fork_session(...)`:

1. records `session_fork_requested`;
2. builds a `fork` snapshot from the parent session;
3. creates a new child session through `SessionService.start_session(...)`;
4. stores fork metadata in child session attrs;
5. records `session_permissions_reset` for the child session;
6. records `session_forked`;
7. records child-to-parent lineage relation best-effort;
8. returns `SessionForkResult(permission_reset=True)`.

Parent messages are referenced through the snapshot. They are not duplicated as
canonical child messages.

## OCEL Object Types

The release actively uses:

- `session_context_snapshot`
- `session_resume`
- `session_fork`
- `session`

Snapshot objects include source session ID, snapshot type, included turn/message
IDs, process IDs, limits, and summary. Resume/fork objects include snapshot IDs,
permission reset flags, reasons, and timestamps.

## OCEL Event Activities

Continuity events:

- `session_resume_requested`
- `session_context_snapshot_created`
- `session_context_reconstructed`
- `session_resumed`
- `session_fork_requested`
- `session_forked`
- `session_permissions_reset`

Failure event names are reserved for future failure paths:

- `session_resume_failed`
- `session_fork_failed`

## Relation Intent

Event-object qualifiers include:

- `session_context`
- `source_session`
- `parent_session`
- `child_session`
- `snapshot_object`
- `resume_object`
- `fork_object`
- `included_turn`
- `included_message`
- `process_context`

Object-object qualifiers include:

- `derived_from_session`
- `includes_turn`
- `includes_message`
- `includes_process_instance`
- `targets_session`
- `uses_snapshot`
- `parent_session`
- `child_session`
- `forked_from_session`

If relation helper APIs change, the restoration standard is that the same
lineage and snapshot facts remain reconstructible from OCEL records.

## Context History Adapter

`session_context_snapshot_to_history_entries(...)` converts snapshot entries
into `ContextHistoryEntry` objects.

For resume snapshots, source is `session_resume`.
For fork snapshots, source is `session_fork`.

Refs include:

- snapshot ID
- source session ID
- message ID when available
- turn ID when available

Roles such as `user` and `assistant` are preserved.

## PIG/OCPX Support

`PIGReportService` includes `session_continuity_summary` in report attrs and
report text:

- session resume count
- session fork count
- session context snapshot count
- session permission reset count
- fork lineage count

This is lightweight reporting only. It is not a full lineage graph.

## Boundaries

v0.10.4 does not:

- use JSONL transcript replay as canonical resume source;
- use Markdown materialized views as canonical resume source;
- restore permission grants;
- restore approval state;
- implement permission/grant model;
- restore external connector, MCP, or plugin state;
- implement semantic retrieval or embeddings;
- add async or UI.

## Restore Checklist

- `SessionContextSnapshot`, `SessionResumeRequest`, `SessionResumeResult`,
  `SessionForkRequest`, and `SessionForkResult` exist and expose `to_dict()`.
- IDs use `session_context_snapshot:`, `session_resume:`, and `session_fork:`
  prefixes.
- `SessionContinuityService.resume_session(...)` records requested, snapshot,
  reconstructed, reset, and resumed events.
- `SessionContinuityService.fork_session(...)` creates a child session and
  records fork lineage.
- `session_permissions_reset` is always recorded for resume/fork.
- Parent messages are referenced by snapshot and are not duplicated as child
  canonical messages.
- Context history adapter preserves user/assistant roles and refs.
- PIG report exposes continuity counts.
- No JSONL or Markdown canonical replay path exists.

## Restore / Verification Commands

Representative tests:

```powershell
.\.venv\Scripts\python.exe -m pytest `
  tests\test_session_continuity_models.py `
  tests\test_session_continuity_service.py `
  tests\test_session_continuity_history_adapter.py `
  tests\test_session_resume_fork_ocel_shape.py `
  tests\test_session_resume_fork_boundaries.py `
  tests\test_pig_reports.py
```

Smoke script:

```powershell
.\.venv\Scripts\python.exe scripts\test_session_continuity.py
```

## Remaining Limitations

- No permission/grant model yet.
- No approval restoration by design.
- No UI for resume/fork.
- No external connector state restore.
- No MCP/plugin state restore.
- No semantic retrieval.
- No full lineage graph UI.

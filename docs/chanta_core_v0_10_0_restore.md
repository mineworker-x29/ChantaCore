# ChantaCore v0.10.0 Restore

## Version

ChantaCore v0.10.0 - OCEL-native Session & Message Substrate.

## Purpose

v0.10.0 introduces the first OCEL-native conversation substrate. ChantaCore's
canonical persistence rule is that durable runtime facts are OCEL
event/object/relation records. JSONL may exist as a debug mirror or export
convenience, but it is not the canonical transcript.

The release adds first-class models for sessions, conversation turns, and
messages, and integrates them into `AgentRuntime`.

## Added Package

The release adds:

- `src/chanta_core/session/__init__.py`
- `src/chanta_core/session/ids.py`
- `src/chanta_core/session/errors.py`
- `src/chanta_core/session/models.py`
- `src/chanta_core/session/service.py`
- `src/chanta_core/session/history_adapter.py`

It updates:

- `src/chanta_core/runtime/agent_runtime.py`
- `src/chanta_core/traces/trace_service.py`
- `src/chanta_core/ocel/store.py`
- `src/chanta_core/ocpx/loader.py`
- `tests/test_imports.py`
- `tests/test_agent_runtime_ocel_shape.py`

## Models

`AgentSession` represents the session object:

- `session_id`
- `session_name`
- `status`
- `created_at`
- `updated_at`
- `closed_at`
- `agent_id`
- `session_attrs`

Status values include `active`, `closed`, and `archived`.

`ConversationTurn` represents a user/assistant turn:

- `turn_id`
- `session_id`
- `status`
- `started_at`
- `completed_at`
- `process_instance_id`
- `user_message_id`
- `assistant_message_id`
- `turn_index`
- `turn_attrs`

Status values include `started`, `completed`, `failed`, and `cancelled`.

`SessionMessage` represents a message:

- `message_id`
- `session_id`
- `turn_id`
- `role`
- `content`
- `content_preview`
- `content_hash`
- `created_at`
- `message_attrs`

Role values include user, assistant, system, tool, context, and other.

`hash_content(text)` uses SHA-256 for deterministic content hashes. Full message
content is stored in OCEL object attrs for local development, with
`content_preview` and `content_hash` included for future external artifact
storage.

## ID Prefixes

ID helpers use these prefixes:

- `session:`
- `conversation_turn:`
- `message:`

`ExecutionContext` still accepts unprefixed session IDs for existing callers;
the OCEL store and loader normalize session object IDs where needed.

## SessionService

`SessionService` records canonical facts through `TraceService` and `OCELStore`.
It does not create a canonical JSONL transcript.

Methods:

- `start_session(...)`
- `close_session(...)`
- `start_turn(...)`
- `record_user_message(...)`
- `record_assistant_message(...)`
- `complete_turn(...)`
- `fail_turn(...)`

The service is intentionally write-oriented in v0.10.0. It creates session,
turn, and message objects and emits lifecycle events, but it does not add a
conversation-history query API or a resume/fork state manager. Retrieval and
session branching are later substrate features.

## OCEL Object Types

The release actively uses:

- `session`
- `conversation_turn`
- `message`

Existing process runtime still uses `process_instance`, `agent`,
`user_request`, `skill`, `prompt`, `llm_call`, `llm_response`, and `outcome`
where appropriate.

## OCEL Event Activities

Session/message lifecycle events include:

- `session_started`
- `session_closed`
- `conversation_turn_started`
- `user_message_received`
- `assistant_message_emitted`
- `conversation_turn_completed`
- `conversation_turn_failed`
- `message_attached_to_turn`
- `process_instance_attached_to_turn`

Event-object relation qualifiers include:

- `session_context`
- `turn_context`
- `message_object`
- `user_message`
- `assistant_message`
- `process_context`

Object-object relation qualifiers include:

- `belongs_to_session`
- `belongs_to_turn`
- `has_user_message`
- `has_assistant_message`
- `runs_process_instance`

The expected OCEL shape after a normal agent run is:

1. A `session` object exists with status/name/agent timestamps in
   `object_attrs`.
2. A `conversation_turn` object exists and belongs to that session.
3. A user `message` object and an assistant `message` object exist.
4. The user and assistant messages belong to the session and, when a turn is
   available, to the turn.
5. If a process instance was created by `ProcessRunLoop`, the turn is linked to
   the process instance with `runs_process_instance` / `process_context`
   semantics.

The relation names are best-effort object-centric structure, not a separate
transcript database. If relation helper APIs change, the restoration standard is
that the same facts remain reconstructible from OCEL event/object/relation
records.

## AgentRuntime Integration

`AgentRuntime.run(...)` now:

1. Creates or uses a session ID.
2. Starts an OCEL-native session.
3. Starts a conversation turn.
4. Records the user message.
5. Runs `ProcessRunLoop` as before.
6. Records the assistant message using `response_text`.
7. Completes the conversation turn and attaches the process instance.
8. Adds `turn_id`, `user_message_id`, and `assistant_message_id` to result
   metadata.

Failure handling records `conversation_turn_failed` before preserving existing
failure semantics.

## Context History Adapter

`session_messages_to_history_entries(...)` converts provided `SessionMessage`
objects into `ContextHistoryEntry` values. It preserves role, session ID, turn
ID, message ID refs, content hash, and source index. It does not retrieve
messages from OCEL automatically.

Adapter output is prompt-facing projection data. It is not canonical storage and
does not mutate session, message, or turn objects. Current callers must supply
the messages they want projected; full OCEL-backed conversation retrieval is
outside this release.

## OCPX/PIG Support

`OCPXLoader.load_session_view(...)` and session-related store functions can
include session, message, and turn activities in session-level views. PIG
reports can therefore see session/message lifecycle events through normal OCPX
activity and object counts.

When restoring this version, verify session support from both sides:

- service-level behavior: `SessionService` emits the lifecycle events listed
  above;
- runtime behavior: `AgentRuntime.run(...)` records message and turn IDs in the
  run metadata;
- read-model behavior: OCPX/PIG can see the resulting OCEL activities and
  object types.

These checks are stronger than only asserting that the dataclasses import.

## Boundaries

v0.10.0 does not:

- implement memory
- implement hooks
- implement session resume/fork
- create canonical JSONL transcripts
- add external dependencies
- add async, UI, MCP, plugins, or external connectors

It also does not define memory semantics. Messages can later become a source for
memory derivation, but v0.10.0 only records the message substrate.

## Restore Checklist

Use this checklist when rebuilding or auditing the release:

- `src/chanta_core/session/` exists and exports models, ID helpers, service, and
  history adapter.
- `new_session_id()`, `new_conversation_turn_id()`, and
  `new_session_message_id()` use stable prefixes.
- `hash_content(...)` is SHA-256 based and deterministic.
- `SessionService.start_session(...)` emits `session_started`.
- `SessionService.start_turn(...)` emits `conversation_turn_started` and, when
  supplied, `process_instance_attached_to_turn`.
- `record_user_message(...)` and `record_assistant_message(...)` create
  `message` objects and emit the expected message events.
- `complete_turn(...)` emits `conversation_turn_completed`.
- `fail_turn(...)` emits `conversation_turn_failed` when used.
- `AgentRuntime.run(...)` keeps existing run behavior while adding session,
  turn, and message IDs to metadata/result attrs.
- No canonical transcript file such as `conversation.jsonl` or `messages.jsonl`
  is introduced.

## Restore / Verification Commands

Representative tests:

```powershell
.\.venv\Scripts\python.exe -m pytest `
  tests\test_session_models.py `
  tests\test_session_service.py `
  tests\test_agent_runtime_session_integration.py `
  tests\test_session_context_history_adapter.py `
  tests\test_session_ocel_shape.py `
  tests\test_agent_runtime_ocel_shape.py `
  tests\test_process_run_loop.py `
  tests\test_ocel_store.py
```

Smoke scripts:

```powershell
.\.venv\Scripts\python.exe scripts\test_session_service.py
.\.venv\Scripts\python.exe scripts\test_session_runtime.py
```

## Operational Notes

Use OCEL queries or OCPX session views to inspect session/message persistence.
`AgentRunResult.metadata` contains IDs needed to follow the session, turn,
messages, and process instance.

## Remaining Limitations

- No memory layer yet.
- No Markdown materialized views yet.
- No hook lifecycle.
- No session resume/fork.
- No external artifact store for full message content.

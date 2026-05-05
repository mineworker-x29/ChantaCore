# ChantaCore v0.10.1 Restore

## Version

ChantaCore v0.10.1 - OCEL-native Memory & Instruction Substrate.

## Purpose

v0.10.1 adds OCEL-native memory and instruction persistence. The source of
truth for memory entries, revisions, instruction artifacts, project rules, and
user preferences remains OCEL event/object/relation records.

This release intentionally does not add Markdown materialized views, automatic
memory retrieval, embeddings, vector search, consolidation jobs, hooks,
permission grants, or session resume/fork.

## Memory Package

The release extends `src/chanta_core/memory/` with:

- `ids.py`
- `errors.py`
- `models.py`
- `service.py`
- `history_adapter.py`

Existing `MemoryRecord` and `MemoryStore` remain for compatibility, but they are
not canonical persistence.

The new OCEL-native memory package should be treated as the canonical path for
new memory facts. Compatibility classes may remain present, but restoration
should not wire new memory lifecycle behavior through a JSONL file or a Markdown
document.

## Instruction Package

The release adds `src/chanta_core/instructions/`:

- `__init__.py`
- `ids.py`
- `errors.py`
- `models.py`
- `service.py`
- `history_adapter.py`

## Memory Models

`MemoryEntry` fields:

- `memory_id`
- `memory_type`
- `title`
- `content`
- `content_preview`
- `content_hash`
- `status`
- `confidence`
- `created_at`
- `updated_at`
- `valid_from`
- `valid_until`
- `contradiction_status`
- `source_kind`
- `scope`
- `memory_attrs`

`MemoryRevision` fields:

- `revision_id`
- `memory_id`
- `revision_index`
- `operation`
- `before_hash`
- `after_hash`
- `content_preview`
- `content_hash`
- `reason`
- `created_at`
- `actor_type`
- `revision_attrs`

`hash_content(text)` uses SHA-256. `preview_text(...)` creates deterministic
local previews.

Memory content may be stored in local OCEL object attributes in v0.10.1. That is
a local-development persistence choice, not a permanent content-addressed
artifact design. The important invariant is that the object includes
`content_preview` and `content_hash` so a later artifact store can move large
content without changing the memory identity model.

## Instruction Models

`InstructionArtifact` records instruction bodies and metadata:

- instruction type/title/body/body preview/body hash
- status, scope, priority
- source path
- attrs

`ProjectRule` records project-level rules:

- rule ID/type/text/status/priority
- source instruction ID
- attrs

`UserPreference` records preference key/value facts:

- preference ID/key/value/status
- confidence
- source kind
- attrs

Instruction and preference models deliberately separate body/text/value from
status and source metadata. That keeps future deprecation, revision, and staged
assimilation workflows from rewriting historical facts in place.

## Services

`MemoryService` methods:

- `create_memory_entry(...)`
- `revise_memory_entry(...)`
- `supersede_memory_entry(...)`
- `archive_memory_entry(...)`
- `withdraw_memory_entry(...)`
- `attach_memory_to_session(...)`
- `attach_memory_to_turn(...)`

`InstructionService` methods:

- `register_instruction_artifact(...)`
- `revise_instruction_artifact(...)`
- `deprecate_instruction_artifact(...)`
- `register_project_rule(...)`
- `revise_project_rule(...)`
- `register_user_preference(...)`
- `revise_user_preference(...)`

Both services write OCEL records through `TraceService.record_session_ocel_record`.
Neither service creates a canonical JSONL or Markdown store.

For v0.10.1, service methods accept provided session, turn, and message IDs as
source references. They do not search previous conversations, infer preferences,
or retrieve candidate memories automatically. If a caller wants to derive memory
from a message, it must call the service explicitly with the relevant IDs.

## OCEL Object Types

The release actively uses:

- `memory_entry`
- `memory_revision`
- `instruction_artifact`
- `project_rule`
- `user_preference`

Object attrs include content/body previews and hashes, full local content/body
for development, status, scope/source fields, and extension attrs.

## OCEL Event Activities

Memory events:

- `memory_entry_created`
- `memory_entry_revised`
- `memory_entry_superseded`
- `memory_entry_archived`
- `memory_entry_withdrawn`
- `memory_revision_recorded`
- `memory_derived_from_message`
- `memory_attached_to_session`
- `memory_attached_to_turn`

Instruction events:

- `instruction_artifact_registered`
- `instruction_artifact_revised`
- `instruction_artifact_deprecated`
- `project_rule_registered`
- `project_rule_revised`
- `user_preference_registered`
- `user_preference_revised`

Best-effort event-object and object-object relations preserve links to sessions,
turns, messages, instructions, rules, and revisions where IDs are provided.

Expected object/relation intent:

- `memory_revision` revises `memory_entry`;
- `memory_entry` can be derived from `message`, `conversation_turn`, or
  `session` when source IDs are supplied;
- `memory_entry` can supersede another `memory_entry`;
- `project_rule` can be derived from `instruction_artifact`;
- `instruction_artifact` can define `project_rule`;
- `user_preference` can be derived from message/session context.

If object-object relation helper APIs are limited, event-object relations must
still preserve enough IDs to reconstruct these links.

## Context History Adapters

Memory adapter:

- `memory_entries_to_history_entries(...)`

Instruction adapters:

- `instruction_artifacts_to_history_entries(...)`
- `project_rules_to_history_entries(...)`
- `user_preferences_to_history_entries(...)`

Adapters operate on provided objects only. They do not perform automatic OCEL
retrieval.

The adapter priority policy is intentionally simple:

- active memory/instruction/preference facts project at useful context priority;
- draft facts project at lower priority;
- superseded, archived, withdrawn, or deprecated facts are skipped or projected
  as low-priority context according to the adapter, but are not deleted.

This is prompt-context projection. It is not memory retrieval, ranking, or
consolidation.

## PIG/OCPX Reporting

`PIGReportService` includes lightweight memory/instruction summary counts in
`report_attrs["memory_instruction_summary"]` and report text:

- memory entry count
- memory revision count
- instruction artifact count
- project rule count
- user preference count
- memory event count
- instruction event count

This is count/report support only, not semantic retrieval.

The report support is useful for sanity checks after service operations. A
minimal healthy run should show non-zero counts for the object types and event
families that were exercised by tests or scripts, but the exact counts depend on
the test fixture and are not a release invariant.

## Boundaries

v0.10.1 does not:

- create `.chanta/MEMORY.md`, `.chanta/PROJECT.md`, or `.chanta/USER.md`
- create canonical JSONL memory/instruction stores
- implement automatic retrieval
- implement embeddings or vector DB
- implement memory consolidation
- implement hooks, permission grants, resume/fork, MCP, plugins, or UI

The release also avoids reverse import behavior. There is no Markdown file whose
edits are read back into OCEL as canonical facts, and no JSONL memory file that
acts as a source of truth.

## Restore Checklist

Use this checklist when rebuilding or auditing the release:

- `src/chanta_core/memory/` contains ID helpers, errors, models, service, and
  history adapter.
- `src/chanta_core/instructions/` contains ID helpers, errors, models, service,
  and history adapter.
- `MemoryEntry` includes content, preview, hash, status, confidence,
  contradiction status, validity fields, source kind, scope, and attrs.
- `MemoryRevision` includes memory ID, operation, before/after hashes, preview,
  hash, reason, actor type, and attrs.
- `InstructionArtifact`, `ProjectRule`, and `UserPreference` expose `to_dict()`
  and include status plus extension attrs.
- Memory events include create, revise, supersede, archive, withdraw, revision
  recorded, derived from message, attached to session, and attached to turn.
- Instruction events include artifact register/revise/deprecate, project rule
  register/revise, and user preference register/revise.
- Context history adapters exist but do not load from OCEL automatically.
- PIG report attrs include lightweight memory/instruction summary counts.
- No `.chanta/*.md` materialized views are created in this release.
- No canonical `memory.jsonl`, `instructions.jsonl`, `preferences.jsonl`, or
  similar JSONL store is introduced.

## Restore / Verification Commands

Representative tests:

```powershell
.\.venv\Scripts\python.exe -m pytest `
  tests\test_memory_models.py `
  tests\test_instruction_models.py `
  tests\test_memory_service.py `
  tests\test_instruction_service.py `
  tests\test_memory_context_history_adapter.py `
  tests\test_instruction_context_history_adapter.py `
  tests\test_memory_instruction_ocel_shape.py `
  tests\test_pig_reports.py
```

Smoke scripts:

```powershell
.\.venv\Scripts\python.exe scripts\test_memory_service.py
.\.venv\Scripts\python.exe scripts\test_instruction_service.py
```

## Operational Notes

Use OCEL store queries for canonical inspection. Use history adapters only when
explicitly projecting provided memory/instruction objects into prompt context.

## Remaining Limitations

- No Markdown materialized views yet.
- No automatic memory retrieval.
- No embeddings or vector DB.
- No memory consolidation job.
- No hook lifecycle.
- No permission/grant model.
- No session resume/fork.

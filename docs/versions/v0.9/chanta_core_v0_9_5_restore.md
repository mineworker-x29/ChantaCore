# ChantaCore v0.9.5 Restore

## Version

ChantaCore v0.9.5 - Context Assembly Snapshot & Prompt Audit.

## Purpose

v0.9.5 adds optional prompt assembly snapshots so operators can inspect what
context blocks were assembled, what compaction did, what messages were finally
rendered, and which refs point back to raw artifacts. Snapshots are for
debugging, audit, and replay support. They are not OCEL storage and are not a
replacement for raw PIG/tool/report/session data.

The privacy boundary is important: snapshot capture is disabled by default and
does not blindly persist full prompt text.

## Added Files

This release adds:

- `src/chanta_core/context/snapshot.py`
- `src/chanta_core/context/snapshot_policy.py`
- `src/chanta_core/context/snapshot_store.py`
- `src/chanta_core/context/redaction.py`
- `src/chanta_core/context/audit.py`

It updates:

- `src/chanta_core/context/__init__.py`
- `src/chanta_core/runtime/loop/context.py`
- `src/chanta_core/runtime/loop/policy.py`
- `src/chanta_core/runtime/loop/process_run_loop.py`
- `src/chanta_core/skills/builtin/llm_chat.py`
- `tests/test_imports.py`

## Snapshot Models

`ContextBlockSnapshot` records block metadata only:

- block ID/type/title/source/priority
- char length and token estimate
- truncated/dropped/collapsed flags
- refs
- snapshot attrs

It does not store raw block content.

`ContextMessageSnapshot` records:

- role
- optional content preview
- char length
- token estimate
- message attrs

`ContextAssemblySnapshot` records:

- snapshot ID
- session and process IDs
- created timestamp
- storage mode
- budget snapshot
- block snapshots
- message snapshots
- optional compaction result
- warnings
- snapshot attrs

## Snapshot Policy

`ContextSnapshotPolicy` controls capture:

- `enabled=False` by default
- `storage_mode="preview"` by default
- `max_preview_chars`
- `redact_sensitive`
- `include_block_refs`
- `include_compaction_result`

Supported storage modes:

- `metadata_only`
- `preview`
- `full`

Full prompt capture is never enabled by default.

## Redaction

`redact_sensitive_text(...)` provides simple deterministic redaction for obvious
secret-like values:

- `API_KEY`
- `SECRET`
- `TOKEN`
- `PASSWORD`
- `PRIVATE_KEY`
- `ACCESS_KEY`
- bearer tokens
- PEM private key blocks
- long token-like strings

`make_preview(...)` redacts first, then truncates with
`...[preview truncated]...`.

This is not a complete secret scanner. It is a lightweight guardrail.

## Snapshot Store

`ContextSnapshotStore` is an append-only JSONL debug store at
`data/context/context_snapshots.jsonl` by default. `data/` is ignored by git.
This is not canonical persistence. Invalid JSONL rows are skipped with warnings
instead of crashing.

Methods:

- `append(snapshot)`
- `load_all()`
- `recent(limit)`
- `get(snapshot_id)`

## ContextAuditService

`ContextAuditService` builds and optionally stores snapshots. It honors snapshot
policy:

- `metadata_only` stores no message content preview
- `preview` stores redacted/truncated previews
- `full` stores full content only if explicitly requested, redacted by default

The service does not mutate blocks or messages and does not call an LLM.

## Runtime Integration

`ProcessContextAssembler.assemble_for_llm_chat(...)` accepts optional:

- `context_snapshot_policy`
- `context_snapshot_store`
- `context_audit_service`
- `session_id`
- `process_instance_id`

Return type remains `list[ChatMessage]`. `ProcessContextAssembler.last_snapshot`
is available for inspection. If snapshot policy is disabled, legacy behavior is
unchanged.

`ProcessRunPolicy` adds optional snapshot fields:

- `enable_context_snapshot=False`
- `context_snapshot_policy=None`

ProcessRunLoop only passes snapshot policy when explicitly enabled.

## Boundaries

v0.9.5 does not:

- enable snapshots by default
- persist full prompt text by default
- store raw block content in block snapshots
- delete or mutate raw OCEL/PIG/tool/report data
- call an LLM
- add semantic compaction
- add external dependencies, async, UI, MCP, plugins, or connectors

## Restore / Verification Commands

Representative tests:

```powershell
.\.venv\Scripts\python.exe -m pytest `
  tests\test_context_redaction.py `
  tests\test_context_snapshot_models.py `
  tests\test_context_snapshot_policy.py `
  tests\test_context_snapshot_store.py `
  tests\test_context_audit_service.py `
  tests\test_process_context_snapshot_integration.py `
  tests\test_process_run_loop_context_snapshot.py
```

Smoke scripts:

```powershell
.\.venv\Scripts\python.exe scripts\test_context_snapshot.py
.\.venv\Scripts\python.exe scripts\inspect_context_snapshots.py
```

## Operational Notes

Use preview snapshots for debugging prompt assembly. Treat snapshot JSONL as a
debug mirror only. If full mode is enabled for a controlled local investigation,
review redaction limitations and remove generated files when no longer needed.

## Remaining Limitations

- No full prompt audit enabled by default.
- No advanced secret scanner.
- No UI viewer.
- No mandatory OCEL event linkage.
- No semantic compaction.

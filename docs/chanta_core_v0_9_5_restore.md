# ChantaCore v0.9.5 Restore Notes

ChantaCore v0.9.5 adds context assembly snapshot and prompt audit support for the v0.9.x context budget phase.

## Scope

- `ContextAssemblySnapshot`, `ContextBlockSnapshot`, and `ContextMessageSnapshot` record prompt-facing assembly metadata.
- `ContextSnapshotPolicy` controls whether snapshots are captured and how much message text is retained.
- `ContextSnapshotStore` writes append-only JSONL records under `data/context/`.
- `ContextAuditService` builds snapshots without mutating blocks, messages, OCEL, PIG, tool, or report stores.
- `ProcessContextAssembler` can optionally store a snapshot and exposes the last generated snapshot for tests/debugging.

## Privacy Defaults

Snapshots are disabled by default. If enabled without overriding the mode, the default storage mode is `preview`, not full prompt storage.

Block snapshots store metadata and references only; they do not store raw block content. Message previews are redacted for obvious sensitive values such as API keys, secrets, bearer tokens, passwords, access keys, and PEM private key blocks.

## Non-Goals

- No LLM calls are used.
- No semantic compaction is implemented.
- No tokenizer dependency is added.
- No UI or external connector is added.
- No raw OCEL/PIG/tool/report data is deleted or mutated.

## Future Work

- Full prompt audit remains opt-in and should stay off by default.
- Redaction is intentionally simple and is not a complete secret scanner.
- A UI snapshot viewer is not included.
- OCEL event linkage for snapshots is not required in this version.
- Semantic compaction remains outside v0.9.5.

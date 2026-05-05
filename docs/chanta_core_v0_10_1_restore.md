# ChantaCore v0.10.1 Restore Notes

ChantaCore v0.10.1 adds an OCEL-native memory and instruction substrate.

## Scope

- `MemoryEntry` and `MemoryRevision` model local memory facts and their revisions.
- `InstructionArtifact`, `ProjectRule`, and `UserPreference` model durable instruction and preference facts.
- `MemoryService` records memory lifecycle events through OCEL event/object/relation records.
- `InstructionService` records instruction, project rule, and user preference lifecycle events through OCEL.
- Context history adapters can project provided memory/instruction objects into prompt-facing `ContextHistoryEntry` values.
- PIG reports include lightweight counts for memory, memory revisions, instruction artifacts, project rules, user preferences, and related event counts.

## Persistence Rule

Memory and instruction persistence is OCEL-based. No canonical JSONL memory or instruction store is introduced. Markdown materialized views are not implemented in v0.10.1.

## Non-Goals

- No `.chanta/MEMORY.md`, `.chanta/PROJECT.md`, or `.chanta/USER.md`.
- No automatic memory retrieval.
- No embeddings or vector database.
- No memory consolidation scheduler.
- No hook lifecycle.
- No permission or grant model.
- No session resume/fork.
- No external connector, MCP, plugin, or marketplace feature.

## Future Work

- v0.10.2 Markdown materialized views.
- v0.10.3 hook lifecycle observability.
- v0.10.4 session resume/fork.
- v0.10.5 file-based tool registry / policy view.

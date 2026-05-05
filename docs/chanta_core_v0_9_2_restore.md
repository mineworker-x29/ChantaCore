# ChantaCore v0.9.2 Restore Notes

ChantaCore v0.9.2 strengthens deterministic microcompaction and structured context rendering. It builds on the five-layer context pipeline and the v0.9.1 session/history snip policy.

Microcompact remains deterministic, local, and non-semantic. It does not call an LLM, does not create learned summaries, and does not delete raw source data. It only changes prompt-facing `ContextBlock` projection.

This release adds deterministic utilities for compacting long lines, long line lists, activity sequences, mappings, JSON-like text, and report-like text. `MicrocompactPolicy` controls bounded local compaction. `MicrocompactLayer` now uses block type hints for PIG context, PIG reports, tool results, decision/conformance blocks, workspace/repo listings, worker/scheduler lists, and artifacts.

PIG context, process reports, tool results, and PI artifacts can carry structured block attributes so prompt context can be rendered more compactly without losing durable raw state. `ContextRenderer` now includes concise metadata and limited refs while avoiding large `block_attrs` dumps.

Future work:

- semantic auto-compact
- tokenizer-based token count
- learned context ranking
- context collapse improvements
- subagent context isolation

# ChantaCore v0.9.1 Restore Notes

ChantaCore v0.9.1 strengthens prompt-facing context snipping with session and history policy. It builds on the v0.9.0 context budget and five-layer compaction foundation without changing OCEL/OCPX/PIG persistence semantics.

Snip is a projection operation only. It affects which `ContextBlock` objects are rendered into prompt context. It does not delete OCEL records, PIG artifacts, PIArtifact records, tool results, ProcessRun reports, worker records, scheduler records, or job records.

The new policy foundation includes:

- `ContextHistoryEntry`
- `ContextHistoryPolicy`
- `SessionContextPolicy`
- `ContextHistoryBuilder`
- session/history-aware `SnipLayer`

System prompt and current user request blocks remain protected. Recent user and assistant history can be preserved according to `ContextHistoryPolicy`. Current session and process blocks can be protected according to `SessionContextPolicy` and priority thresholds. Older and lower-priority history is removed from prompt-facing context first when the budget is under pressure.

LLM semantic compaction is still not implemented. No LLM is called to summarize history. `AutoCompactLayer` remains present and disabled by default.

Remaining limitations:

- no persistent conversation history store yet
- no semantic auto-compact
- no tokenizer-based token counting
- no learned history selection
- no subagent context isolation

# ChantaCore v0.9.0 Restore Notes

ChantaCore v0.9.0 introduces the five-layer context compaction foundation for prompt/context budget control. The design is inspired by Claude Code context pressure handling: the context window is treated as the binding resource, oversized tool outputs are reduced before heavier compaction, raw durable state stays outside the prompt, and the model receives compacted context blocks.

The full architecture now exists:

- BudgetReductionLayer
- SnipLayer
- MicrocompactLayer
- ContextCollapseLayer
- AutoCompactLayer

v0.9.0 implements only deterministic and lightweight behavior. Budget reduction truncates oversized blocks by type-specific character caps. Snip drops low-priority unprotected blocks when total context exceeds the usable budget. Microcompact removes repeated blank lines, strips trailing whitespace, truncates very long lines, and applies a deterministic first/last line strategy for long lists. ContextCollapse creates a compact reference block for omitted low-priority blocks. AutoCompact exists as a disabled stub by default.

No LLM semantic compaction is implemented in this version. Compaction does not call an LLM and does not add tokenizer-based counting. Raw artifacts and source-store data remain preserved; only prompt/context blocks are reduced before injection.

Future work:

- semantic auto-compact
- tokenizer-based counting
- session history snip
- context collapse with learned summaries
- subagent context isolation

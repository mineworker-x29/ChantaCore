# ChantaCore v0.9.4 Restore Notes

ChantaCore v0.9.4 hardens AutoCompact guardrails and adds deterministic compaction readiness/reporting.

AutoCompact remains disabled by default. No LLM semantic compaction is implemented, no production LLM summarizer is provided, and no compaction path calls an LLM. The new `AutoCompactPolicy` defaults to `enabled=False` and `allow_llm_summarizer=False`.

This release adds:

- `AutoCompactPolicy`
- `AutoCompactRequest`
- `AutoCompactResult`
- `AutoCompactSummarizer` interface
- `ContextCompactionReadinessChecker`
- `ContextCompactionReporter`

`AutoCompactLayer` refuses unsafe execution when AutoCompact is enabled without the allow flag, when no summarizer is provided, when input is too large, when output is too large, or when references are not preserved. Tests use only a fake deterministic summarizer to verify the interface.

`ContextCompactionReadinessChecker` can recommend AutoCompact when deterministic layers are insufficient, but it does not run AutoCompact. `ContextCompactionReporter` produces concise operator-readable reports without dumping raw block content.

Remaining limitations:

- no real semantic summarizer
- no tokenizer-based token count
- no learned summary
- no automatic AutoCompact trigger
- no subagent context isolation

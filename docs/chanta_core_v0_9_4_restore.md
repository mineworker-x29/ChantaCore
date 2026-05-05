# ChantaCore v0.9.4 Restore

## Version

ChantaCore v0.9.4 - AutoCompact Guardrails & Compaction Readiness.

## Purpose

v0.9.4 hardens the fifth compaction layer without implementing semantic
compaction. AutoCompact remains a future interface, guarded so it cannot
accidentally call an LLM or external summarizer. The release also adds
readiness checks and operator-readable compaction reports so deterministic
layers can be evaluated before future semantic compaction is considered.

## Added Files

This release adds:

- `src/chanta_core/context/auto_compact.py`
- `src/chanta_core/context/readiness.py`
- `src/chanta_core/context/report.py`

It updates:

- `src/chanta_core/context/layers/auto_compact.py`
- `src/chanta_core/context/pipeline.py`
- `tests/test_imports.py`

## AutoCompactPolicy

`AutoCompactPolicy` defaults are intentionally safe:

- `enabled=False`
- `require_explicit_enable=True`
- `allow_llm_summarizer=False`

Additional limits:

- `max_input_chars`
- `max_output_chars`
- `preserve_refs`
- `policy_attrs`

Validation ensures positive limits and boolean guard flags.

## AutoCompact Request / Result

`AutoCompactRequest` is the future summarizer input container:

- `request_id`
- `blocks`
- `input_text`
- `refs`
- `reason`
- `request_attrs`

`AutoCompactResult` records:

- `success`
- `output_block`
- `output_text`
- `used_summarizer`
- `warnings`
- `error`
- `result_attrs`

No production LLM summarizer is implemented.

`AutoCompactSummarizer` is an interface only. Tests may use a fake deterministic
summarizer to verify guard behavior, but the runtime has no default summarizer.

## AutoCompactLayer Guardrails

`AutoCompactLayer` behavior:

1. If policy is disabled, return no-op with `result_attrs["disabled"] = True`.
2. If enabled but `allow_llm_summarizer=False`, do not run and return a warning.
3. If enabled but no summarizer is provided, do not run and return a warning.
4. If explicitly enabled, allowed, and provided a summarizer, enforce
   `max_input_chars` before calling it.

The default pipeline constructs `AutoCompactLayer` with a disabled policy.

## Readiness Checker

`ContextCompactionReadinessChecker.evaluate(...)` builds
`ContextCompactionReadiness` from a compaction result and budget. Status values:

- `ok`
- `warning`
- `over_budget`
- `unknown`

It computes:

- total chars/tokens
- budget snapshot
- layer summary
- truncated/dropped/collapsed counts
- remaining over-budget flag
- whether AutoCompact is recommended
- warnings

Recommendation is advisory only. It never triggers AutoCompact.

## Compaction Reporter

`ContextCompactionReporter.build_report(...)` creates
`ContextCompactionReport` with concise operator text:

- total chars/tokens
- usable budget
- per-layer changed status
- truncated/dropped/collapsed counts
- AutoCompact disabled/recommended status
- warnings

It does not dump block contents.

## Pipeline Integration

The default order remains:

1. `BudgetReductionLayer`
2. `SnipLayer`
3. `MicrocompactLayer`
4. `ContextCollapseLayer`
5. `AutoCompactLayer(enabled=False)`

The pipeline result includes the AutoCompact layer result, which should show it
is disabled by default.

## Boundaries

v0.9.4 does not:

- implement semantic auto-compact
- call an LLM for compaction
- add a production summarizer
- auto-trigger AutoCompact from readiness
- add tokenizer dependency
- delete raw source data
- add async, UI, MCP, plugins, or external connectors

## Restore / Verification Commands

Representative tests:

```powershell
.\.venv\Scripts\python.exe -m pytest `
  tests\test_auto_compact_policy.py `
  tests\test_auto_compact_models.py `
  tests\test_auto_compact_layer_guardrails.py `
  tests\test_context_compaction_readiness.py `
  tests\test_context_compaction_report.py `
  tests\test_pipeline_autocompact_safety.py `
  tests\test_context_layers_auto_compact.py
```

Smoke scripts:

```powershell
.\.venv\Scripts\python.exe scripts\test_autocompact_guardrails.py
.\.venv\Scripts\python.exe scripts\test_context_compaction_report.py
```

## Operational Notes

Use readiness/report output when deterministic compaction is not enough. The
correct v0.9.4 behavior is recommendation and visibility, not automatic LLM
summarization.

## Remaining Limitations

- No real semantic summarizer.
- No tokenizer-based token count.
- No learned summary.
- No automatic AutoCompact trigger.
- No subagent context isolation.

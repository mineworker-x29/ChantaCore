# ChantaCore v0.9.2 Restore

## Version

ChantaCore v0.9.2 - Deterministic Microcompact & Structured Context Rendering.

## Purpose

v0.9.2 strengthens the third compaction layer: `MicrocompactLayer`. The layer is
deterministic, local, and non-semantic. It does not call an LLM, does not create
a learned summary, and does not delete source data. It only changes prompt-facing
`ContextBlock` projections.

This release also improves structured rendering so PIG context, PIG reports,
tool results, decision blocks, workspace/repo listings, and artifact blocks can
be compacted and displayed more predictably.

## Added Files

New context utilities:

- `src/chanta_core/context/microcompact.py`
- `src/chanta_core/context/microcompact_policy.py`

Updated components:

- `src/chanta_core/context/layers/microcompact.py`
- `src/chanta_core/context/renderer.py`
- `src/chanta_core/context/pipeline.py`
- `src/chanta_core/context/adapters.py`
- relevant PIG/tool context block adapters

## Microcompact Utilities

`compact_lines(...)` preserves head/tail lines and inserts an omitted-line
marker when a block has too many lines.

`compact_long_line(...)` truncates a single overlong line with a deterministic
marker.

`compact_activity_sequence(...)` renders activity sequences as
`a -> b -> c`, preserving head/tail items for long sequences.

`compact_mapping(...)` sorts keys deterministically and renders only the first
configured number of items. Nested dict/list values are represented compactly
with their type/length rather than dumping huge raw JSON.

`compact_json_like_text(...)` attempts `json.loads`; if the input is valid JSON,
it renders a deterministic compact representation. Invalid JSON falls back to
line/long-line compaction.

`compact_report_text(...)` preserves section headers and first lines of sections
while enforcing a character cap.

No external dependency is used.

## MicrocompactPolicy

`MicrocompactPolicy` controls:

- `max_lines`
- `max_line_chars`
- `max_activity_items`
- `max_mapping_items`
- `max_report_chars`
- `max_json_chars`
- `preserve_refs`

Validation requires positive limits and a boolean `preserve_refs`.

## MicrocompactLayer Behavior

The layer now applies block-type-specific deterministic policies:

- `pig_context`: compact activity sequences and report-like text.
- `pig_report`: use report compaction.
- `tool_result`: compact JSON-like text when possible; otherwise compact lines.
- `conformance`: preserve status/issue count and compact long issue lists.
- `decision`: preserve selected skill/mode/guidance hints and compact long score maps.
- `workspace` / `repo`: compact long file or match listings.
- `worker` / `scheduler`: compact long job/schedule lists.
- `artifact`: compact content while preserving identifying attrs.

Refs and block attrs are preserved. The layer result records
`microcompacted_block_count`, block type counts, and policy details.

## Structured Rendering

`ContextRenderer` now renders:

- `[block_type] title` header
- compact metadata line
- truncation/compaction marker
- concise refs limited by policy

It deliberately avoids dumping large `block_attrs` blobs.

## Pipeline Integration

The default pipeline order remains:

1. `BudgetReductionLayer`
2. `SnipLayer`
3. `MicrocompactLayer`
4. `ContextCollapseLayer`
5. `AutoCompactLayer(enabled=False)`

System prompts and user requests remain protected by the snip layer and are not
removed by microcompaction.

## Boundaries

v0.9.2 does not:

- implement semantic summarization
- call an LLM for compaction
- add tokenizer-based counting
- add external dependencies
- delete raw source data
- add async, UI, MCP, plugins, or external connectors

## Restore / Verification Commands

Representative tests:

```powershell
.\.venv\Scripts\python.exe -m pytest `
  tests\test_microcompact_utils.py `
  tests\test_microcompact_policy.py `
  tests\test_microcompact_layer_structured.py `
  tests\test_context_renderer_structured.py `
  tests\test_context_pipeline_microcompact_integration.py `
  tests\test_process_context_microcompact_integration.py
```

Smoke scripts:

```powershell
.\.venv\Scripts\python.exe scripts\test_microcompact.py
.\.venv\Scripts\python.exe scripts\test_context_compaction.py
```

## Operational Notes

Use `ContextCompactionResult.layer_results` to confirm `MicrocompactLayer`
changed blocks and did not drop protected context. If a block still exceeds
budget after microcompaction, later collapse may replace it with references.

## Remaining Limitations

- No semantic auto-compact.
- No tokenizer-based token count.
- No learned ranking.
- No context collapse semantic summary.
- No subagent context isolation.

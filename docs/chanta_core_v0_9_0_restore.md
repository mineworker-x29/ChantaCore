# ChantaCore v0.9.0 Restore

## Version

ChantaCore v0.9.0 - Context Budget & Five-Layer Compaction Foundation.

## Purpose

v0.9.0 introduces the prompt-facing context budget substrate. Before this
release, ChantaCore could generate many durable context-bearing artifacts:
PIG context, PIG reports, PI artifacts, tool results, repository/workspace
inspection outputs, conformance reports, decision diagnostics, worker and
scheduler reports, edit proposals, and patch reports. Those artifacts remain
durable source data, but they cannot all be injected into an LLM prompt without
budget control.

The design treats the context window as a binding runtime resource. Durable
state stays in source stores such as OCEL/PIG/tool/report stores, while the
prompt receives compacted `ContextBlock` projections. Claude Code's context
pressure handling was used as architectural inspiration, but v0.9.0 remains
fully deterministic and local.

## Package Layout

The release adds the context package:

- `src/chanta_core/context/block.py`
- `src/chanta_core/context/budget.py`
- `src/chanta_core/context/result.py`
- `src/chanta_core/context/pipeline.py`
- `src/chanta_core/context/renderer.py`
- `src/chanta_core/context/errors.py`
- `src/chanta_core/context/layers/base.py`
- `src/chanta_core/context/layers/budget_reduction.py`
- `src/chanta_core/context/layers/snip.py`
- `src/chanta_core/context/layers/microcompact.py`
- `src/chanta_core/context/layers/context_collapse.py`
- `src/chanta_core/context/layers/auto_compact.py`

The package is exported through `src/chanta_core/context/__init__.py` and is
imported by runtime context assembly.

## Core Models

`ContextBlock` is the prompt-facing unit of context. It carries:

- `block_id`
- `block_type`
- `title`
- `content`
- `priority`
- `source`
- `token_estimate`
- `char_length`
- `was_truncated`
- `refs`
- `block_attrs`

`estimate_tokens(text)` deliberately uses a deterministic heuristic:
`max(1, len(text) // 4)`. No tokenizer dependency is introduced.

`ContextBudget` defines both global and per-block character budgets:

- `max_total_chars`
- `max_total_estimated_tokens`
- `max_block_chars`
- `max_tool_result_chars`
- `max_pig_context_chars`
- `max_report_chars`
- `max_artifact_chars`
- `max_workspace_chars`
- `max_repo_chars`
- `reserve_chars`

`usable_chars()` returns `max_total_chars - reserve_chars`.

`ContextCompactionLayerResult` records per-layer changed/truncated/dropped/
created IDs and warnings. `ContextCompactionResult` records final blocks,
aggregate totals, warnings, and layer results.

## Five-Layer Pipeline

`ContextCompactionPipeline.default()` runs layers in this order:

1. `BudgetReductionLayer`
2. `SnipLayer`
3. `MicrocompactLayer`
4. `ContextCollapseLayer`
5. `AutoCompactLayer(enabled=False)`

This order matters. Oversized individual blocks are reduced first, low-priority
blocks are snipped next, deterministic microcompaction is applied after the
coarsest reductions, collapse creates compact references if still needed, and
AutoCompact remains a disabled stub.

## Layer Behavior

`BudgetReductionLayer` applies block-type-specific character caps. It truncates
with a deterministic marker, preserves refs, sets `was_truncated=True`, and
recomputes character/token estimates.

`SnipLayer` drops low-priority blocks when the total prompt projection exceeds
`ContextBudget.usable_chars()`. `system` and `user_request` blocks are protected
unless the budget is impossible. It records dropped block IDs and warnings.

`MicrocompactLayer` in v0.9.0 performs only lightweight deterministic cleanup:
repeated blank line removal, trailing whitespace stripping, long-line truncation,
and first/last line preservation for long lists.

`ContextCollapseLayer` creates a deterministic reference block when low-priority
blocks must be omitted. Raw content is not included in the collapsed block.

`AutoCompactLayer` exists, but is disabled by default. v0.9.0 does not implement
semantic auto-compaction and does not call an LLM.

## Adapters and Runtime Integration

PIG context and selected runtime artifacts can become `ContextBlock` values.
The v0.9.0 integration focuses on:

- `PIGContext.to_context_block(...)`
- `ToolResult.to_context_block(...)` or adapter equivalents
- `ProcessRunReport.to_context_block(...)` or adapter equivalents
- `ProcessContextAssembler.assemble_for_llm_chat(...)`

`ProcessContextAssembler` accepts optional `context_budget`,
`compaction_pipeline`, and `extra_blocks`. If no budget and no extra blocks are
provided, the legacy assembly behavior is preserved.

`ProcessRunPolicy` supports optional context budget use. `ProcessRunLoop` passes
the budget into runtime context assembly where configured.

## Renderer

`ContextRenderer` renders compacted blocks with:

- `[block_type] title` header
- compact block content
- truncation marker when relevant
- concise refs section

The renderer is not a persistence layer. It only materializes a prompt-facing
string from `ContextBlock` values.

## Boundaries

v0.9.0 does not:

- call an LLM for compaction
- implement semantic summarization
- add tokenizer-based counting
- delete OCEL/PIG/tool/report raw data
- introduce external dependencies
- add async, UI, MCP, plugins, or external connectors

The raw durable state remains in its source stores. Compaction only affects the
prompt projection.

## Restore / Verification Commands

Representative tests for this release:

```powershell
.\.venv\Scripts\python.exe -m pytest `
  tests\test_context_block.py `
  tests\test_context_budget.py `
  tests\test_context_layers_budget_reduction.py `
  tests\test_context_layers_snip.py `
  tests\test_context_layers_microcompact.py `
  tests\test_context_layers_collapse.py `
  tests\test_context_layers_auto_compact.py `
  tests\test_context_pipeline.py `
  tests\test_context_renderer.py `
  tests\test_pig_context_block.py `
  tests\test_process_context_budget_integration.py `
  tests\test_process_run_loop_context_budget.py
```

Smoke scripts:

```powershell
.\.venv\Scripts\python.exe scripts\test_context_compaction.py
.\.venv\Scripts\python.exe scripts\test_process_run_loop_context_budget.py
```

## Operational Notes

Use this release when prompt injection pressure comes from large tool outputs,
PIG context, or report artifacts. The expected recovery path is to re-run
context assembly with a conservative `ContextBudget`, inspect the
`ContextCompactionResult.layer_results`, and verify that `system` and
`user_request` blocks were preserved.

## Remaining Limitations

- No semantic auto-compact.
- No tokenizer-based token counting.
- No session history policy yet.
- No learned summary or learned ranking.
- No subagent context isolation.

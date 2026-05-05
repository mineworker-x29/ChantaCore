# ChantaCore v0.9.3 Restore

## Version

ChantaCore v0.9.3 - Deterministic Context Collapse & Reference Projection.

## Purpose

v0.9.3 strengthens `ContextCollapseLayer`. Collapse is deterministic reference
projection, not summarization. When prompt budget pressure remains after budget
reduction, snip, and microcompact, low-priority blocks can be removed from the
prompt and represented by a compact manifest of references.

The critical boundary is that raw content remains in source stores. Collapsed
context blocks contain metadata and references only.

## Added Files

This release adds:

- `src/chanta_core/context/references.py`
- `src/chanta_core/context/collapse_policy.py`
- `src/chanta_core/context/collapse.py`

It updates:

- `src/chanta_core/context/layers/context_collapse.py`
- `src/chanta_core/context/renderer.py`
- `src/chanta_core/context/pipeline.py`
- `tests/test_imports.py`

## ContextReference

`ContextReference` is a compact pointer to source material. It carries:

- `ref_id`
- `ref_type`
- `source`
- `title`
- `block_id`
- `object_id`
- `event_id`
- `artifact_id`
- `path`
- `attrs`

Reference types include context blocks, OCEL events/objects, PI artifacts, PIG
reports, tool results, workspace files, repo matches, worker jobs, scheduler
schedules, edit proposals, patch applications, and `other`.

`ContextReference` does not store raw collapsed content.

## ContextCollapsePolicy

`ContextCollapsePolicy` controls:

- whether collapse is enabled
- minimum number of blocks to collapse
- max collapsed block chars
- max references
- grouping by block type
- whether titles/sources/ref counts are included
- priority for the collapsed block

Default policy is enabled and deterministic.

## CollapsedContextManifest

`CollapsedContextManifest` records:

- `manifest_id`
- `collapsed_block_count`
- `collapsed_by_type`
- `references`
- `created_at`
- `manifest_attrs`

`to_context_block(...)` creates a `ContextBlock` with:

- `block_type="collapsed_context"`
- title `Collapsed Context References`
- content stating that raw content is preserved in source stores
- refs derived from `ContextReference`
- attrs including manifest ID and collapsed counts

## ContextCollapseLayer Behavior

When total context is within budget, the layer is a no-op.

When over budget, candidates are selected from non-protected blocks. Protected
block types are:

- `system`
- `user_request`

Collapsible block types include tool results, PIG reports, artifacts, workspace
and repo blocks, worker/scheduler blocks, edit/patch blocks, old history, old
decisions, and old conformance blocks.

Candidate ordering is deterministic: low priority first, with timestamp/order
fallbacks where available. The layer drops enough blocks to fit, creates a
manifest, and tries to add the collapsed context block. If the manifest block is
too large, it is reduced; if it still cannot fit, it is dropped with a warning.

Layer result attrs include:

- `collapsed_block_count`
- `collapsed_by_type`
- `manifest_id`
- `reference_count`

## Renderer Support

`ContextRenderer` renders `collapsed_context` blocks clearly, including:

- collapsed block count
- grouped type counts
- limited references
- the raw-content preservation statement

It does not dump collapsed raw content.

## Pipeline Integration

The default order remains:

1. `BudgetReductionLayer`
2. `SnipLayer`
3. `MicrocompactLayer`
4. `ContextCollapseLayer`
5. `AutoCompactLayer(enabled=False)`

`ContextCollapseLayer` appears in `ContextCompactionResult.layer_results`, and
warnings are aggregated into the pipeline result.

## Boundaries

v0.9.3 does not:

- perform semantic summarization
- call an LLM
- delete raw source data
- mutate OCEL/PIG/tool/report stores
- enable AutoCompact
- add tokenizer, external dependencies, async, UI, MCP, plugins, or connectors

## Restore / Verification Commands

Representative tests:

```powershell
.\.venv\Scripts\python.exe -m pytest `
  tests\test_context_references.py `
  tests\test_context_collapse_policy.py `
  tests\test_collapsed_context_manifest.py `
  tests\test_context_collapse_layer.py `
  tests\test_context_renderer_collapse.py `
  tests\test_context_pipeline_collapse_integration.py `
  tests\test_process_context_collapse_integration.py
```

Smoke scripts:

```powershell
.\.venv\Scripts\python.exe scripts\test_context_collapse.py
.\.venv\Scripts\python.exe scripts\test_context_compaction.py
```

## Operational Notes

When investigating prompt omissions, inspect `ContextCollapseLayer.result_attrs`
and the `collapsed_context` block refs. The raw omitted blocks should not appear
in rendered prompt content, but their source pointers should remain visible.

## Remaining Limitations

- No semantic collapse.
- No auto-compact execution.
- No tokenizer-based budget.
- No learned reference ranking.
- No subagent context isolation.

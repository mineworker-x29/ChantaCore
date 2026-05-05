# ChantaCore v0.9.1 Restore

## Version

ChantaCore v0.9.1 - Context History Snip & Session Context Policy.

## Purpose

v0.9.1 strengthens the prompt-facing snip policy introduced in v0.9.0. The key
rule is that context snipping is not persistence. OCEL/OCPX/PIG source records,
tool results, process reports, worker jobs, scheduler records, and artifacts
remain durable. Snip only changes the context projection that is rendered into a
prompt.

This release adds a session/history policy layer so old or low-priority
conversation history can be omitted deterministically while current system,
user, session, and process context remains protected.

## Added Files

The release adds:

- `src/chanta_core/context/history.py`
- `src/chanta_core/context/policy.py`
- `src/chanta_core/context/history_builder.py`

It updates:

- `src/chanta_core/context/layers/snip.py`
- `src/chanta_core/context/pipeline.py`
- `src/chanta_core/runtime/loop/context.py`
- `tests/test_imports.py`

## Context History Model

`ContextHistoryEntry` represents a prompt-facing history item, not a persistent
history store. It carries:

- `entry_id`
- `session_id`
- `process_instance_id`
- `role`
- `content`
- `created_at`
- `source`
- `priority`
- `refs`
- `entry_attrs`

`history_entry_to_context_block(...)` converts history entries into
`ContextBlock` values. Mapping is role-aware:

- user history can become `user_request`
- assistant history becomes history/context content
- tool history can become `tool_result`
- PIG history can become `pig_context`

The helper preserves refs and records `session_id`, `process_instance_id`,
`created_at`, and source in `block_attrs`.

## Policy Models

`ContextHistoryPolicy` defines deterministic history selection controls:

- `max_history_blocks`
- `max_recent_history_blocks`
- `preserve_last_user_blocks`
- `preserve_last_assistant_blocks`
- `preserve_current_process_blocks`
- `preserve_current_session_blocks`
- `min_priority_to_keep`
- `history_block_priority_decay`

`SessionContextPolicy` ties the policy to an active session/process context:

- `session_id`
- `process_instance_id`
- `include_history`
- `include_pig_context`
- `include_reports`
- `include_tool_results`
- `history_policy`

These are prompt/context policies, not storage policies.

## History Builder

`ContextHistoryBuilder` provides:

- `build_from_entries(entries)`
- `build_recent_history_blocks(entries, session_policy=...)`

It filters deterministically by session/process where configured, respects
`include_history=False`, converts entries into blocks, and sorts by
`created_at` then entry ID. It does not mutate entries and does not load history
from a persistent store.

## Session-Aware SnipLayer

`SnipLayer` now accepts optional `ContextHistoryPolicy` and protected block
types. Default protected types remain:

- `system`
- `user_request`

Additional protection applies to current session/process blocks and recent
user/assistant history according to policy. If the budget is exceeded, the layer
drops lower-priority history/tool/report/artifact blocks first. Older history
drops before newer history on priority ties. Dropped IDs and reason metadata are
reported in the layer result.

## Pipeline Integration

`ContextCompactionPipeline.default(...)` can configure `SnipLayer` with session
policy while preserving the default order:

1. `BudgetReductionLayer`
2. `SnipLayer`
3. `MicrocompactLayer`
4. `ContextCollapseLayer`
5. `AutoCompactLayer(enabled=False)`

AutoCompact remains disabled. No semantic LLM summarization is introduced.

## ProcessContextAssembler Integration

`ProcessContextAssembler.assemble_for_llm_chat(...)` accepts:

- `history_entries`
- `session_context_policy`

History is optional. No history is injected by default. When provided, the
assembler builds history blocks, applies the compaction pipeline if a budget is
configured, and renders `ChatMessage` values without changing the public return
type.

## Boundaries

v0.9.1 does not:

- delete raw history/session/OCEL/PIG data
- implement a persistent conversation history store
- call an LLM for history summarization
- enable AutoCompact
- add tokenizer, async, UI, MCP, plugins, or external connectors

## Restore / Verification Commands

Representative tests:

```powershell
.\.venv\Scripts\python.exe -m pytest `
  tests\test_context_history.py `
  tests\test_context_history_policy.py `
  tests\test_context_history_builder.py `
  tests\test_snip_layer_session_policy.py `
  tests\test_process_context_history_integration.py `
  tests\test_context_pipeline_history_policy.py `
  tests\test_context_layers_snip.py `
  tests\test_process_run_loop_context_budget.py
```

Smoke script:

```powershell
.\.venv\Scripts\python.exe scripts\test_context_history_snip.py
```

## Operational Notes

Use v0.9.1 when conversation history starts crowding out current task context.
Inspect `SnipLayer.result_attrs` to confirm protected block IDs, dropped history
IDs, and deterministic snip reasons.

## Remaining Limitations

- No persistent conversation history store.
- No semantic auto-compact.
- No tokenizer-based token counting.
- No learned history selection.
- No subagent context isolation.

# ChantaCore v0.10.3 Restore

## Version

ChantaCore v0.10.3 - OCEL-native Hook Lifecycle Observability.

## Purpose

v0.10.3 adds hook lifecycle observability as an OCEL-native substrate. Hook
definitions, invocations, results, and policies are persisted as OCEL
event/object/relation records.

This release is observational only. It does not execute hook handlers, enforce
permissions, block tools, rewrite tool calls, mutate tool input/output, or load
external plugins. `HookPolicy` is observe/log metadata, not a permission model.

## Added Package

The release adds `src/chanta_core/hooks/`:

- `__init__.py`
- `ids.py`
- `errors.py`
- `models.py`
- `registry.py`
- `lifecycle.py`
- `service.py`

## Lifecycle Stages

`lifecycle.py` defines deterministic lifecycle stage helpers:

- `normalize_lifecycle_stage(stage)`
- `is_known_lifecycle_stage(stage)`

Known stages include session, turn, process, decision, skill, tool, context
compaction, materialized view refresh, error, and `other` stages. Unknown values
normalize to `other`.

## Models

`HookDefinition` describes a hook:

- hook ID/name/type
- lifecycle stage
- description
- status
- priority
- scope/source kind
- `handler_ref`
- created/updated timestamps
- attrs

`handler_ref` is metadata only in v0.10.3. It is not imported, called, or
executed.

`HookInvocation` records an observed lifecycle match/invocation:

- invocation ID
- hook ID
- lifecycle stage/status
- session, turn, and process IDs if provided
- triggering event ID if provided
- deterministic input summary/hash
- attrs

`HookResult` records the observational result:

- result ID
- invocation ID and hook ID
- status
- result kind
- output summary/hash
- error message
- attrs

Forbidden result kinds are rejected:

- `allow`
- `deny`
- `ask`
- `block`
- `rewrite`
- `mutate_input`
- `mutate_output`

`HookPolicy` records observe/log-only policy metadata:

- policy ID
- hook ID
- policy kind
- status
- scope
- attrs

Forbidden policy kinds are rejected using the same set above. This prevents
v0.10.3 hooks from being mistaken for permission enforcement.

## Registry

`HookRegistry` is in-memory only:

- `register`
- `list_hooks`
- `get_hook`
- `find_by_stage`
- `disable_hook`
- `clear`

Hook ordering is deterministic:

1. priority descending, when priority exists;
2. hook name;
3. hook ID.

The registry does not load external plugins, import handlers, or execute hooks.
Canonical registration facts are emitted by `HookLifecycleService` through
OCEL.

## HookLifecycleService

`HookLifecycleService` records hook lifecycle facts through `TraceService` and
`OCELStore`.

Methods:

- `register_hook_definition(...)`
- `update_hook_definition(...)`
- `deprecate_hook_definition(...)`
- `register_hook_policy(...)`
- `match_hooks(...)`
- `record_hook_invocation(...)`
- `complete_hook_invocation(...)`
- `fail_hook_invocation(...)`
- `skip_hook_invocation(...)`
- `observe_lifecycle_point(...)`

`observe_lifecycle_point(...)` is no-op observation. It matches active hooks for
a lifecycle stage, records invocation, and immediately records an observed/noop
result. It does not execute `handler_ref` and cannot change caller behavior.

## OCEL Object Types

The release actively uses:

- `hook_definition`
- `hook_invocation`
- `hook_result`
- `hook_policy`

Object attrs include lifecycle stage, status, hook IDs, invocation IDs, result
kind, policy kind, summaries, hashes, and contextual session/turn/process IDs
where provided.

## OCEL Event Activities

Generic hook events:

- `hook_definition_registered`
- `hook_definition_updated`
- `hook_definition_deprecated`
- `hook_policy_registered`
- `hook_matched`
- `hook_invoked`
- `hook_completed`
- `hook_failed`
- `hook_skipped`
- `hook_result_recorded`

Lifecycle-specific invocation events:

- `pre_process_run_hook_invoked`
- `post_process_run_hook_invoked`
- `pre_tool_dispatch_hook_invoked`
- `post_tool_dispatch_hook_invoked`
- `pre_materialized_view_refresh_hook_invoked`
- `post_materialized_view_refresh_hook_invoked`
- `on_error_hook_invoked`

Events are marked with `observability_only=True` and
`enforcement_enabled=False`.

## Relation Intent

Event-object relation qualifiers include:

- `hook_definition_object`
- `hook_invocation_object`
- `hook_result_object`
- `hook_policy_object`
- `session_context`
- `turn_context`
- `process_context`

Object-object relation qualifiers include:

- `invokes`
- `result_of`
- `applies_to_hook`
- `belongs_to_session`
- `belongs_to_turn`
- `observes_process_instance`

If relation helper APIs change, the restoration standard is that the same facts
remain reconstructible from OCEL records.

## PIG/OCPX Support

`PIGReportService` includes a lightweight hook lifecycle summary in
`report_attrs["hook_lifecycle_summary"]` and report text:

- hook definition count
- hook invocation count
- hook result count
- hook policy count
- hook invoked/completed/failed/skipped counts
- hook invocations by lifecycle stage

This is reporting only. It is not hook analytics, enforcement, or permission
evaluation.

## Integration Scope

v0.10.3 provides service-level lifecycle observation. Runtime integration points
such as `AgentRuntime`, `ProcessRunLoop`, `ToolDispatcher`, and
`MaterializedViewService` can call `HookLifecycleService` in a later release,
but no behavior-changing integration is required here.

## Boundaries

v0.10.3 does not:

- execute hook handlers;
- dynamically import `handler_ref`;
- execute shell, HTTP, or LLM hooks;
- load MCP/plugin hooks;
- enforce permission allow/deny/ask;
- block tool calls;
- rewrite tool input;
- rewrite tool output;
- mutate runtime behavior;
- add async hook runtime;
- add canonical JSONL hook persistence;
- make Markdown canonical.

## Restore Checklist

Use this checklist when rebuilding or auditing the release:

- `src/chanta_core/hooks/` contains ID helpers, errors, models, registry,
  lifecycle helpers, and service.
- IDs use `hook_definition:`, `hook_invocation:`, `hook_result:`, and
  `hook_policy:` prefixes.
- `HookDefinition`, `HookInvocation`, `HookResult`, and `HookPolicy` all expose
  `to_dict()`.
- `HookResult` and `HookPolicy` reject enforcement-like values.
- `HookRegistry` is in-memory and deterministic.
- `HookLifecycleService` emits hook OCEL events.
- Hook object types appear in OCEL object state.
- `handler_ref` remains metadata-only.
- PIG reports expose hook lifecycle counts.
- Tests confirm no external handler execution or permission enforcement surface.

## Restore / Verification Commands

Representative tests:

```powershell
.\.venv\Scripts\python.exe -m pytest `
  tests\test_hook_models.py `
  tests\test_hook_registry.py `
  tests\test_hook_lifecycle_service.py `
  tests\test_hook_ocel_shape.py `
  tests\test_hook_boundaries.py `
  tests\test_pig_reports.py
```

Full related regression set:

```powershell
.\.venv\Scripts\python.exe -m pytest `
  tests\test_imports.py `
  tests\test_hook_models.py `
  tests\test_hook_registry.py `
  tests\test_hook_lifecycle_service.py `
  tests\test_hook_ocel_shape.py `
  tests\test_hook_boundaries.py `
  tests\test_materialized_view_models.py `
  tests\test_materialized_view_renderers.py `
  tests\test_materialized_view_service.py `
  tests\test_materialized_view_ocel_shape.py `
  tests\test_materialized_view_boundaries.py `
  tests\test_memory_models.py `
  tests\test_instruction_models.py `
  tests\test_memory_service.py `
  tests\test_instruction_service.py `
  tests\test_memory_context_history_adapter.py `
  tests\test_instruction_context_history_adapter.py `
  tests\test_memory_instruction_ocel_shape.py `
  tests\test_session_models.py `
  tests\test_session_service.py `
  tests\test_agent_runtime_session_integration.py `
  tests\test_session_context_history_adapter.py `
  tests\test_session_ocel_shape.py `
  tests\test_process_run_loop.py `
  tests\test_ocel_store.py `
  tests\test_context_history.py `
  tests\test_pig_reports.py
```

Smoke script:

```powershell
.\.venv\Scripts\python.exe scripts\test_hook_lifecycle.py
```

## Remaining Limitations

- No hook enforcement.
- No permission/grant integration.
- No external plugin or MCP hook loading.
- No async hooks.
- No shell, HTTP, or LLM hook execution.
- No runtime tool blocking or mutation.
- No session resume/fork.

# ChantaCore v0.6.2 Restore - Built-in Skill Baseline with Process Intelligence Skills

## 1. Version identity

Version: `0.6.2`

Version name: ChantaCore v0.6.2 - Built-in Skill Baseline with Process Intelligence Skills

This restore document records the expected source, runtime, trace, and test
state for v0.6.2. It is intentionally a restore document, not a short note,
because this version expands the built-in skill surface and establishes
process-intelligence skills as first-class ChantaCore capabilities.

## 2. Architectural identity

ChantaCore is not only an LLM/tool harness.

The intended stack is:

```text
runtime execution
-> OCEL event/object/relation persistence
-> OCPX object-centric process read/computation model
-> PIG graph/guide/diagnostics/recommendations/context
-> future feedback into runtime and prompt context
```

The process intelligence layer is `pig`.

Do not create a separate package such as:

- `src/chanta_core/process_intelligence/`
- `src/chanta_core/pi/`
- `src/chanta_core/intelligence/`

PIG means Process Intelligence Graph / Guide / Diagnostics /
Recommendations / Context. Although the name includes Graph, the layer also
owns guide summaries, diagnostics, recommendations, and future runtime context.

## 3. Scope

v0.6.2 adds a baseline set of built-in skills:

- `skill:llm_chat`
- `skill:echo`
- `skill:summarize_text`
- `skill:inspect_ocel_recent`
- `skill:summarize_process_trace`

The two process intelligence skills are built-in ChantaCore capabilities:

- `inspect_ocel_recent`
- `summarize_process_trace`

They use the local OCEL/OCPX/PIG stack. They are not external tools and they
do not require LM Studio.

## 4. Non-goals

v0.6.2 intentionally does not implement:

- external skill ingestion
- arbitrary callable execution
- tool dispatch
- permission gate
- worker queue
- MissionLoop
- GoalLoop
- multi-iteration planning
- async runtime
- pm4py or ocpa runtime dependency
- pandas, numpy, networkx, FastAPI, or Streamlit integration
- PIGContext prompt feedback

PIGContext feedback is planned for a later version, expected as v0.6.3 work if
the current architecture remains valid.

## 5. Built-in skill contract

All built-in skills follow the same boundary:

```text
SkillExecutionContext -> SkillExecutionResult
```

A built-in skill must not return `ProcessRunResult` directly and must not own
or mutate `ProcessRunState`.

Each built-in module exposes:

```python
create_<skill_name>_skill() -> Skill
execute_<skill_name>_skill(...) -> SkillExecutionResult
```

The registry registers built-ins through:

```python
SkillRegistry.register_builtin_skills()
```

The executor dispatches by `skill_id`.

## 6. Built-in skill list

### skill:llm_chat

Implementation:

```text
src/chanta_core/skills/builtin/llm_chat.py
```

Purpose:

- answer the user request with the configured LLM provider

Trace behavior:

- records `assemble_context`
- records `call_llm`
- records `receive_llm_response`

### skill:echo

Implementation:

```text
src/chanta_core/skills/builtin/echo.py
```

Purpose:

- return user input as-is
- provide deterministic non-LLM dispatch coverage

Expected output attrs:

- `execution_type = "builtin"`
- `echoed = True`
- `response_length`

This skill does not call the LLM, OCEL query layer, OCPX, or PIG.

### skill:summarize_text

Implementation:

```text
src/chanta_core/skills/builtin/summarize_text.py
```

Purpose:

- summarize input text through the configured LLM provider

Expected output attrs:

- `execution_type = "llm"`
- `summary_mode = "builtin_summarize_text"`
- `input_length`
- `response_length`

Trace behavior:

- records `call_llm`
- records `receive_llm_response`

This skill does not use external tools.

### skill:inspect_ocel_recent

Implementation:

```text
src/chanta_core/skills/builtin/inspect_ocel_recent.py
```

Purpose:

- inspect recent OCEL events, objects, and relations from `OCELStore`

Expected output attrs:

- `event_count`
- `object_count`
- `event_object_relation_count`
- `object_object_relation_count`
- `recent_event_activities`
- `duplicate_relations_valid`

This skill reads the canonical OCEL SQLite store. It does not call the LLM and
does not use external tools.

### skill:summarize_process_trace

Implementation:

```text
src/chanta_core/skills/builtin/summarize_process_trace.py
```

Purpose:

- summarize a recent or process-instance-centered trace through OCPX and PIG

Expected output attrs:

- `activity_sequence`
- `event_count`
- `object_count`
- `guide`
- `diagnostics`
- `recommendations`
- `scope`

If `context.context_attrs["process_instance_id"]` is present, the skill should
analyze that process instance. Otherwise it analyzes a recent view.

This skill does not call the LLM and does not use external tools.

## 7. Registry state

`SkillRegistry.register_builtin_skills()` must register:

- `skill:llm_chat`
- `skill:echo`
- `skill:summarize_text`
- `skill:inspect_ocel_recent`
- `skill:summarize_process_trace`

Lookup must work by both `skill_id` and `skill_name`.

`list_skills()` returns deterministic order sorted by `skill_id`.

Duplicate rules from v0.6.1 remain:

- identical duplicate skill id registration is idempotent
- same skill id with different definition raises
- same skill name with different skill id raises

## 8. SkillExecutor state

`SkillExecutor` dispatches built-ins through a handler map keyed by `skill_id`.

Expected handlers:

- `skill:llm_chat -> execute_llm_chat_skill`
- `skill:echo -> execute_echo_skill`
- `skill:summarize_text -> execute_summarize_text_skill`
- `skill:inspect_ocel_recent -> execute_inspect_ocel_recent_skill`
- `skill:summarize_process_trace -> execute_summarize_process_trace_skill`

Unsupported skills continue to return a deterministic failed
`SkillExecutionResult` by default.

`SkillExecutionPolicy` from v0.6.1 remains active.

## 9. ProcessRunLoop selection

Default `ProcessRunLoop` behavior still selects:

```text
skill:llm_chat
```

v0.6.2 adds a minimal non-planner selection path:

```python
ProcessRunLoop.run(..., skill_id: str | None = None)
```

If `skill_id` is provided, the loop resolves that built-in skill through
`SkillRegistry` and dispatches it through `SkillExecutor`.

This is not a planner and not multi-iteration planning.

## 10. OCEL trace expectations

All built-in skills are represented through:

- `select_skill`
- `execute_skill`
- `observe_result`

LLM-based skills also record:

- `call_llm`
- `receive_llm_response`

Non-LLM skills do not record LLM activities.

Skill objects remain OCEL objects with:

- `object_type = "skill"`
- `object_id = "skill:<name>"`

Skill selection and execution relations remain:

- `selected_skill -> skill:<id>`
- `executed_skill -> skill:<id>`

Duplicate relation validation should remain valid.

## 11. Canonical model constraints

v0.6.2 preserves the canonical model:

`OCELEvent`:

- `event_id`
- `event_activity`
- `event_timestamp`
- `event_attrs`

`OCELObject`:

- `object_id`
- `object_type`
- `object_attrs`

`OCELRelation`:

- `relation_kind`
- `source_id`
- `target_id`
- `qualifier`
- `relation_attrs`

Do not reintroduce:

- canonical top-level `event_type`
- canonical top-level `object_key`
- canonical top-level `display_name`
- generic metadata dump field

Timestamp creation remains centralized through:

```python
from chanta_core.utility.time import utc_now_iso
```

## 12. OCPX and PIG

OCPX continues to expose `activity_sequence(view)`.

PIG public names remain:

- `PIGBuilder`
- `PIGService`

Do not introduce:

- `PIGGraphBuilder`
- `PIGGuideService`

`summarize_process_trace` should use:

- `OCPXLoader`
- `OCPXEngine`
- `PIGService`

No separate process intelligence package is created.

## 13. Tests

v0.6.2 adds coverage for:

- built-in registry baseline
- deterministic echo skill
- summarize_text with fake LLM
- inspect_ocel_recent without LLM
- summarize_process_trace without LLM
- ProcessRunLoop execution with non-default skill selection
- process intelligence skills without LM Studio

Expected unit command:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_imports.py tests\test_ocel_store.py tests\test_time_utility.py tests\test_skill_model.py tests\test_skill_registry.py tests\test_skill_executor.py tests\test_skill_executor_failure.py tests\test_builtin_skills.py tests\test_process_intelligence_skills.py tests\test_process_run_loop.py tests\test_process_run_loop_failure.py tests\test_process_run_loop_skill_dispatch.py tests\test_process_run_loop_skill_failure.py tests\test_process_run_loop_builtin_skill_selection.py tests\test_process_instance_runtime.py tests\test_agent_runtime_ocel_shape.py tests\test_ocpx_foundation.py tests\test_pig_foundation.py
```

## 14. Scripts

v0.6.2 adds:

```text
scripts/test_builtin_skills.py
scripts/test_process_intelligence_skills.py
```

The process-intelligence script should run without LM Studio because the
skills it exercises do not require an LLM.

## 15. Restore checklist

Skill baseline:

- five built-in skills are registered.
- lookup by id and name works.
- `skill:echo` runs without LLM.
- `skill:summarize_text` runs with fake or configured LLM.
- `skill:inspect_ocel_recent` runs without LLM.
- `skill:summarize_process_trace` runs without LLM.

Runtime:

- `ProcessRunLoop` can still default to `skill:llm_chat`.
- `ProcessRunLoop.run(..., skill_id=...)` can run non-default built-ins.
- selected skill is traced through `select_skill`.
- executed skill is traced through `execute_skill`.
- non-LLM built-ins do not emit LLM call events.
- LLM built-ins emit `call_llm` and `receive_llm_response`.

Process intelligence:

- `inspect_ocel_recent` reads OCELStore.
- `summarize_process_trace` uses OCPX and PIG.
- no `process_intelligence`, `pi`, or `intelligence` package exists.
- PIG remains the process intelligence layer.

Git hygiene:

- generated SQLite files remain ignored.
- `data/` remains ignored.
- `.pytest-tmp/` remains ignored.
- no `.env` is tracked.

## 16. Remaining limitations

v0.6.2 still has:

- no PIGContext feedback
- no external skill ingestion
- no arbitrary callable skill execution
- no tool dispatch
- no permission gate
- no worker queue
- no multi-iteration planning
- no async runtime
- no full process mining algorithm
- no pm4py/ocpa conformance claim

## 17. Conclusion

ChantaCore v0.6.2 establishes the first built-in skill baseline beyond
`llm_chat`. It adds deterministic, LLM-based, OCEL inspection, and
OCPX/PIG-based process trace summary skills while keeping skill execution
bounded by `SkillExecutor`, traced through OCEL, and intentionally free of
external skill ingestion or tool runtime behavior.

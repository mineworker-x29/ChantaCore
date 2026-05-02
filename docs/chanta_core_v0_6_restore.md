# ChantaCore v0.6 Restore - Skill Dispatch Runtime

## 1. Version identity

Version: `0.6.0`

Version name: ChantaCore v0.6 - Skill Dispatch Runtime

This restore note documents the state that should be reconstructed when
restoring v0.6 from source. It is intentionally more detailed than a release
note because v0.6 changes the runtime ownership boundary between
`ProcessRunLoop` and skill execution.

## 2. Architectural purpose

v0.6 introduces a real skill dispatch layer.

Before v0.6, `ProcessRunLoop` selected `skill:llm_chat` but still assembled
context and called the LLM client directly. That made the loop responsible for
both process control and skill-specific execution.

In v0.6, the ownership is split:

- `ProcessRunLoop` owns process progression.
- `SkillRegistry` owns skill lookup.
- `SkillExecutor` owns dispatch to a concrete skill implementation.
- The built-in `llm_chat` skill owns LLM-specific execution.
- `TraceService` and `OCELFactory` continue to own OCEL persistence.

This keeps the loop simple and prepares a future path for additional skill
types without putting every execution path directly inside the loop.

## 3. Non-goals

v0.6 does not implement:

- external skill ingestion
- arbitrary Python callable skill execution
- full tool dispatch
- permission gates
- worker queue
- MissionLoop
- GoalLoop
- multi-iteration planning
- async execution
- MCP/plugin runtime
- pm4py or ocpa runtime dependency

These are intentionally deferred.

## 4. Skill model

The canonical skill descriptor lives in:

```text
src/chanta_core/skills/skill.py
```

`Skill` is a dataclass with:

- `skill_id`
- `skill_name`
- `description`
- `execution_type`
- `input_schema`
- `output_schema`
- `tags`
- `skill_attrs`

It also exposes `to_dict()`.

Important ontology distinction:

- `Skill` is a capability object.
- `Skill` is not an event activity.
- Skill execution is represented by the stable event activity
  `execute_skill`.

## 5. Built-in skill

The first executable built-in skill is:

```text
skill:llm_chat
```

Implementation files:

```text
src/chanta_core/skills/builtin/__init__.py
src/chanta_core/skills/builtin/llm_chat.py
```

The factory function is:

```python
create_llm_chat_skill() -> Skill
```

The compatibility alias remains:

```python
builtin_llm_chat_skill = create_llm_chat_skill
```

The built-in skill has:

- `skill_id = "skill:llm_chat"`
- `skill_name = "llm_chat"`
- `execution_type = "llm"`
- `tags = ["llm", "chat", "default"]`
- `skill_attrs["is_builtin"] = True`
- `skill_attrs["provider_mode"] = "configured"`

## 6. Skill execution context

`SkillExecutionContext` lives in:

```text
src/chanta_core/skills/context.py
```

It carries the runtime context from `ProcessRunLoop` to `SkillExecutor`:

- `process_instance_id`
- `session_id`
- `agent_id`
- `user_input`
- `system_prompt`
- `event_attrs`
- `context_attrs`

The field is intentionally named `context_attrs`, not generic `metadata`.

## 7. Skill execution result

`SkillExecutionResult` lives in:

```text
src/chanta_core/skills/result.py
```

It is the uniform result object returned from skill dispatch:

- `skill_id`
- `skill_name`
- `success`
- `output_text`
- `output_attrs`
- `error`

The `ProcessRunLoop` converts this result into `ProcessObservation`.

For successful `llm_chat`, `output_attrs` includes:

- `execution_type = "llm"`
- `response_length`

For failed `llm_chat`, `output_attrs` includes:

- `execution_type = "llm"`
- `exception_type`
- `failure_stage = "call_llm"`

## 8. Skill registry

`SkillRegistry` lives in:

```text
src/chanta_core/skills/registry.py
```

It supports:

- `register(skill)`
- `get(skill_id_or_name)`
- `require(skill_id_or_name)`
- `list_skills()`
- `register_builtin_skills()`
- `get_builtin_llm_chat()`

Lookup works by:

- skill id, for example `skill:llm_chat`
- skill name, for example `llm_chat`

Different definitions for the same `skill_id` are not silently overwritten.

## 9. Skill executor

`SkillExecutor` lives in:

```text
src/chanta_core/skills/executor.py
```

Constructor dependencies:

- `llm_client`
- `context_assembler`
- `trace_service`

Primary method:

```python
execute(skill: Skill, context: SkillExecutionContext) -> SkillExecutionResult
```

Dispatch behavior:

- If `skill.skill_id == "skill:llm_chat"` or
  `skill.execution_type == "llm"`, execution is delegated to
  `execute_llm_chat_skill(...)`.
- Unsupported execution types return a failed `SkillExecutionResult` with
  `failure_stage = "skill_dispatch"`.

v0.6 does not execute arbitrary callables and does not load external skills.

## 10. ProcessRunLoop integration

The loop lives in:

```text
src/chanta_core/runtime/loop/process_run_loop.py
```

The loop still owns:

- process state
- activity decision
- skill selection
- process observation conversion
- outcome recording
- process completion or failure

The loop no longer owns:

- LLM-specific context execution
- direct `llm_client.chat_messages(...)` calls

The v0.6 loop flow is:

1. Start process run loop.
2. Decide next activity.
3. Resolve `skill:llm_chat` from `SkillRegistry`.
4. Record `select_skill`.
5. Record `execute_skill`.
6. Build `SkillExecutionContext`.
7. Call `SkillExecutor.execute(...)`.
8. Extend loop event list with events emitted by the skill executor.
9. Convert `SkillExecutionResult` into `ProcessObservation`.
10. Record `observe_result`.
11. Record outcome.
12. Complete process instance.

The default policy remains bounded to one iteration.

## 11. OCEL trace shape

v0.6 preserves the OCEL canonical model:

- `OCELEvent` uses `event_activity`.
- `OCELObject` uses `object_attrs`.
- relation payloads use `relation_attrs`.
- timestamps use `chanta_core.utility.time.utc_now_iso()`.

The expected success activity sequence for a direct `ProcessRunLoop` run is:

```text
start_process_run_loop
decide_next_activity
select_skill
execute_skill
assemble_context
call_llm
receive_llm_response
observe_result
record_outcome
complete_process_instance
```

For `AgentRuntime`, the process setup events come first:

```text
receive_user_request
start_process_instance
start_process_run_loop
decide_next_activity
select_skill
execute_skill
assemble_context
call_llm
receive_llm_response
observe_result
record_outcome
complete_process_instance
```

## 12. Skill object trace

`skill:llm_chat` is represented as an OCEL object:

```text
object_id = skill:llm_chat
object_type = skill
```

Its `object_attrs` include:

- `skill_name`
- `description`
- `execution_type`
- `input_schema`
- `output_schema`
- `tags`
- `is_builtin`
- `provider_mode`

The key event-object relations are:

- `select_skill --selected_skill--> skill:llm_chat`
- `execute_skill --executed_skill--> skill:llm_chat`

The process-object relation remains:

- `process_instance --uses_skill--> skill:llm_chat`

## 13. LLM chat skill trace

The built-in LLM chat skill records:

- `assemble_context`
- `call_llm`
- `receive_llm_response`

These are emitted through `TraceService`, so the LLM-specific path remains
OCEL-backed even though it moved out of `ProcessRunLoop`.

## 14. Failure compatibility

v0.6 preserves the v0.5.1 failure path.

If `llm_chat` fails:

- `execute_llm_chat_skill(...)` returns a failed `SkillExecutionResult`.
- `ProcessRunLoop` converts it into a failed `ProcessObservation`.
- `ProcessRunLoop` records `fail_process_instance`.
- The failure includes `failure_stage = "call_llm"`.
- `ProcessRunPolicy.raise_on_failure` still controls raise vs failed result.

## 15. OCPX and PIG

OCPX still reads event activities from OCELStore.

`OCPXEngine.activity_sequence(view)` should include:

- `select_skill`
- `execute_skill`
- `call_llm`
- `receive_llm_response`

PIG public names remain:

- `PIGBuilder`
- `PIGService`

No `PIGGraphBuilder` or `PIGGuideService` is introduced.

## 16. Validation commands

Editable install:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

Unit tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_imports.py tests\test_ocel_store.py tests\test_time_utility.py tests\test_skill_registry.py tests\test_skill_executor.py tests\test_process_run_loop.py tests\test_process_run_loop_failure.py tests\test_process_run_loop_skill_dispatch.py tests\test_process_instance_runtime.py tests\test_agent_runtime_ocel_shape.py tests\test_ocpx_foundation.py tests\test_pig_foundation.py
```

Scripts:

```powershell
.\.venv\Scripts\python.exe scripts\test_skill_dispatch.py
.\.venv\Scripts\python.exe scripts\test_process_run_loop.py
.\.venv\Scripts\python.exe scripts\test_process_run_loop_failure.py
.\.venv\Scripts\python.exe scripts\test_agent_runtime.py
.\.venv\Scripts\python.exe scripts\test_ocel_runtime.py
.\.venv\Scripts\python.exe scripts\test_ocpx_loader.py
.\.venv\Scripts\python.exe scripts\test_pig_imports.py
```

Generated file hygiene:

```powershell
git status --short
git status --ignored --short data .pytest-tmp
git ls-files | findstr "data"
git ls-files | findstr ".sqlite"
git ls-files | findstr ".env"
```

## 17. Restore checklist

Skill foundation:

- `Skill` exists.
- `SkillRegistry` exists.
- `SkillExecutor` exists.
- `SkillExecutionContext` exists.
- `SkillExecutionResult` exists.
- `skill:llm_chat` is registered by default.
- skill lookup works by id and name.

Loop integration:

- `ProcessRunLoop` uses `SkillRegistry`.
- `ProcessRunLoop` uses `SkillExecutor`.
- direct LLM execution is not hardcoded in the loop.
- `SkillExecutionResult` is converted into `ProcessObservation`.
- success path works.
- failure path works.

OCEL trace:

- `select_skill` is recorded.
- `execute_skill` is recorded.
- `call_llm` is recorded.
- `receive_llm_response` is recorded.
- skill object exists.
- `selected_skill` relation exists.
- `executed_skill` relation exists.
- duplicate relation validator returns valid.

OCPX/PIG:

- OCPX activity sequence works.
- skill dispatch activities appear in the activity sequence.
- PIGService analyze_recent works.
- `PIGBuilder` and `PIGService` names remain unchanged.

Regression:

- fake LLM success test passes.
- fake LLM failure test passes.
- existing ProcessRunLoop tests pass.
- AgentRuntime integration test passes.
- generated files remain ignored.

## 18. Known limitations

v0.6 is still intentionally minimal:

- no external skill ingestion
- no arbitrary callable skill execution
- no tool dispatch
- no permission gate
- no worker queue
- no multi-iteration planning
- no full process mining algorithm
- no full pm4py/ocpa conformance claim

## 19. Conclusion

ChantaCore v0.6 introduces a real skill dispatch boundary while keeping the
runtime synchronous, bounded, and OCEL-backed. The main architectural result is
that `ProcessRunLoop` now controls process progression, while `SkillExecutor`
owns skill-specific execution dispatch.

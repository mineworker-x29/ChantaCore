# ChantaCore v0.6.1 Restore - Skill Dispatch Contract Hardening

## 1. Version identity

Version: `0.6.1`

Version name: ChantaCore v0.6.1 - Skill Dispatch Contract Hardening

This restore document records the expected source, runtime, trace, and test
state for v0.6.1. It replaces the shorter note-style document because v0.6.1 is
primarily a contract-hardening release, and restore work needs enough detail to
distinguish skill failure, process failure, and unsupported skill dispatch.

## 2. Scope

v0.6.1 hardens the skill dispatch layer introduced in v0.6.

It does not add new autonomy features. It makes the existing dispatch path
stricter and more predictable before future versions add additional skills,
tools, workers, permission gates, or multi-iteration planning.

The main runtime path remains:

```text
AgentRuntime
-> ProcessRunLoop
-> SkillRegistry
-> SkillExecutor
-> built-in skill:llm_chat
-> TraceService
-> OCELFactory
-> OCELStore
```

## 3. Non-goals

v0.6.1 intentionally does not implement:

- external skill ingestion
- arbitrary callable skill execution
- tool dispatch
- permission gate
- worker queue
- MissionLoop
- GoalLoop
- multi-iteration planning
- async runtime
- pm4py or ocpa runtime dependency
- pandas, numpy, networkx, FastAPI, or Streamlit integration

If any of these exist in a restored v0.6.1 tree, the tree has drifted beyond
the intended release boundary.

## 4. Skill model contract

The skill model lives in:

```text
src/chanta_core/skills/skill.py
```

`Skill` remains a dataclass with:

- `skill_id: str`
- `skill_name: str`
- `description: str`
- `execution_type: str`
- `input_schema: dict[str, Any]`
- `output_schema: dict[str, Any]`
- `tags: list[str]`
- `skill_attrs: dict[str, Any]`

`Skill` exposes:

- `to_dict()`
- `validate()`

`validate()` enforces:

- `skill_id` is not empty
- `skill_id` starts with `skill:`
- `skill_name` is not empty
- `execution_type` is not empty
- `input_schema` is a dict
- `output_schema` is a dict
- `tags` is `list[str]`
- `skill_attrs` is a dict

Invalid descriptors raise:

```text
SkillValidationError
```

defined in:

```text
src/chanta_core/skills/errors.py
```

## 5. Registry contract

The registry lives in:

```text
src/chanta_core/skills/registry.py
```

`SkillRegistry` supports:

- `register(skill)`
- `get(skill_id_or_name)`
- `require(skill_id_or_name)`
- `list_skills()`
- `register_builtin_skills()`
- `get_builtin_llm_chat()`

Registry behavior:

- every registration calls `skill.validate()`
- lookup by `skill_id` works
- lookup by `skill_name` works
- registering the same skill id with an identical definition is idempotent
- registering the same skill id with a different definition raises
- registering the same skill name with a different skill id raises
- `list_skills()` returns deterministic order sorted by `skill_id`

Registry contract errors raise:

```text
SkillRegistryError
```

defined in:

```text
src/chanta_core/skills/errors.py
```

## 6. Built-in skill

The built-in LLM chat skill remains:

```text
skill:llm_chat
```

Implementation:

```text
src/chanta_core/skills/builtin/llm_chat.py
```

Factory:

```python
create_llm_chat_skill() -> Skill
```

Compatibility alias:

```python
builtin_llm_chat_skill = create_llm_chat_skill
```

Expected descriptor values:

- `skill_id = "skill:llm_chat"`
- `skill_name = "llm_chat"`
- `execution_type = "llm"`
- `tags = ["llm", "chat", "default"]`
- `skill_attrs["is_builtin"] = True`
- `skill_attrs["provider_mode"] = "configured"`

## 7. Executor contract

The executor lives in:

```text
src/chanta_core/skills/executor.py
```

`SkillExecutor` validates the skill and dispatches supported skill execution.

v0.6.1 introduces:

```python
SkillExecutionPolicy
```

with:

- `raise_on_failure: bool = False`
- `record_failure_event: bool = True`

Default behavior is intentionally non-throwing for skill execution failures.
The executor returns a failed `SkillExecutionResult`, and `ProcessRunLoop`
decides whether the process fails.

Supported v0.6.1 dispatch:

- `skill_id == "skill:llm_chat"`
- or `execution_type == "llm"`

Unsupported skill behavior:

- returns `SkillExecutionResult(success=False)`
- does not crash by default
- includes `failure_stage = "skill_dispatch"`
- includes `exception_type = "UnsupportedSkillExecution"`
- includes `skill_id`
- includes `skill_name`

If `SkillExecutionPolicy.raise_on_failure=True`, the executor raises after
creating/recording the failed result.

## 8. SkillExecutionResult contract

The result model lives in:

```text
src/chanta_core/skills/result.py
```

Fields:

- `skill_id`
- `skill_name`
- `success`
- `output_text`
- `output_attrs`
- `error`

Successful `llm_chat` result:

- `success = True`
- `output_text = <LLM response text>`
- `output_attrs["execution_type"] = "llm"`
- `output_attrs["response_length"] = len(output_text)`

Failing `llm_chat` result:

- `success = False`
- `output_text = None`
- `error = str(exception)`
- `output_attrs["failure_stage"] = "call_llm"`
- `output_attrs["exception_type"] = type(exception).__name__`
- `output_attrs["skill_id"] = "skill:llm_chat"`
- `output_attrs["skill_name"] = "llm_chat"`

## 9. ProcessRunLoop behavior

`ProcessRunLoop` remains the runtime owner for process progression.

On skill success:

1. select `skill:llm_chat`
2. record `select_skill`
3. record `execute_skill`
4. call `SkillExecutor.execute(...)`
5. convert `SkillExecutionResult(success=True)` into
   `ProcessObservation(success=True)`
6. record `observe_result`
7. record `record_outcome`
8. record `complete_process_instance`

On skill failure:

1. `SkillExecutor` returns `SkillExecutionResult(success=False)`
2. `ProcessRunLoop` converts it into `ProcessObservation(success=False)`
3. `ProcessRunLoop` records `observe_result`
4. `ProcessRunLoop` records `fail_process_instance`
5. return failed `ProcessRunResult` if `ProcessRunPolicy.raise_on_failure=False`
6. raise if `ProcessRunPolicy.raise_on_failure=True`

Every skill execution result, success or failure, should become a
`ProcessObservation`.

## 10. OCEL canonical model

v0.6.1 must preserve the canonical model from v0.3.2+:

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

Timestamp generation remains centralized through:

```python
from chanta_core.utility.time import utc_now_iso
```

## 11. OCEL skill failure trace

v0.6.1 adds a distinct skill failure event:

```text
fail_skill_execution
```

This means the selected skill failed.

It is intentionally separate from:

```text
fail_process_instance
```

which means the whole process instance failed.

For failed skill execution, the OCEL trace should include:

Event-object relations:

- `process_context -> process_instance`
- `failed_skill -> skill:<id>`
- `observed_error -> error`
- `acting_agent -> agent`
- `session_context -> session`

Object-object relations:

- `error --error_from_skill_execution--> skill`
- `error --error_from_process--> process_instance`

The error object has:

- `object_type = "error"`
- `object_attrs["error_message"]`
- `object_attrs["error_type"]`
- `object_attrs["failure_stage"]`
- `object_attrs["skill_id"]`
- `object_attrs["process_instance_id"]`
- `object_attrs["created_at"]`

## 12. Expected failing sequence

For a failing built-in `llm_chat` run through `ProcessRunLoop`, the expected
activity sequence is:

```text
start_process_run_loop
decide_next_activity
select_skill
execute_skill
assemble_context
call_llm
fail_skill_execution
observe_result
fail_process_instance
```

## 13. OCPX and PIG behavior

OCPX must be able to load failed skill traces from `OCELStore`.

`OCPXEngine.activity_sequence(view)` can include:

- `fail_skill_execution`
- `fail_process_instance`

PIG behavior:

- `PIGService` should analyze recent or failed views without crashing.
- `PIGBuilder` and `PIGService` names remain unchanged.
- `PIGGraphBuilder` and `PIGGuideService` are not introduced.
- `failed_skill_execution` diagnostic can be emitted when the activity appears.
- recommendation can point to reviewing skill failure / inspecting error object.

## 14. Tests

v0.6.1 adds or extends tests for:

- skill model validation
- registry lookup
- duplicate identical registration
- duplicate skill id with different definition
- duplicate skill name with different id
- deterministic `list_skills()`
- unsupported skill failure result
- fake failing LLM skill result
- `fail_skill_execution` OCEL trace
- process-loop skill failure
- OCPX/PIG compatibility with failed traces

Expected unit command:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_imports.py tests\test_ocel_store.py tests\test_time_utility.py tests\test_skill_model.py tests\test_skill_registry.py tests\test_skill_executor.py tests\test_skill_executor_failure.py tests\test_process_run_loop.py tests\test_process_run_loop_failure.py tests\test_process_run_loop_skill_dispatch.py tests\test_process_run_loop_skill_failure.py tests\test_process_instance_runtime.py tests\test_agent_runtime_ocel_shape.py tests\test_ocpx_foundation.py tests\test_pig_foundation.py
```

## 15. Scripts

v0.6.1 adds:

```text
scripts/test_skill_failure.py
```

This script uses a fake failing LLM and should not require LM Studio.

It prints:

- result status
- observations
- activity sequence
- duplicate relation validation

## 16. Restore checklist

Skill model:

- `Skill.validate()` exists.
- invalid `skill_id` is rejected.
- empty `skill_name` is rejected.
- non-dict schema is rejected.
- `SkillValidationError` exists.

Registry:

- skill id lookup works.
- skill name lookup works.
- identical duplicate registration is idempotent.
- duplicate skill id with different definition raises.
- duplicate skill name with different id raises.
- `list_skills()` is deterministic.

Executor:

- `SkillExecutor` exists.
- `SkillExecutionPolicy` exists.
- `llm_chat` success result works.
- unsupported skill failure is deterministic.
- failing LLM failure is deterministic.
- failed results include `failure_stage` and `exception_type`.

OCEL:

- `fail_skill_execution` is recorded.
- `fail_process_instance` remains recorded for terminating process failures.
- error object is created.
- `error_from_skill_execution` relation exists.
- `error_from_process` relation exists.
- duplicate relation validation returns valid.

ProcessRunLoop:

- failed `SkillExecutionResult` becomes `ProcessObservation(success=False)`.
- success path regression passes.
- failure path regression passes.
- fake tests pass without LM Studio.

OCPX/PIG:

- activity sequence can include `fail_skill_execution`.
- failed skill trace can be loaded.
- `PIGService` does not crash.
- `PIGBuilder` and `PIGService` names remain unchanged.

## 17. Git hygiene

Generated files must remain ignored:

- `.env`
- `.env.*`
- `.venv/`
- `data/`
- `*.sqlite`
- `*.sqlite3`
- `.pytest_cache/`
- `.pytest-tmp/`
- `__pycache__/`
- `*.pyc`
- `src/chanta_core.egg-info/`

Only `.env.example` may be tracked among env files.

## 18. Remaining limitations

v0.6.1 still has:

- no external skill ingestion
- no arbitrary callable skill execution
- no tool dispatch
- no permission gate
- no worker queue
- no multi-iteration planning
- no MissionLoop or GoalLoop
- no async runtime
- no full process mining algorithm
- no pm4py/ocpa conformance claim

## 19. Conclusion

ChantaCore v0.6.1 makes the Skill Dispatch Runtime stricter and more
diagnosable. Unsupported skills and failing LLM skill calls now produce
predictable failed `SkillExecutionResult` values, failed observations, and
OCEL-backed `fail_skill_execution` traces before process-level failure is
recorded.

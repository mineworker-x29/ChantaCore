# ChantaCore v0.5.1 Restore - ProcessRunLoop Failure & Evaluation Hardening

작성일: 2026-05-02
작성자: Vera
대상 버전: ChantaCore v0.5.1
버전 이름: ProcessRunLoop Failure & Evaluation Hardening

이 문서는 ChantaCore v0.5.1을 복원하거나 리뷰할 때 기준으로 삼기 위한 restore
문서다. 단순 변경 노트가 아니라, v0.5.1에서 실패 경로를 어떤 의미로 hardening했고,
어떤 evaluation semantics를 추가했으며, 어떤 기능을 의도적으로 추가하지 않았는지를
정리한다.

## 1. 버전 목적

v0.5.1의 목적은 v0.5의 bounded one-iteration `ProcessRunLoop`를 유지하면서 실패 경로를
runtime/trace/read-model 관점에서 안정화하는 것이다.

v0.5에서 이미 구현된 것:

```text
single user request
single process_instance
single loop iteration
single built-in skill: skill:llm_chat
synchronous LLM call
OCEL trace persistence
OCPX/PIG read model
AgentRuntime uses ProcessRunLoop
```

v0.5.1에서 추가로 강화한 것:

```text
failed ProcessObservation
failed ProcessRunResult
raise_on_failure policy
runtime_basic evaluation attrs
fail_process_instance OCEL event
error object
error_from_process relation
OCPX/PIG failed process compatibility
fake failing LLM test
```

## 2. Non-goals

v0.5.1은 실패 처리 hardening 버전이지, autonomy 확장 버전이 아니다.

구현하지 않는 것:

```text
multi-iteration planning
retry policy
worker queue
tool dispatch
permission gate
subagent delegation
full skill marketplace
full evaluator
reward model
LLM judge
process mining algorithm
pm4py/ocpa runtime dependency
pandas/numpy/networkx dependency
FastAPI/Streamlit server
async runtime
```

이 범위를 넘어서면 v0.5.1의 목적이 흐려진다.

## 3. v0.5 baseline

v0.5의 success-path loop는 다음과 같다.

```text
AgentRuntime.run(...)
  -> receive_user_request
  -> start_process_instance
  -> ProcessRunLoop.run(...)
       -> start_process_run_loop
       -> decide_next_activity
       -> select_skill
       -> execute_skill
       -> assemble_context
       -> call_llm
       -> receive_llm_response
       -> observe_result
       -> record_outcome
       -> complete_process_instance
```

v0.5.1은 이 구조를 유지한다. 변경의 중심은 exception path다.

## 4. ProcessRunPolicy 변경

v0.5.1에서 `ProcessRunPolicy`에 다음 field를 추가했다.

```text
raise_on_failure: bool = True
```

의미:

- `True`: 실패를 OCEL에 기록한 뒤 exception을 다시 raise한다.
- `False`: 실패를 OCEL에 기록하고 `ProcessRunResult(status="failed")`를 반환한다.

기본값을 `True`로 둔 이유:

기존 `AgentRuntime`은 LLM exception을 re-raise하는 동작을 갖고 있었다. v0.5.1은
runtime compatibility를 깨지 않기 위해 기본 behavior를 유지한다.

테스트나 직접 loop 실행에서는 다음처럼 사용한다.

```python
ProcessRunPolicy(raise_on_failure=False)
```

Backward compatibility:

기존 `fail_on_exception` 접근이 필요할 수 있어 property alias를 유지할 수 있다. 하지만
v0.5.1의 공식 policy name은 `raise_on_failure`다.

## 5. Failure path overview

LLM call 또는 skill execution 중 exception이 발생하면 loop는 다음 순서를 따른다.

```text
1. state.status = "failed"
2. state.last_error = str(error)
3. failure_stage 결정
4. state.state_attrs["exception_type"] 저장
5. state.state_attrs["failure_stage"] 저장
6. failed ProcessObservation 생성
7. observations list에 append
8. state.observations에 append
9. TraceService.record_process_instance_failed(...)
10. OCELFactory.fail_process_instance(...)
11. OCELStore append
12. raise_on_failure에 따라 raise 또는 failed ProcessRunResult 반환
```

## 6. Failure stage semantics

v0.5.1의 failure stage는 간단하다.

현재 기본 실패 경로:

```text
execute_skill activity 내부에서 LLMClient.chat_messages(...)가 실패
```

이 경우 observation activity는 `execute_skill`이고, failure_stage는 `call_llm`이다.

예:

```text
activity = "execute_skill"
failure_stage = "call_llm"
exception_type = "RuntimeError"
error = "fake LLM failure"
```

이 구분의 이유:

- process activity 관점에서 현재 loop iteration은 `execute_skill`을 수행 중이다.
- 실제 exception이 발생한 sub-stage는 LLM call이다.
- 따라서 activity와 failure_stage를 분리해 두면 향후 tool dispatch나 retry policy를
  추가할 때 실패 위치를 더 정확히 다룰 수 있다.

## 7. Failed ProcessObservation

v0.5.1은 failure path에서도 observation을 만든다.

Shape:

```text
ProcessObservation(
  activity="execute_skill",
  success=False,
  output_text=None,
  output_attrs={
    "failure_stage": "call_llm",
    "exception_type": "RuntimeError",
    "iteration": 0,
    "selected_skill_id": "skill:llm_chat"
  },
  error="fake LLM failure"
)
```

이 observation은 두 위치에 남는다.

```text
ProcessRunResult.observations
ProcessRunState.observations
```

중요:

failure observation은 아직 OCEL object로 별도 저장하지 않는다. v0.5.1에서는
`fail_process_instance` event와 `error` object가 canonical trace 역할을 한다.

## 8. Failed ProcessRunResult

`raise_on_failure=False`일 때 loop는 failed result를 반환한다.

Shape:

```text
ProcessRunResult(
  process_instance_id="process_instance:<id>",
  session_id="<session_id>",
  agent_id="<agent_id>",
  status="failed",
  response_text="",
  observations=[failed_observation],
  result_attrs={...}
)
```

`response_text`는 실패 시 빈 문자열이다.

## 9. Basic evaluation semantics

v0.5.1에서 `ProcessRunEvaluator`를 추가했다.

파일:

```text
src/chanta_core/runtime/loop/evaluation.py
```

Class:

```text
ProcessRunEvaluator
```

Method:

```text
evaluate(state: ProcessRunState) -> dict[str, Any]
```

Success attrs:

```text
{
  "success": True,
  "evaluation_mode": "runtime_basic",
  "observation_count": <int>
}
```

Failure attrs:

```text
{
  "success": False,
  "evaluation_mode": "runtime_basic",
  "observation_count": <int>,
  "error": "...",
  "exception_type": "...",
  "failure_stage": "..."
}
```

What this is:

- runtime-level basic evaluation
- status and observation count summary
- failure summary

What this is not:

- LLM evaluator
- reward model
- scoring model
- correctness judge
- process mining metric

## 10. OCEL failure event

Failure path persists the canonical event activity:

```text
fail_process_instance
```

`OCELEvent` remains canonical:

```text
event_id
event_activity
event_timestamp
event_attrs
```

No canonical `event_type` field is reintroduced.

Failure event attrs include:

```text
error_message
error_type
error
failure_stage
runtime_event_type
lifecycle
source_runtime
session_id
trace_id
actor_type
actor_id
process_instance_id
```

`session_id` and `actor_id` remain convenience attributes inside `event_attrs`.
Canonical linkage remains object-centric through event-object relations.

## 11. Error object

Failure path creates an OCEL object:

```text
object_type = "error"
```

`OCELObject` remains canonical:

```text
object_id
object_type
object_attrs
```

No canonical top-level `object_key` or `display_name` fields are reintroduced.
Those values may exist inside `object_attrs`.

Error object attrs:

```text
{
  "object_key": "<ExceptionType>",
  "display_name": "<ExceptionType>",
  "error_message": "<message>",
  "error_type": "<ExceptionType>",
  "error": "<message>",
  "failure_stage": "<stage>",
  "process_instance_id": "process_instance:<id>",
  "created_at": "...Z",
  "updated_at": "...Z"
}
```

## 12. Failure relations

Failure event-object relations:

```text
fail_process_instance --process_context--> process_instance
fail_process_instance --observed_error--> error
fail_process_instance --session_context--> session
fail_process_instance --acting_agent--> agent
```

Failure object-object relation:

```text
error --error_from_process--> process_instance
```

Chosen qualifier:

```text
error_from_process
```

Do not mix this with another new qualifier unless a future migration explicitly defines it.
The older `error_from_run` vocabulary may remain for compatibility, but v0.5.1 failure path uses
`error_from_process`.

## 13. Expected failure activity sequence

For fake failing LLM with clean temp DB:

```text
start_process_run_loop
decide_next_activity
select_skill
execute_skill
assemble_context
call_llm
fail_process_instance
```

`receive_llm_response` is not expected on failure.

`observe_result` is also not currently emitted as an OCEL event on failure. The failed observation
is present in `ProcessRunResult` and `ProcessRunState`; the canonical persisted failure marker is
`fail_process_instance` with an `error` object.

This distinction is intentional for v0.5.1. If future versions want failed observations as OCEL
events, that should be added explicitly.

## 14. OCPX compatibility

OCPX can load failed process_instance views using:

```text
OCPXLoader.load_process_instance_view(process_instance_id)
```

Expected view:

- includes `fail_process_instance`
- includes related `error` object
- exposes event attrs for failure info where available

`OCPXEngine.activity_sequence(view)` should include:

```text
fail_process_instance
```

## 15. PIG compatibility

PIG remains lightweight.

v0.5.1 adds a diagnostic:

```text
failed_process_instance
```

Trigger condition:

- activity sequence contains `fail_process_instance`, or
- process_instance object attrs contain `status == "failed"`

Recommendation:

```text
inspect_error_object
```

This is not full graph reasoning. It is a simple failure indicator for early process intelligence.

## 16. AgentRuntime behavior

`AgentRuntime` should preserve existing failure behavior.

Because `ProcessRunPolicy.raise_on_failure` defaults to `True`, LLM exceptions are recorded and
then re-raised.

Direct loop tests can opt into returned failed results:

```python
ProcessRunLoop(
    llm_client=FakeFailingLLMClient(),
    trace_service=TraceService(ocel_store=store),
    policy=ProcessRunPolicy(raise_on_failure=False),
)
```

## 17. Tests

New test:

```text
tests/test_process_run_loop_failure.py
```

Fake failing LLM:

```text
chat_messages(...) raises RuntimeError("fake LLM failure")
```

Assertions:

```text
ProcessRunResult.status == "failed"
response_text == ""
failed observation exists
failed observation success is False
error text includes "fake LLM failure"
activity sequence includes fail_process_instance
error object exists
process_instance object exists
fail_process_instance --observed_error--> error
error --error_from_process--> process_instance
duplicate relation validation valid=True
OCPX loads failed process_instance view
PIGService analyzes failed process view
failed_process_instance diagnostic exists
```

Regression tests still expected to pass:

```text
tests/test_process_run_loop.py
tests/test_process_instance_runtime.py
tests/test_agent_runtime_ocel_shape.py
tests/test_ocel_store.py
tests/test_time_utility.py
tests/test_ocpx_foundation.py
tests/test_pig_foundation.py
tests/test_imports.py
```

## 18. Scripts

New script:

```text
scripts/test_process_run_loop_failure.py
```

It does not require LM Studio.

It prints:

```text
status
observations
activity_sequence
duplicate relation validation
```

Expected output includes:

```text
status: failed
success: False
failure_stage: call_llm
exception_type: RuntimeError
fail_process_instance
duplicate_relations valid=True
```

Existing scripts:

```text
scripts/test_process_run_loop.py
scripts/test_agent_runtime.py
scripts/test_ocel_runtime.py
scripts/test_ocpx_loader.py
scripts/test_pig_imports.py
scripts/test_llm_client.py
```

`scripts/test_llm_client.py` depends on LM Studio/provider state.

## 19. Validation commands

Install:

```text
.\.venv\Scripts\python.exe -m pip install -e .
```

Unit tests:

```text
.\.venv\Scripts\python.exe -m pytest tests\test_imports.py tests\test_ocel_store.py tests\test_time_utility.py tests\test_process_run_loop.py tests\test_process_run_loop_failure.py tests\test_process_instance_runtime.py tests\test_agent_runtime_ocel_shape.py tests\test_ocpx_foundation.py tests\test_pig_foundation.py
```

Scripts:

```text
.\.venv\Scripts\python.exe scripts\test_process_run_loop.py
.\.venv\Scripts\python.exe scripts\test_process_run_loop_failure.py
.\.venv\Scripts\python.exe scripts\test_agent_runtime.py
.\.venv\Scripts\python.exe scripts\test_ocel_runtime.py
.\.venv\Scripts\python.exe scripts\test_ocpx_loader.py
.\.venv\Scripts\python.exe scripts\test_pig_imports.py
```

Optional:

```text
.\.venv\Scripts\python.exe scripts\test_llm_client.py
```

If LM Studio is not running, LLM script failure should be treated as environment failure.

## 20. Git hygiene

Generated files remain ignored.

Required ignore coverage:

```text
.env
.env.*
!.env.example
.venv/
data/
*.sqlite
*.sqlite3
.pytest_cache/
.pytest-tmp/
__pycache__/
*.pyc
src/chanta_core.egg-info/
```

Checks:

```text
git status --short
git status --ignored --short data .pytest-tmp
git ls-files | findstr "data"
git ls-files | findstr ".sqlite"
git ls-files | findstr ".env"
```

Expected:

```text
data/ ignored
.pytest-tmp/ ignored
no tracked data
no tracked sqlite
only .env.example tracked among env files
```

## 21. Restore checklist

Failure path:

```text
PASS: LLM exception is recorded before raise/return.
PASS: ProcessObservation(success=False) is created.
PASS: ProcessRunState.status becomes failed.
PASS: ProcessRunResult(status="failed") is supported.
PASS: raise_on_failure=False test path works.
PASS: raise_on_failure=True default behavior is preserved.
```

OCEL:

```text
PASS: fail_process_instance event_activity is recorded.
PASS: error object is created.
PASS: fail_process_instance --observed_error--> error.
PASS: error --error_from_process--> process_instance.
PASS: duplicate relation validation returns valid=True.
```

Evaluation:

```text
PASS: result_attrs.success is True/False.
PASS: evaluation_mode is runtime_basic.
PASS: observation_count is recorded.
PASS: failure result_attrs include error, exception_type, failure_stage.
```

OCPX/PIG:

```text
PASS: OCPX failed process view loads.
PASS: activity_sequence includes fail_process_instance.
PASS: PIGService does not crash on failed/recent view.
PASS: failed_process_instance diagnostic is produced for failed process view.
```

Regression:

```text
PASS: existing success path tests pass.
PASS: fake LLM success test passes.
PASS: fake LLM failure test passes.
PASS: unit tests do not require LM Studio.
PASS: generated files are ignored.
```

## 22. Known limitations

Still not implemented:

- retry policy
- retry count
- exponential backoff
- tool dispatch
- permission gate
- worker queue
- subagent delegation
- multi-iteration planning
- context compaction
- persisted observation object
- LLM evaluator
- scoring model
- full PIG graph reasoning
- full OCPX process mining engine
- pm4py/ocpa conformance

## 23. Recommended next version

Recommended next version:

```text
ChantaCore v0.5.2 - ProcessRunLoop Failure Query & Diagnostics
```

Reason:

v0.5.1 records failures correctly. The next safe step is to improve read/query/diagnostic support
around failures without adding tools or workers yet.

Candidate scope:

- query recent failed process instances
- query error objects by process_instance
- PIG guide section for failure stage distribution
- script for listing failed runs
- avoid duplicate fixed process_instance IDs in failure demo script

Alternative next version:

```text
ChantaCore v0.6.0 - Multi-Iteration Preparation
```

Only choose v0.6 if failure query/read-model confidence is sufficient.

## 24. Final conclusion

ChantaCore v0.5.1 hardens the ProcessRunLoop failure path without expanding autonomy.
It ensures that failed LLM execution still produces a structured failed observation, failed result,
OCEL `fail_process_instance` event, `error` object, error-process relation, and OCPX/PIG-readable
failure trace.

It does not add retry, tool dispatch, worker queues, permissions, subagents, or multi-iteration
planning. That restraint is intentional: v0.5.1 makes the one-iteration loop safer before the
runtime becomes more capable.

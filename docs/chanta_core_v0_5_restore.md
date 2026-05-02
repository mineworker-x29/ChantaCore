# ChantaCore v0.5 Restore - ProcessRunLoop Runtime

작성일: 2026-05-02
작성자: Vera
대상 버전: ChantaCore v0.5.0
버전 이름: ProcessRunLoop Runtime

이 문서는 ChantaCore v0.5.0을 복원하거나 리뷰할 때 기준으로 삼기 위한 restore
문서다. v0.5는 v0.4의 `process_instance`와 `skill:llm_chat` trace ontology 위에
bounded runtime loop를 추가한다.

## 1. 버전 목적

v0.5의 목적은 단일 `process_instance`를 전진시키는 canonical runtime loop를 도입하는
것이다.

v0.4에서는 AgentRuntime이 prompt assembly, skill selection, skill execution trace,
LLM call, response, outcome, process completion까지 직접 수행했다.

v0.5에서는 이 직접 실행 구간을 `ProcessRunLoop`로 분리한다.

새 실행 구조:

```text
AgentRuntime.run(...)
  -> create ExecutionContext
  -> record receive_user_request
  -> record start_process_instance
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
  -> AgentRunResult
```

## 2. Non-goals

v0.5에서 의도적으로 구현하지 않는 것:

```text
MissionLoop
GoalLoop
worker queue
task queue
full skill marketplace
tool runtime
permission system
context compaction pipeline
subagent delegation
streaming AsyncGenerator
MCP/plugin execution
Claude Code feature clone
```

v0.5는 loop skeleton이지만, 실제로 OCEL persistence까지 연결된 bounded runtime이다.

## 3. Architecture inspiration

v0.5는 Claude Code의 loop pattern을 참고한다.

참고한 개념:

- single shared loop
- mutable loop state
- context assembly before model call
- runtime/harness-controlled execution
- observation/result collection
- stop condition
- persistence throughout loop

복제하지 않은 개념:

- shell sandbox
- permission prompt system
- streaming loop protocol
- MCP/plugin system
- tool marketplace
- subagent delegation
- compaction pipeline

따라서 v0.5는 Claude Code를 복제한 것이 아니라, loop architecture pattern만 ChantaCore
process runtime에 맞게 단순화한 것이다.

## 4. Runtime loop package

v0.5에서 추가된 package:

```text
src/chanta_core/runtime/loop/
  __init__.py
  process_run_loop.py
  state.py
  result.py
  decider.py
  policy.py
  context.py
  observation.py
```

각 파일 역할:

```text
process_run_loop.py  - canonical bounded loop runtime
state.py             - mutable ProcessRunState
result.py            - ProcessRunResult
decider.py           - v0.5 next activity decider
policy.py            - loop bound and stop condition
context.py           - LLM chat context assembler
observation.py       - ProcessObservation
```

## 5. ProcessRunState

`ProcessRunState`는 mutable dataclass다. loop가 소유하고 iteration마다 갱신한다.

Fields:

```text
process_instance_id
session_id
agent_id
status
iteration
max_iterations
current_activity
selected_skill_id
observations
last_error
state_attrs
```

상태 lifecycle:

```text
created/running -> completed
created/running -> failed
```

v0.5 구현에서는 loop 시작 시 `status="running"`으로 만들고, 성공 시 `"completed"`,
실패 시 `"failed"`로 변경한다.

## 6. ProcessRunPolicy

`ProcessRunPolicy`가 bounded loop를 보장한다.

Default values:

```text
max_iterations = 1
stop_on_text_response = True
fail_on_exception = True
```

Continuation rule:

```text
state.status == "running" and state.iteration < state.max_iterations
```

Stop-after-observation rule:

```text
if state.iteration >= state.max_iterations: stop
if stop_on_text_response and observation.success and observation.output_text: stop
```

따라서 기본 v0.5 loop는 one-iteration bounded loop다. 정상 응답이 오면 observation을
남기고 종료한다.

## 7. ProcessActivityDecider

v0.5 decider는 planner가 아니다. LLM planner도 아니다.

Rule:

```text
if iteration == 0:
    return "execute_skill"
else:
    return "complete_process_instance"
```

현재 loop는 첫 iteration에서 `skill:llm_chat`을 실행한다.

## 8. ProcessContextAssembler

`ProcessContextAssembler`는 LLM chat call 전 context를 구성한다.

Current behavior:

```text
system prompt가 있으면 system message 추가
user_input을 user message로 추가
```

주의:

v0.5 구현은 단순화를 위해 `PromptAssemblyService`와 완전히 통합되어 있지는 않다.
향후 prompt assembly logic이 복잡해지면 v0.6 이후에 `PromptAssemblyService`와
통합하거나 delegation 구조를 정리하는 것이 좋다.

## 9. ProcessObservation

`ProcessObservation`은 loop가 실행 결과를 수집하는 read/write boundary다.

Fields:

```text
activity
success
output_text
output_attrs
error
```

v0.5 success path observation 예:

```text
activity = "execute_skill"
success = True
output_text = "<LLM response>"
output_attrs = {
  "skill_id": "skill:llm_chat",
  "iteration": 0
}
error = None
```

observation은 `state.observations`에 dict로 쌓이고, `ProcessRunResult.observations`에도
typed dataclass로 반환된다.

## 10. ProcessRunResult

`ProcessRunResult`는 loop-level result다.

Fields:

```text
process_instance_id
session_id
agent_id
status
response_text
observations
result_attrs
```

`AgentRuntime`은 이 result를 받아 기존 compatibility surface인 `AgentRunResult`로
감싼다.

## 11. ProcessRunLoop success path

v0.5 success path:

```text
1. Create ProcessRunState
2. record_process_run_loop_started
3. while policy.should_continue(state):
4.   decide_next_activity
5.   record_next_activity_decided
6.   select skill:llm_chat
7.   record_skill_selected
8.   record_skill_executed
9.   assemble context
10.  record_context_assembled
11.  record_llm_call_started
12.  LLMClient.chat_messages(...)
13.  record_llm_response_received
14.  create ProcessObservation
15.  record_result_observed
16.  append observation to state
17.  increment iteration
18.  stop if policy says stop
19. record_outcome_recorded
20. record_process_instance_completed
21. return ProcessRunResult
```

중요한 점:

- LLM 호출은 model-generated tool call이 아니다.
- runtime harness인 `ProcessRunLoop`가 직접 `LLMClient.chat_messages(...)`를 호출한다.
- skill execution은 현재 `skill:llm_chat` ontology로 trace되는 runtime-controlled action이다.

## 12. ProcessRunLoop failure path

예외 발생 시:

```text
state.status = "failed"
state.last_error = str(error)
record_process_instance_failed(...)
if fail_on_exception:
    raise
else:
    return failed ProcessRunResult
```

`AgentRuntime` compatibility behavior는 LLM exception을 re-raise하는 것이다.

## 13. OCEL event_activity additions

v0.5에서 추가된 stable event activities:

```text
start_process_run_loop
decide_next_activity
assemble_context
observe_result
```

v0.4에서 유지되는 activities:

```text
receive_user_request
start_process_instance
select_skill
execute_skill
call_llm
receive_llm_response
record_outcome
complete_process_instance
fail_process_instance
```

v0.5 AgentRuntime full sequence:

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

Numbered activity는 만들지 않는다.

금지:

```text
task_1
task_2
step_1
execute_skill_1
execute_skill_2
```

## 14. TraceService additions

v0.5에서 `TraceService`에 추가된 methods:

```text
record_process_run_loop_started
record_next_activity_decided
record_context_assembled
record_result_observed
```

이 methods는 `OCELFactory`를 통해 OCELRecord를 만들고 `OCELStore`에 append한다.
동시에 기존 compatibility를 위해 `AgentEvent`를 반환하고 JSONL raw/debug mirror에도 남길 수 있다.

## 15. OCELFactory additions

v0.5에서 `OCELFactory`에 추가된 methods:

```text
start_process_run_loop
decide_next_activity
assemble_context
observe_result
```

각 method는 다음 공통 relations를 포함한다.

```text
process_context -> process_instance
session_context -> session
acting_agent -> agent
```

그리고 process instance 기본 object-object relations를 유지한다.

```text
user_request --belongs_to_session--> session
process_instance --derived_from_request--> user_request
process_instance --handled_in_session--> session
process_instance --executed_by_agent--> agent
```

skill 관련 event는 `skill:llm_chat`과 연결된다.

```text
selected_skill -> skill:llm_chat
executed_skill -> skill:llm_chat
process_instance --uses_skill--> skill:llm_chat
```

## 16. AgentRuntime integration

v0.5 `AgentRuntime.run(...)` 역할:

```text
1. ExecutionContext 생성
2. process_instance_id 결정
3. receive_user_request 기록
4. start_process_instance 기록
5. ProcessRunLoop 생성 또는 주입된 loop 사용
6. loop.run(...) 호출
7. loop.events를 AgentRunResult.events에 포함
8. response_text 반환
```

`AgentRuntime`이 더 이상 직접 수행하지 않는 것:

```text
PromptAssemblyService.assemble 직접 호출
skill selection 직접 호출
LLMClient.chat_messages 직접 호출
outcome 직접 기록
completion 직접 기록
```

이 작업들은 loop 내부로 이동했다.

## 17. OCPX compatibility

OCPX는 v0.5 loop activities를 그대로 읽는다.

주요 API:

```text
OCPXLoader.load_process_instance_view(process_instance_id)
OCPXLoader.load_recent_view(limit)
OCPXLoader.load_session_view(session_id)
OCPXEngine.activity_sequence(view)
```

`activity_sequence(view)`는 `event.event_activity` list를 반환한다.

v0.5 process_instance view 예:

```text
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

`receive_user_request`는 process_context relation이 없는 경우 session view에는 포함되지만
process_instance view에는 포함되지 않을 수 있다. 이는 receive event가 primary request/session
context 중심 event이기 때문이다.

## 18. PIG compatibility

Public names remain:

```text
PIGBuilder
PIGService
```

Do not reintroduce:

```text
PIGGraphBuilder
PIGGuideService
```

v0.5 guide additions:

```text
activity_sequence
process_instance_count
skill_usage_count
selected_skills
observation_count
loop_iteration_count
```

PIG remains a foundational graph/guide layer. It does not yet run full graph reasoning or
process mining algorithms.

## 19. Tests

v0.5 core tests:

```text
tests/test_process_run_loop.py
tests/test_process_instance_runtime.py
tests/test_agent_runtime_ocel_shape.py
tests/test_imports.py
tests/test_ocel_store.py
tests/test_time_utility.py
tests/test_ocpx_foundation.py
tests/test_pig_foundation.py
```

`tests/test_process_run_loop.py` uses fake LLM and temp OCELStore. It asserts:

```text
ProcessRunResult.status == "completed"
response_text == "Hello from loop."
len(observations) == 1
observation.success is True
event activities include the loop sequence
duplicate relation validation valid=True
```

`tests/test_agent_runtime_ocel_shape.py` asserts AgentRuntime now emits:

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

## 20. Scripts

v0.5 script additions:

```text
scripts/test_process_run_loop.py
```

It prints:

```text
response_text
session_id
process_instance_id
activity_sequence
duplicate_relations
```

Existing scripts expected to continue working:

```text
scripts/test_agent_runtime.py
scripts/test_ocel_runtime.py
scripts/test_ocpx_loader.py
scripts/test_pig_imports.py
scripts/test_llm_client.py
```

## 21. Validation commands

Acceptance commands:

```text
.\.venv\Scripts\python.exe -m pip install -e .

.\.venv\Scripts\python.exe -m pytest tests\test_imports.py tests\test_ocel_store.py tests\test_time_utility.py tests\test_process_run_loop.py tests\test_process_instance_runtime.py tests\test_agent_runtime_ocel_shape.py tests\test_ocpx_foundation.py tests\test_pig_foundation.py

.\.venv\Scripts\python.exe scripts\test_process_run_loop.py
.\.venv\Scripts\python.exe scripts\test_agent_runtime.py
.\.venv\Scripts\python.exe scripts\test_ocel_runtime.py
.\.venv\Scripts\python.exe scripts\test_ocpx_loader.py
.\.venv\Scripts\python.exe scripts\test_pig_imports.py
```

Optional when LM Studio is running:

```text
.\.venv\Scripts\python.exe scripts\test_llm_client.py
```

## 22. Restore checklist

When restoring v0.5, verify:

```text
PASS: ProcessRunLoop exists.
PASS: AgentRuntime calls ProcessRunLoop.
PASS: ProcessTraceLoop does not exist.
PASS: MissionLoop does not exist.
PASS: GoalLoop does not exist.
PASS: ProcessRunState is mutable.
PASS: ProcessRunPolicy.max_iterations defaults to 1.
PASS: should_continue uses iteration < max_iterations.
PASS: ProcessActivityDecider chooses execute_skill on iteration 0.
PASS: skill:llm_chat is selected and executed.
PASS: LLMClient.chat_messages is called by runtime harness.
PASS: observation is appended to state.
PASS: observe_result is persisted.
PASS: record_outcome is persisted.
PASS: complete_process_instance is persisted.
PASS: OCELEvent uses event_activity.
PASS: OCELObject uses object_attrs.
PASS: timestamps use utc_now_iso.
PASS: OCPX activity_sequence includes loop activities.
PASS: PIGService works.
PASS: PIGBuilder/PIGService names remain unchanged.
PASS: generated SQLite/data files are ignored.
```

## 23. Git hygiene

Generated files must remain ignored:

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
git status --ignored --short data .pytest-tmp
git ls-files | findstr "data"
git ls-files | findstr ".sqlite"
git ls-files | findstr ".env"
```

Expected:

```text
data/ ignored
.pytest-tmp/ ignored
no tracked SQLite
no tracked data
only .env.example tracked among env files
```

## 24. Known limitations

v0.5 remains deliberately small.

Not implemented:

- multi-iteration planning
- tool dispatch
- permission gate
- context compaction
- subagent delegation
- worker queue
- worker runtime
- task queue
- skill marketplace
- process variant mining
- full OCPX computation engine
- full PIG graph reasoning
- full pm4py/ocpa conformance

## 25. Recommended next version

The next reasonable version should not jump straight to full autonomy.

Recommended v0.6 direction:

```text
ChantaCore v0.6 - Loop Failure Handling & Multi-Iteration Preparation
```

Candidate scope:

- explicit retry policy
- failed observation modeling
- max_iterations > 1 test path
- stop reason fields
- cleaner ProcessContextAssembler delegation to PromptAssemblyService
- richer OCPX process_instance view for loop iterations
- PIG diagnostics for failed/incomplete loops

Do not add worker queue, tool runtime, subagent delegation, or complex process mining until
the bounded loop state model is stable.

## 26. Final conclusion

ChantaCore v0.5 is the version where execution moves from direct AgentRuntime LLM execution
to a bounded `ProcessRunLoop`. The loop is intentionally one-iteration by default, but it is
real runtime code: it owns mutable state, selects and executes `skill:llm_chat`, calls the LLM
through the harness, records an observation, applies a stop condition, and persists every major
transition into OCEL.

It is not a MissionLoop, GoalLoop, worker system, tool runtime, or Claude Code clone. It is the
minimal process runtime skeleton needed before those future layers can be added safely.

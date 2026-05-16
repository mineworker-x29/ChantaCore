# ChantaCore v0.4 Restore - ProcessInstance & Skill Trace Ontology

작성일: 2026-05-02
작성자: ChantaCore Maintainers
대상 버전: ChantaCore v0.4.0
버전 이름: ProcessInstance & Skill Trace Ontology

이 문서는 ChantaCore v0.4.0을 재구성하거나 설계 판단을 복원할 때
참조하기 위한 restore 문서다. 단순 변경 노트가 아니라, v0.4에서 어떤
ontology 결정을 했고 어떤 실행 경로가 안정화되었는지, 그리고 어떤
것을 의도적으로 구현하지 않았는지를 기록한다.

## 1. 버전 목적

v0.4의 목적은 v0.3.2의 OCEL canonical model alignment 위에
`process_instance` 중심의 실행 ontology를 세우는 것이었다.

v0.3.2까지는 OCEL-oriented canonical event/object/relation 모델을
정리했고, v0.4에서는 그 모델 위에서 실제 AgentRuntime 실행을 하나의
object-centric process case로 표현하도록 정리했다.

핵심 변화는 다음과 같다.

- `mission`과 `goal`을 별도 active object type으로 만들지 않는다.
- 하나의 사용자 요청 실행을 `process_instance` object로 표현한다.
- mission/goal/objective 의미는 `process_instance.object_attrs`에 저장한다.
- 각 실행 단계는 numbered task/step object가 아니라 stable `event_activity`
  event instance로 표현한다.
- 현재 LLM 응답 경로를 첫 번째 skill object인 `skill:llm_chat`의 선택과 실행으로
  trace한다.

## 2. v0.4 이전 상태

v0.3.2 기준 ChantaCore에는 다음 기반이 있었다.

- OCEL canonical model:
  - `OCELEvent(event_id, event_activity, event_timestamp, event_attrs)`
  - `OCELObject(object_id, object_type, object_attrs)`
  - `OCELRelation(relation_kind, source_id, target_id, qualifier, relation_attrs)`
- SQLite canonical persistence:
  - `event`
  - `object`
  - `event_object`
  - `object_object`
  - `chanta_event_payload`
  - `chanta_object_state`
  - relation extension tables
- relation hygiene:
  - logical uniqueness indexes
  - relation insert dedupe
  - duplicate relation validation
- OCPX lightweight read model
- PIGBuilder/PIGService foundation

v0.4는 여기에 runtime ontology를 붙였다.

## 3. 핵심 설계 결정

### 3.1 process_instance를 canonical case anchor로 사용

v0.4에서 하나의 executable case/process anchor는 `process_instance`다.

예시 object:

```text
object_id = process_instance:<short_hash>
object_type = process_instance
object_attrs = {
  "object_key": "process_instance:<short_hash>",
  "display_name": "Interactive user request process",
  "process_kind": "interactive_user_request",
  "source_type": "user_request",
  "mission_text": null,
  "goal_text": "Answer the user's request",
  "objective_text": "<user input>",
  "status": "running|completed|failed",
  "created_at": "...Z",
  "updated_at": "...Z"
}
```

이 결정의 이유는 mission, goal, objective가 v0.4 단계에서는 서로 겹치는
purpose/objective 개념이기 때문이다. 이를 모두 별도 object type으로 active 생성하면
초기 ontology가 과하게 분리되고, 실제 runtime path가 필요 이상으로 복잡해진다.

따라서 v0.4에서는 process instance가 실행 단위이고, mission/goal/objective는
그 process instance의 속성으로 남는다.

### 3.2 mission / goal active object를 만들지 않음

v0.4에서 다음 object type은 active runtime path에서 만들지 않는다.

```text
mission
goal
task_instance
step_instance
```

`mission` type은 넓은 vocabulary나 placeholder에는 남을 수 있지만,
AgentRuntime 실행 중 active object로 생성하지 않는다.

검증 기준:

- `OCELFactory`에서 `object_type="mission"` 생성 없음
- `OCELFactory`에서 `object_type="goal"` 생성 없음
- `OCELFactory`에서 `object_type="task_instance"` 생성 없음
- `OCELFactory`에서 `object_type="step_instance"` 생성 없음

### 3.3 step은 event instance로 표현

v0.4는 task/step instance object를 만들지 않는다.

각 실행 단계는 다음처럼 표현한다.

- event instance identity: `event_id`
- process activity label: `event_activity`
- process/case context: event-object relation
  - event `--process_context-->` process_instance

따라서 numbered activity를 만들지 않는다.

금지 예시:

```text
task_1
task_2
step_1
execute_skill_1
execute_skill_2
```

## 4. v0.4 event_activity taxonomy

v0.4 AgentRuntime의 canonical event sequence는 다음과 같다.

```text
receive_user_request
start_process_instance
assemble_prompt
select_skill
execute_skill
call_llm
receive_llm_response
record_outcome
complete_process_instance
```

각 activity는 reusable process activity label이다.

### 4.1 receive_user_request

사용자 입력을 runtime이 받았음을 기록한다.

주요 object:

- `user_request`
- `session`
- `agent`
- `process_instance`

주요 event-object relations:

```text
primary_request -> user_request
session_context -> session
acting_agent -> agent
```

### 4.2 start_process_instance

사용자 요청을 처리하기 위한 process instance를 시작한다.

주요 event-object relations:

```text
process_context -> process_instance
primary_request -> user_request
session_context -> session
acting_agent -> agent
```

### 4.3 assemble_prompt

기존 `PromptAssemblyService`가 system/user messages를 구성한다.

주요 object:

- `prompt`
- `process_instance`
- `session`
- `agent`

주요 relations:

```text
assembled_prompt -> prompt
request_to_prompt
```

### 4.4 select_skill

현재 LLM 응답 경로에 사용할 skill을 선택한다.

v0.4의 built-in skill:

```text
object_id = skill:llm_chat
object_type = skill
skill_name = llm_chat
execution_type = llm
```

주요 relation:

```text
selected_skill -> skill:llm_chat
process_instance --uses_skill--> skill:llm_chat
```

### 4.5 execute_skill

선택된 `skill:llm_chat` 실행을 기록한다.

이 단계는 아직 복잡한 skill executor나 marketplace를 의미하지 않는다. v0.4에서는
기존 LLM path를 skill ontology로 감싼 것이다.

주요 relation:

```text
executed_skill -> skill:llm_chat
process_instance --uses_skill--> skill:llm_chat
```

### 4.6 call_llm

LLM provider/model 호출 시작을 기록한다.

주요 object:

- `llm_call`
- `provider`
- `llm_model`

주요 relations:

```text
llm_call -> llm_call:<uuid>
used_provider -> provider:<provider>
used_model -> model:<hash>
```

### 4.7 receive_llm_response

LLM 응답 수신을 기록한다.

주요 object:

- `llm_response`
- `llm_call`

주요 relation:

```text
generated_response -> response:<uuid>
llm_call_to_response
```

### 4.8 record_outcome

runtime outcome object를 만든다.

주요 object:

- `outcome`

주요 relation:

```text
produced_outcome -> outcome:<uuid>
outcome --outcome_of_process--> process_instance
```

### 4.9 complete_process_instance

process instance를 completed 상태로 마감한다.

주요 relation:

```text
process_context -> process_instance
produced_outcome -> outcome:<uuid>
```

## 5. Object-object relations

v0.4의 핵심 object-object relations:

```text
user_request --belongs_to_session--> session
process_instance --derived_from_request--> user_request
process_instance --handled_in_session--> session
process_instance --executed_by_agent--> agent
process_instance --uses_skill--> skill:llm_chat
outcome --outcome_of_process--> process_instance
```

이 relation들은 process_instance-centered view와 future process intelligence layer의
기초가 된다.

## 6. Skill foundation

v0.4에서 skill package는 minimal foundation이다.

주요 파일:

```text
src/chanta_core/skills/skill.py
src/chanta_core/skills/registry.py
src/chanta_core/skills/builtin.py
```

`Skill` dataclass:

```text
skill_id
skill_name
description
execution_type
input_schema
output_schema
skill_attrs
```

Built-in skill:

```text
skill_id = "skill:llm_chat"
skill_name = "llm_chat"
execution_type = "llm"
skill_attrs = {
  "provider_mode": "configured",
  "is_builtin": true
}
```

v0.4의 중요한 한계:

- skill marketplace가 아니다.
- tool runtime이 아니다.
- permission system이 아니다.
- LLM call을 skill execution ontology로 trace하는 단계다.

## 7. AgentRuntime v0.4 path

v0.4 기준 실행 흐름:

```text
AgentRuntime.run(...)
  -> ExecutionContext.create(...)
  -> TraceService.record_user_request_received(...)
  -> TraceService.record_process_instance_started(...)
  -> PromptAssemblyService.assemble(...)
  -> TraceService.record_prompt_assembled(...)
  -> SkillRegistry.get_builtin_llm_chat()
  -> TraceService.record_skill_selected(...)
  -> TraceService.record_skill_executed(...)
  -> TraceService.record_llm_call_started(...)
  -> LLMClient.chat_messages(...)
  -> TraceService.record_llm_response_received(...)
  -> TraceService.record_outcome_recorded(...)
  -> TraceService.record_process_instance_completed(...)
  -> AgentRunResult
```

v0.5에서 이 직접 실행 부분은 `ProcessRunLoop`로 이동한다. 하지만 v0.4 restore 관점에서는
위 경로가 기준이다.

## 8. TraceService v0.4 responsibilities

`TraceService`는 compatibility `AgentEvent`를 반환하면서 canonical persistence는
OCELStore에 맡긴다.

주요 public methods:

```text
record_user_request_received
record_process_instance_started
record_prompt_assembled
record_skill_selected
record_skill_executed
record_llm_call_started
record_llm_response_received
record_outcome_recorded
record_process_instance_completed
record_process_instance_failed
```

Backward-compatible aliases:

```text
record_run_started
record_run_completed
record_run_failed
```

이 aliases는 legacy script/test compatibility를 위한 것이며, canonical OCEL activity는
process_instance vocabulary를 따른다.

## 9. OCEL canonical model 유지

v0.4에서도 v0.3.2의 canonical shape를 유지한다.

`OCELEvent`:

```text
event_id
event_activity
event_timestamp
event_attrs
```

`OCELObject`:

```text
object_id
object_type
object_attrs
```

`OCELRelation`:

```text
relation_kind
source_id
target_id
qualifier
relation_attrs
```

SQLite는 event-object relation과 object-object relation을 계속 분리한다.

```text
event_object
object_object
chanta_event_object_relation_ext
chanta_object_object_relation_ext
```

## 10. Timestamp policy

모든 runtime timestamp는 다음 utility를 사용한다.

```text
chanta_core.utility.time.utc_now_iso()
```

규칙:

- timezone-aware UTC
- ISO-8601
- trailing `Z`
- `datetime.utcnow()` 사용 금지
- naive `datetime.now()` 사용 금지

## 11. OCPX updates

v0.4에서 OCPX는 process_instance-centered read view를 읽을 수 있다.

추가/주요 API:

```text
OCPXLoader.load_process_instance_view(process_instance_id)
OCPXLoader.load_session_process_instances(session_id)
OCPXEngine.activity_sequence(view)
OCPXEngine.summarize_process_instance_view(view)
```

`load_process_instance_view`는 `process_context` relation을 기준으로 관련 event들을 읽는다.

## 12. PIG updates

v0.4에서 public naming은 다음으로 고정한다.

```text
PIGBuilder
PIGService
```

사용하지 않는 이름:

```text
PIGGraphBuilder
PIGGuideService
```

`PIGService` entrypoints:

```text
analyze_recent(limit)
analyze_session(session_id)
analyze_process_instance(process_instance_id)
```

## 13. Tests and scripts

v0.4에서 기대한 핵심 테스트:

```text
tests/test_imports.py
tests/test_ocel_store.py
tests/test_time_utility.py
tests/test_agent_runtime_ocel_shape.py
tests/test_process_instance_runtime.py
tests/test_ocpx_foundation.py
tests/test_pig_foundation.py
```

핵심 runtime scripts:

```text
scripts/test_agent_runtime.py
scripts/test_ocel_runtime.py
scripts/test_ocpx_loader.py
scripts/test_pig_imports.py
scripts/test_process_instance_runtime.py
```

## 14. Restore checklist

v0.4를 복원할 때 다음을 확인한다.

```text
PASS: process_instance object type is used.
PASS: mission object is not actively created.
PASS: goal object is not actively created.
PASS: task_instance is not actively created.
PASS: step_instance is not actively created.
PASS: mission_text/goal_text/objective_text are process_instance.object_attrs.
PASS: skill:llm_chat exists.
PASS: select_skill is related to skill:llm_chat.
PASS: execute_skill is related to skill:llm_chat.
PASS: outcome is related to process_instance.
PASS: duplicate relation validation returns valid=True.
PASS: OCPX can load process_instance view.
PASS: PIGService can analyze process_instance/recent/session view.
```

## 15. Known limitations

v0.4 does not implement:

- ProcessRunLoop
- worker runtime
- worker queue
- task queue
- full skill execution framework
- permission gate
- tool runtime
- subagent delegation
- process mining algorithm
- pm4py/ocpa conformance

v0.4 is ontology alignment and trace foundation, not an autonomous agent loop.

## 16. Migration notes

If `data/ocel/chanta_core_ocel.sqlite` contains older v0.3 records, recent views may show
older `goal` or `assemble_prompt` events. Clean tests should use temp DBs. Because `data/`
is ignored and this is a development runtime, deleting the local development SQLite DB and
rerunning scripts is acceptable when schema/history confusion appears.

Do not auto-drop or destructively migrate DBs in runtime code.

## 17. Final conclusion

ChantaCore v0.4 is the version where runtime trace ontology moves from generic agent run
events to `process_instance` and `skill:llm_chat` centered object-centric execution records.
It intentionally avoids MissionLoop, GoalLoop, worker queues, task objects, and tool runtime.
The result is a clean process-instance foundation for v0.5's ProcessRunLoop.

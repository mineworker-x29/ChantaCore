# ChantaCore v0.4 Note

작성일: 2026-05-02
작성자: Vera
대상 버전: ChantaCore v0.4.0 - ProcessInstance & Skill Trace Ontology

## 목적

v0.4는 v0.3.2의 OCEL canonical model을 유지하면서 runtime trace ontology를 `process_instance` 중심으로 정리한 버전이다.

## 핵심 결정

v0.4에서는 mission과 goal을 별도 OCEL object type으로 적극 생성하지 않는다.

대신 단일 executable case/process anchor로 `process_instance` object를 사용한다. mission, goal, objective에 해당하는 정보는 `process_instance.object_attrs`에 저장한다.

예:

```text
mission_text
goal_text
objective_text
process_kind
source_type
status
```

각 process step은 event instance로 표현한다. instance 식별은 `event_id`가 담당하고, reusable process activity class는 `event_activity`가 담당한다.

## v0.4 Event Activity

basic AgentRuntime path의 canonical activity sequence:

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

번호형 activity나 instance-specific activity는 만들지 않는다.

```text
task_1
task_2
step_1
execute_skill_1
execute_skill_2
```

위 형태는 사용하지 않는다.

## Skill Foundation

v0.4의 첫 capability object는 `skill:llm_chat`이다.

```text
object_id = skill:llm_chat
object_type = skill
skill_name = llm_chat
execution_type = llm
```

현재 AgentRuntime은 실제 복잡한 skill execution framework를 만들지 않고, 기존 LLM response path를 `skill:llm_chat`의 선택과 실행으로 trace한다.

## Process Relations

대표 object-object relation:

```text
process_instance --derived_from_request--> user_request
process_instance --handled_in_session--> session
process_instance --executed_by_agent--> agent
process_instance --uses_skill--> skill:llm_chat
outcome --outcome_of_process--> process_instance
```

대표 event-object relation:

```text
process_context -> process_instance
primary_request -> user_request
session_context -> session
acting_agent -> agent
selected_skill -> skill:llm_chat
executed_skill -> skill:llm_chat
llm_call -> llm_call:<uuid>
generated_response -> response:<uuid>
produced_outcome -> outcome:<uuid>
```

## OCPX/PIG

OCPXLoader는 process_instance-centered view를 읽을 수 있다.

```text
load_process_instance_view(process_instance_id)
load_session_process_instances(session_id)
```

OCPXEngine은 activity sequence와 process_instance summary helper를 제공한다.

PIGService는 process_instance, session, recent view 분석 entrypoint를 제공한다.

```text
analyze_process_instance(process_instance_id)
analyze_session(session_id)
analyze_recent(limit)
```

## 남은 제한

worker runtime은 아직 없다.
task queue는 아직 없다.
full skill execution framework는 아직 없다.
full process mining algorithm은 아직 없다.
full pm4py/ocpa conformance를 주장하지 않는다.

## 결론

ChantaCore v0.4는 mission/goal/task/step runtime을 늘리는 대신, `process_instance`와 `skill:llm_chat`을 중심으로 AgentRuntime trace를 정렬한 process ontology foundation 버전이다.

# ChantaCore v0.3.2 Restore Notes

작성일: 2026-05-02
작성자: ChantaCore Maintainers
대상 버전: ChantaCore v0.3.2 - OCEL Canonical Model Alignment & Execution Ontology

## 1. 목적

v0.3.2는 v0.3/v0.3.1에서 구축한 OCEL-oriented runtime trace foundation을 유지하면서, canonical event/object/relation 모델을 더 명확하게 정렬한 버전이다.

이 버전은 worker runtime, skill execution, mission runtime, memory runtime을 추가하지 않는다. 변경 범위는 OCEL canonical model alignment, execution ontology 정리, timestamp utility 중앙화, OCPX/PIG read model 호환성 유지다.

## 2. 핵심 모델 변경

`OCELEvent` canonical field는 다음으로 축소했다.

```text
event_id
event_activity
event_timestamp
event_attrs
```

`event_type`, `source_runtime`, `session_id`, `trace_id`, `actor_type`, `actor_id`, `status`는 canonical top-level field가 아니다. 필요한 경우 `event_attrs` 안에 `runtime_event_type`, `lifecycle`, `source_runtime`, `session_id`, `trace_id`, `actor_type`, `actor_id`로 저장한다.

`OCELObject` canonical field는 다음으로 축소했다.

```text
object_id
object_type
object_attrs
```

`object_key`, `display_name`, `created_at`, `updated_at`, object-specific state는 `object_attrs` 안에 저장한다.

Python relation model은 `OCELRelation`으로 통합했다.

```text
relation_kind
source_id
target_id
qualifier
relation_attrs
```

SQLite persistence는 여전히 `event_object`와 `object_object`를 분리한다. 즉 Python model은 통합했지만 OCEL metamodel의 relation 분리는 DB에서 유지된다.

## 3. 실행 온톨로지

event instance는 `event_id`로 식별한다.
object instance는 `object_id`로 식별한다.
activity label은 `event_activity`로 표현한다.

v0.3.2에서 basic AgentRuntime success path의 canonical activity는 다음이다.

```text
receive_user_request
start_goal
assemble_prompt
call_llm
receive_llm_response
complete_goal
```

AgentRunResult에 포함되는 legacy-compatible `AgentEvent.event_type`은 유지한다. 따라서 runtime result에는 `user_request_received`, `agent_run_started` 같은 compatibility event type이 남아 있을 수 있다. canonical OCEL persistence 기준은 `event_activity`다.

basic AgentRuntime path는 lightweight `goal` object를 추가한다.

대표 object relation:

```text
goal --derived_from_request--> user_request
goal --handled_in_session--> session
goal --executed_by_agent--> agent
```

## 4. SQLite 저장 정책

clean v0.3.2 DB의 operational table은 다음 field를 사용한다.

```text
chanta_event_payload:
  event_id
  event_activity
  event_timestamp
  event_attrs_json

chanta_object_state:
  object_id
  object_type
  object_attrs_json

chanta_event_object_relation_ext:
  event_id
  object_id
  qualifier
  relation_attrs_json

chanta_object_object_relation_ext:
  source_object_id
  target_object_id
  qualifier
  relation_attrs_json
```

표준형 table은 유지한다.

```text
event
object
event_object
object_object
event_map_type
object_map_type
```

`event.ocel_type`은 `event_activity`에 대응한다.
`object.ocel_type`은 `object_type`에 대응한다.

v0.3.1 relation hygiene은 유지한다.

```text
event_object unique key:
  event_id, object_id, qualifier

object_object unique key:
  source_object_id, target_object_id, qualifier
```

`INSERT OR IGNORE`와 `WHERE NOT EXISTS` guard도 유지한다.

## 5. Timestamp Utility

새 모듈:

```text
src/chanta_core/utility/time.py
```

제공 함수:

```python
utc_now_iso() -> str
```

요구사항:

- `datetime.now(UTC)` 사용
- timezone-aware UTC
- ISO-8601 string
- trailing `Z`
- `datetime.utcnow()` 사용 금지

`ExecutionContext`, `AgentEvent`, `OCELFactory`, `OCELStore`는 이 utility를 사용한다.

## 6. OCPX/PIG 호환성

OCPX event view는 `event_activity`, `event_timestamp`, `event_attrs`를 사용한다.

OCPX object view는 `object_attrs`를 사용한다.

`OCPXEngine.count_events_by_activity(...)`를 추가했고, 기존 `count_events_by_type(...)`는 compatibility alias로 activity count를 반환한다.

PIG public naming은 유지한다.

```text
PIGBuilder
PIGService
```

`PIGGraphBuilder`, `PIGGuideService` 이름은 사용하지 않는다.

## 7. Migration Note

v0.3.2는 destructive migration을 자동 수행하지 않는다.

기존 개발 DB에 v0.3/v0.3.1 column이 남아 있을 수 있다. `OCELStore.initialize()`는 새 v0.3.2 column을 추가하고, old NOT NULL column이 있는 개발 DB에도 새 insert가 가능하도록 compatibility write를 수행한다.

다만 clean v0.3.2 형태를 확인하려면 ignored `data/ocel/chanta_core_ocel.sqlite` 개발 DB를 삭제하고 재생성하는 것이 가장 단순하다. production-like data를 자동 삭제하지 않는다.

## 8. 검증

추가/수정된 주요 test:

```text
tests/test_ocel_store.py
tests/test_agent_runtime_ocel_shape.py
tests/test_time_utility.py
tests/test_ocpx_foundation.py
tests/test_pig_foundation.py
```

검증 대상:

- `OCELEvent` minimal canonical fields
- `OCELObject` minimal canonical fields
- `OCELRelation` unified relation dispatch
- duplicate relation hygiene 유지
- fake LLM 기반 AgentRuntime OCEL shape
- goal object와 goal relation
- UTC timestamp utility
- OCPX/PIG foundation compatibility

## 9. 남은 제한

v0.3.2는 full OCEL 2.0 JSON export/import conformance를 완성하지 않는다.

pm4py/ocpa compatibility는 future-facing 목표다.

worker event emission은 아직 없다.

skill runtime은 아직 없다.

full process mining algorithm은 아직 없다.

## 10. 결론

ChantaCore v0.3.2는 v0.3.1의 relation hygiene을 유지하면서, OCEL-oriented canonical model을 `event_activity`, `event_attrs`, `object_attrs`, `relation_attrs` 중심으로 정렬하고 basic runtime path에 lightweight goal object를 추가한 ontology alignment 버전이다.

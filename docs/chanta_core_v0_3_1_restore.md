# ChantaCore v0.3.1 Restore Notes

작성일: 2026-05-02
작성자: ChantaCore Maintainers
대상 버전: ChantaCore v0.3.1 - OCEL Relation Hygiene & Store Validation
대상 저장소: `<CHANTA_CORE_REPO>`

## 1. 문서 목적

이 문서는 ChantaCore v0.3.1에서 실제로 변경된 구현, 검증 결과, 남은 제한을 복원 가능한 수준으로 기록한다.

v0.3.1은 v0.3에서 만든 OCEL-oriented runtime trace foundation을 확장한 버전이다. 새 worker runtime, skill execution, mission runtime, memory runtime은 추가하지 않았다. 이번 버전의 범위는 기존 `AgentRuntime -> TraceService -> OCELFactory -> OCELStore -> SQLite` 경로에서 relation 중복을 방지하고, 이를 검증하는 테스트와 validator를 추가하는 데 한정된다.

## 2. 배경

v0.3 실험에서 `AgentRuntime.run(...)` 실행 시 OCEL event, object, event-object relation, object-object relation이 SQLite에 저장되는 것은 확인되었다.

다만 같은 logical object-object relation이 반복 저장되는 문제가 관찰되었다.

예:

```text
request:<hash> --belongs_to_session--> session:<session_id>
```

원인은 relation table에 logical uniqueness 제약이 없었고, `OCELStore.append_record(...)`가 매번 relation row를 append했기 때문이다.

v0.3.1은 이 문제를 다음 두 층에서 막는다.

1. SQLite unique index로 새 DB의 logical duplicate 저장을 막는다.
2. Store insert query에 `INSERT OR IGNORE`와 `WHERE NOT EXISTS` guard를 넣어, 기존 DB에 unique index가 생성되지 못한 경우에도 새 duplicate가 추가되지 않게 한다.

## 3. 근거, 철회 기준, 유효기간

이 문서는 2026-05-02 현재 로컬 저장소에서 확인한 파일 내용과 명령 실행 결과를 근거로 한다.

확인한 주요 명령:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe scripts\test_llm_client.py
.\.venv\Scripts\python.exe scripts\test_agent_runtime.py
.\.venv\Scripts\python.exe scripts\test_ocel_runtime.py
.\.venv\Scripts\python.exe scripts\test_ocpx_loader.py
.\.venv\Scripts\python.exe scripts\test_pig_imports.py
.\.venv\Scripts\python.exe -m pytest tests\test_imports.py tests\test_ocel_store.py tests\test_ocpx_foundation.py tests\test_pig_foundation.py tests\test_agent_runtime_ocel_shape.py
git status --short
git status --ignored --short data .pytest-tmp
```

이 문서의 설명을 철회하거나 갱신해야 하는 조건:

- `src/chanta_core/ocel/schema.py`의 relation index 정책이 변경되는 경우
- `src/chanta_core/ocel/store.py`의 relation insert policy가 변경되는 경우
- `TraceService` 또는 `AgentRuntime`의 runtime event sequence가 변경되는 경우
- 기존 SQLite DB를 정리하는 destructive migration이 추가되는 경우
- worker, skill, mission, memory runtime이 실제 OCEL emission을 시작하는 경우

현재 설명의 유효기간은 위 조건이 발생하기 전까지다.

## 4. 변경 파일 요약

v0.3.1에서 직접 관련된 주요 파일:

```text
src/chanta_core/ocel/schema.py
src/chanta_core/ocel/store.py
src/chanta_core/ocel/validators.py
src/chanta_core/ocel/query.py
scripts/test_ocel_runtime.py
tests/test_ocel_store.py
tests/test_agent_runtime_ocel_shape.py
README.md
.gitignore
pyproject.toml
src/chanta_core/__init__.py
docs/chanta_core_v0_3_1_restore.md
```

관련 상태:

- package version은 `0.3.1`로 올렸다.
- README에는 `v0.3.1 OCEL relation hygiene` 섹션을 추가했다.
- `.gitignore`에는 `src/chanta_core.egg-info/`와 `.pytest-tmp/`를 포함했다.

## 5. Relation Uniqueness Policy

v0.3.1의 logical uniqueness는 다음처럼 정의한다.

Event-object relation:

```text
event_id
object_id
qualifier
```

Object-object relation:

```text
source_object_id
target_object_id
qualifier
```

중요한 판단:

- `relation_order`는 uniqueness key에 포함하지 않았다.
- v0.3.1에서는 같은 event-object-qualifier 또는 source-target-qualifier 조합을 여러 번 저장할 의미가 아직 없다.
- 미래에 repeated relation semantics가 필요해지면 별도 occurrence id, semantic role, 또는 versioned relation 모델로 확장하는 것이 맞다.

## 6. SQLite Schema 변경

파일: `src/chanta_core/ocel/schema.py`

추가된 unique index 묶음:

```python
UNIQUE_INDEX_STATEMENTS = [
    "CREATE UNIQUE INDEX IF NOT EXISTS idx_event_object_unique ...",
    "CREATE UNIQUE INDEX IF NOT EXISTS idx_object_object_unique ...",
    "CREATE UNIQUE INDEX IF NOT EXISTS idx_chanta_event_object_relation_ext_unique ...",
    "CREATE UNIQUE INDEX IF NOT EXISTS idx_chanta_object_object_relation_ext_unique ...",
]
```

실제 logical key:

```text
event_object:
  ocel_event_id, ocel_object_id, ocel_qualifier

object_object:
  ocel_source_id, ocel_target_id, ocel_qualifier

chanta_event_object_relation_ext:
  event_id, object_id, qualifier

chanta_object_object_relation_ext:
  source_object_id, target_object_id, qualifier
```

추가된 query index:

```text
idx_chanta_event_payload_session_id
idx_chanta_event_payload_timestamp
idx_chanta_object_state_object_type
idx_chanta_event_object_relation_ext_event_id
idx_chanta_event_object_relation_ext_object_id
idx_chanta_object_object_relation_ext_source
idx_chanta_object_object_relation_ext_target
```

`REQUIRED_INDEXES`도 추가했다. validator는 required table뿐 아니라 index 존재 여부도 확인할 수 있다.

중요한 구현 판단:

- 기존 table은 drop하지 않는다.
- 기존 data DB에 이미 duplicate relation이 있으면 SQLite가 unique index 생성을 거부할 수 있다.
- 이 경우 schema initialization은 중단하지 않고 계속 진행한다.
- 따라서 clean DB에서는 unique index가 생성되고, 기존 dirty DB에서는 validator가 누락 index 또는 duplicate relation을 보고할 수 있다.

## 7. OCELStore Insert Policy

파일: `src/chanta_core/ocel/store.py`

`initialize()` 동작:

```text
1. DDL_STATEMENTS 실행
2. UNIQUE_INDEX_STATEMENTS 실행
3. unique index 생성 중 IntegrityError가 나면 기존 duplicate가 있다고 보고 중단하지 않음
4. QUERY_INDEX_STATEMENTS 실행
```

relation insert 대상 네 테이블 모두에 `INSERT OR IGNORE`를 적용했다.

```text
event_object
object_object
chanta_event_object_relation_ext
chanta_object_object_relation_ext
```

또한 모든 relation insert에 `WHERE NOT EXISTS` guard를 추가했다.

이중 방어가 필요한 이유:

- 새 DB에서는 unique index가 primary 방어선이다.
- 기존 DB는 이미 duplicate가 있으면 unique index가 생성되지 않을 수 있다.
- 그런 DB에서도 v0.3.1 이후 같은 logical relation이 더 쌓이면 안 된다.
- 그래서 store query가 index 유무와 별개로 duplicate insert를 피하게 했다.

유지한 동작:

- event table은 기존처럼 `INSERT OR IGNORE`다.
- `chanta_event_payload`는 event id 기준으로 `INSERT OR REPLACE`다.
- object table과 `chanta_object_state`는 object id 기준으로 upsert한다.
- `chanta_raw_event_mirror`는 debug/audit mirror이므로 raw event가 반복 append될 수 있다.

## 8. Duplicate Relation Validator

파일: `src/chanta_core/ocel/validators.py`

추가된 메서드:

```python
validate_duplicate_relations() -> dict[str, Any]
```

반환 구조:

```text
valid
event_object_duplicate_count
object_object_duplicate_count
chanta_event_object_relation_ext_duplicate_count
chanta_object_object_relation_ext_duplicate_count
details
```

중복 검출 기준:

```sql
GROUP BY logical_key
HAVING COUNT(*) > 1
```

각 table의 logical key:

```text
event_object:
  ocel_event_id, ocel_object_id, ocel_qualifier

object_object:
  ocel_source_id, ocel_target_id, ocel_qualifier

chanta_event_object_relation_ext:
  event_id, object_id, qualifier

chanta_object_object_relation_ext:
  source_object_id, target_object_id, qualifier
```

`validate_minimum_counts()`에는 `duplicate_relations` summary를 포함시켰다.

`validate_structure()`는 index summary도 제공하지만, 기존 return shape와 사용성을 깨지 않기 위해 structure validity는 required table 존재 여부를 중심으로 유지했다.

## 9. OCEL Query Helper

파일: `src/chanta_core/ocel/query.py`

추가된 메서드:

```python
relation_counts_for_session(session_id: str) -> dict[str, object]
session_event_object_relations(session_id: str) -> list[dict[str, Any]]
session_object_relations(session_id: str) -> list[dict[str, Any]]
```

용도:

- session 단위 relation count 확인
- AgentRuntime shape regression debugging
- 기존 `data/` DB에 남아 있는 relation 상태 분석

이 helper들은 process mining algorithm이 아니다. v0.3.1의 범위는 debugging/read helper 수준이다.

## 10. AgentRuntime Injection과 Shape Test

v0.3.1의 regression test는 LM Studio에 의존하지 않도록 fake LLM client를 사용한다.

파일: `tests/test_agent_runtime_ocel_shape.py`

검증 구조:

```text
FakeLLMClient.chat_messages(...) -> "Hello from fake LLM."
OCELStore(tmp_path / "test_ocel.sqlite")
TraceService(ocel_store=temp_store)
AgentRuntime(llm_client=fake_llm, trace_service=trace_service)
```

검증하는 event sequence:

```text
[
    "user_request_received",
    "agent_run_started",
    "prompt_assembled",
    "llm_call_started",
    "llm_response_received",
    "agent_run_completed",
]
```

검증하는 OCEL shape:

```text
event_count == 6
object_count >= 7
event_object_relation_count > 0
object_object_relation_count > 0
```

필수 object type:

```text
session
agent
user_request
prompt
llm_call
llm_response
outcome
```

중요한 duplicate regression:

```text
source_object_id LIKE "request:%"
target_object_id = "session:test-session-ocel-shape"
qualifier = "belongs_to_session"
count == 1
```

이 테스트가 의미하는 것:

- AgentRuntime의 현재 success path가 실제로 6개 runtime event를 만든다.
- runtime event가 OCELStore에 저장된다.
- user request는 payload string만이 아니라 `user_request` object로 저장된다.
- request-session relation이 반복 생성되지 않는다.

이 테스트가 의미하지 않는 것:

- worker event emission이 구현됐다는 뜻은 아니다.
- full OCEL 2.0 export compatibility가 완성됐다는 뜻은 아니다.
- pm4py 또는 ocpa integration이 동작한다는 뜻은 아니다.

## 11. Store Idempotency Test

파일: `tests/test_ocel_store.py`

추가된 테스트:

```python
test_append_same_record_does_not_duplicate_relations
```

테스트 절차:

```text
1. temp OCELStore 생성
2. session object와 agent object를 포함한 simple OCELRecord 생성
3. event-object relation 1개 생성
4. object-object relation 1개 생성
5. 같은 record를 두 번 append
6. relation count가 1로 유지되는지 확인
7. duplicate validator가 valid True인지 확인
```

기대 결과:

```text
event_count == 1
object_count == 2
event_object_relation_count == 1
object_object_relation_count == 1
validate_duplicate_relations()["valid"] is True
```

이 테스트는 store-level idempotency를 고정한다. 즉 같은 logical relation이 같은 record append로 반복 저장되지 않아야 한다.

## 12. Runtime Script 변경

파일: `scripts/test_ocel_runtime.py`

추가 출력:

```python
print("duplicate_relations:", validator.validate_duplicate_relations())
```

clean DB 기대:

```text
duplicate_relations.valid == True
```

현재 로컬 `data/` DB에서 관찰된 상태:

- script 자체는 성공적으로 실행된다.
- event/object/relation count는 증가한다.
- 하지만 v0.3 시점에 이미 저장된 object-object duplicate가 남아 있어 duplicate validation은 `False`를 보고할 수 있다.

이 차이는 구현 실패가 아니라 기존 DB 상태 차이다. v0.3.1은 기존 duplicate row를 삭제하지 않는다.

## 13. README 변경

파일: `README.md`

추가 섹션:

```text
v0.3.1 OCEL relation hygiene
```

README에 명시한 내용:

- event-object와 object-object relation은 logical uniqueness를 사용한다.
- duplicate logical relation insert는 무시된다.
- `OCELValidator`는 duplicate relation row를 탐지할 수 있다.
- raw mirror는 debug/audit 목적이므로 반복 append될 수 있다.
- worker OCEL emission은 아직 future work다.

## 14. Git Ignore와 Generated File Hygiene

파일: `.gitignore`

확인 및 보강한 항목:

```text
.env
.env.*
!.env.example
.venv/
data/
*.sqlite
*.sqlite3
__pycache__/
*.pyc
.pytest_cache/
.pytest-tmp/
src/chanta_core.egg-info/
```

확인 결과:

```text
git status --ignored --short data .pytest-tmp

!! .pytest-tmp/
!! data/
```

즉 `data/`와 `.pytest-tmp/`는 ignored 상태다.

주의:

```text
src/chanta_core.egg-info/*
src/chanta_core/__pycache__/__init__.cpython-311.pyc
```

위 generated file 일부는 이미 tracked 상태로 확인되었다. 이번 v0.3.1 작업에서는 사용자 변경 또는 기존 추적 상태를 임의로 정리하지 않기 위해 삭제하지 않았다.

## 15. 검증 결과

실행 결과:

```text
editable install: passed
scripts/test_llm_client.py: passed
scripts/test_agent_runtime.py: passed
scripts/test_ocel_runtime.py: passed
scripts/test_ocpx_loader.py: passed
scripts/test_pig_imports.py: passed
pytest requested suite: 6 passed
```

요청된 pytest suite:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_imports.py tests\test_ocel_store.py tests\test_ocpx_foundation.py tests\test_pig_foundation.py tests\test_agent_runtime_ocel_shape.py
```

결과:

```text
6 passed
```

주의할 점:

- `scripts/test_ocel_runtime.py`는 현재 로컬 `data/` DB를 사용한다.
- 해당 DB에 v0.3 중복 relation이 이미 있으면 duplicate validation은 `False`를 보고한다.
- clean temp DB를 쓰는 unit/regression test에서는 duplicate validation이 `True`다.

## 16. 현재 AgentRuntime Success Path OCEL 형태

현재 success path는 다음 runtime event를 생성한다.

```text
1. user_request_received
2. agent_run_started
3. prompt_assembled
4. llm_call_started
5. llm_response_received
6. agent_run_completed
```

대표 object types:

```text
session
agent
user_request
prompt
llm_call
llm_response
llm_model
provider
outcome
```

대표 relation qualifiers:

```text
session_context
acting_agent
primary_request
assembled_prompt
llm_call
used_provider
used_model
generated_response
produced_outcome
belongs_to_session
created_by_agent
request_to_prompt
prompt_to_llm_call
llm_call_to_response
response_to_outcome
```

failure path에서는 `agent_run_failed` event와 `error` object가 저장되어야 한다. v0.3.1의 주요 regression focus는 success path relation 중복 방지이며, failure path 확장 테스트는 다음 후보 작업이다.

## 17. 복원 절차

새 환경에서 v0.3.1 상태를 복원하는 기본 절차:

```powershell
cd <CHANTA_CORE_REPO>
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e .
```

LM Studio 기반 script 검증을 하려면 `.env`가 필요하다.

```powershell
Copy-Item .env.example .env
```

예시:

```dotenv
CHANTA_LLM_PROVIDER=lm_studio
LM_STUDIO_BASE_URL=http://localhost:1234/v1
LM_STUDIO_API_KEY=lm-studio
LM_STUDIO_MODEL=<loaded-model-id>
CHANTA_LLM_TIMEOUT_SECONDS=120
```

LM Studio 없이 확인 가능한 핵심 pytest:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_ocel_store.py tests\test_agent_runtime_ocel_shape.py
```

전체 요청 검증:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_imports.py tests\test_ocel_store.py tests\test_ocpx_foundation.py tests\test_pig_foundation.py tests\test_agent_runtime_ocel_shape.py
```

## 18. 남은 제한

v0.3.1은 기존 SQLite DB에 이미 존재하는 duplicate relation row를 삭제하지 않는다.

v0.3.1은 destructive migration을 수행하지 않는다.

v0.3.1은 worker runtime을 추가하지 않는다.

v0.3.1은 skill execution, mission runtime, memory runtime을 추가하지 않는다.

v0.3.1은 pm4py 또는 ocpa를 mandatory dependency로 추가하지 않는다.

v0.3.1은 full OCEL 2.0 JSON export/import compatibility를 완성한 버전이 아니다. 현재 SQLite OCELStore가 canonical persistence이며, standards-oriented export/import는 future work다.

## 19. 다음 작업 후보

근거가 있는 다음 후보 작업:

```text
1. 기존 DB duplicate relation 정리용 non-destructive report script
2. 선택적 cleanup migration command
3. agent_run_failed fake LLM regression test
4. TraceService failure path OCEL shape test
5. OCEL JSON export 실제 구현
6. OCPX session/object-type filtered view 확장
7. PIG diagnostics의 relation coverage 분석 확장
8. tracked egg-info / pycache 정리 여부 결정
```

이 후보들은 v0.3.1의 필수 범위는 아니다.

## 20. 결론

ChantaCore v0.3.1은 v0.3의 OCEL 기반 runtime trace foundation을 유지하면서, logical event-object/object-object relation 중복 저장을 방지하고, duplicate validation과 AgentRuntime OCEL shape regression test를 추가한 relation hygiene 버전이다.

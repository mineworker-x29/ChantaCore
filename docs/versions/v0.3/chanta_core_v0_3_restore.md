# ChantaCore v0.3 Restore Notes

작성일: 2026-05-02  
작성자: ChantaCore Maintainers  
대상 경로: `<CHANTA_CORE_REPO>`  
복원 기준 이름: `ChantaCore v0.3`

## 1. 목적

이 문서는 ChantaCore v0.3의 현재 구현 상태를 나중에 복원하거나 이어서 개발할 수 있도록 기록한다.

v0.3의 핵심 목적은 v0.2의 trace-aware agent runtime skeleton 위에, agent loop나 memory/skill/mission 기능을 더 붙이기 전에 먼저 object-centric process intelligence foundation을 세우는 것이다.

v0.3에서 새로 추가된 큰 층은 다음 세 가지다.

```text
src/chanta_core/ocel
  OCEL-oriented canonical event/object/relation foundation
  SQLite persistence
  object-aware runtime trace writing

src/chanta_core/ocpx
  future object-centric process computation layer
  lightweight read models over OCELStore

src/chanta_core/pig
  Process Intelligence Graph / Guide foundation
  lightweight graph, guide, diagnostics, recommendations over OCPX views
```

v0.3에서 깊게 구현한 실행 경로는 다음이다.

```text
AgentRuntime
  -> TraceService
  -> OCELFactory
  -> OCELStore
  -> SQLite
```

기존 LLM 실행 경로도 유지된다.

```text
AgentRuntime
  -> PromptAssemblyService
  -> LLMClient
  -> AgentRunResult
```

## 2. 근거와 유효기간

이 문서의 사실 설명은 2026-05-02 로컬 저장소에서 확인한 파일 구조, 코드 내용, 명령 실행 결과를 근거로 한다.

확인에 사용한 주요 명령은 다음이다.

```powershell
rg --files src\chanta_core
git status --short
git status --ignored --short data .pytest-tmp
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe scripts\test_llm_client.py
.\.venv\Scripts\python.exe scripts\test_agent_runtime.py
.\.venv\Scripts\python.exe scripts\test_ocel_runtime.py
.\.venv\Scripts\python.exe scripts\test_ocpx_loader.py
.\.venv\Scripts\python.exe scripts\test_pig_imports.py
.\.venv\Scripts\python.exe -m pytest tests\test_imports.py tests\test_ocel_store.py tests\test_ocpx_foundation.py tests\test_pig_foundation.py
```

판단 철회 기준:

- 이 문서 작성 이후 `src/chanta_core/ocel`, `src/chanta_core/ocpx`, `src/chanta_core/pig`, `src/chanta_core/traces/trace_service.py`, `src/chanta_core/runtime/agent_runtime.py`가 변경되면 구현 설명은 갱신되어야 한다.
- `.env`, LM Studio server, model id, timeout 설정이 바뀌면 LLM 실행 검증 결과는 다시 확인해야 한다.
- `data/` 또는 `*.sqlite` 파일이 Git 추적 대상으로 올라오면 ignore 상태 설명은 철회되어야 한다.
- `PIGBuilder`, `PIGService` naming이 다시 변경되면 PIG API 설명은 갱신되어야 한다.

유효기간:

- 구조 설명은 현재 작업 트리 상태가 유지되는 동안 유효하다.
- 실행 가능성 설명은 Python 3.11.9, 현재 `.venv`, 현재 LM Studio-compatible endpoint 상태가 유지되는 동안 강하게 유효하다.

## 3. 패키지 메타데이터

`pyproject.toml` 기준 주요 값:

```toml
[project]
name = "chanta-core"
version = "0.3.0"
description = "OCEL-oriented process intelligence runtime core for ChantaResearchGroup agents."
requires-python = ">=3.11"
dependencies = [
    "openai>=2.33.0",
    "python-dotenv>=1.2.2",
    "pytest>=8.0.0",
]

[project.scripts]
chanta-cli = "chanta_core.cli.main:main"

[tool.pytest.ini_options]
addopts = "--basetemp=.pytest-tmp"
```

`pytest`의 `--basetemp=.pytest-tmp` 설정은 sandbox 환경에서 Windows 사용자 Temp 디렉터리에 접근하지 못하는 문제를 피하기 위해 추가되었다.

`src/chanta_core/__init__.py` 기준 패키지 버전:

```python
__version__ = "0.3.0"
```

## 4. v0.3 대상 구조

v0.3에서 핵심적으로 새로 추가된 구조:

```text
src/chanta_core/ocel/
  __init__.py
  models.py
  schema.py
  store.py
  factory.py
  mapper.py
  export.py
  importers.py
  validators.py
  query.py

src/chanta_core/ocpx/
  __init__.py
  models.py
  loader.py
  object_view.py
  event_view.py
  process_view.py
  engine.py
  adapters.py
  validators.py

src/chanta_core/pig/
  __init__.py
  models.py
  builder.py
  diagnostics.py
  recommendations.py
  service.py
```

중요한 정리 사항:

- `ocpx`와 `pig` 아래에 있던 upstream/reference/legacy 성격 파일은 제거했다.
- `PIGGraphBuilder`는 중복 표현이므로 제거했다. PIG 자체가 Process Intelligence Graph를 뜻하기 때문이다.
- public builder 이름은 `PIGBuilder`로 정리했다.
- `PIGGuideService`도 별도 service 이름을 쓰지 않고 `PIGBuilder.build_guide_from_view(...)`로 통합했다.
- `PIGService`는 orchestration facade로 유지한다.

## 5. OCEL 모델

파일: `src/chanta_core/ocel/models.py`

v0.3의 OCEL foundation은 event와 object를 분리한다.

주요 dataclass:

```text
OCELObject
OCELEvent
EventObjectRelation
ObjectObjectRelation
OCELRecord
```

각 모델은 `to_dict()`를 제공한다.

핵심 원칙:

- 이벤트와 객체를 분리한다.
- 사용자 요청은 payload string이 아니라 `user_request` 객체로 남긴다.
- 이벤트-객체 관계와 객체-객체 관계를 별도 relation으로 저장한다.

초기 canonical object vocabulary는 `src/chanta_core/ocel/schema.py`의 `REQUIRED_OBJECT_TYPES`에 있다.

현재 vocabulary:

```text
session
agent
worker
user_request
message
prompt
llm_call
llm_response
llm_model
provider
skill
tool
mission
delegation
trace
artifact
file
repository
memory_entry
pattern_asset
recommendation
error
outcome
```

v0.3 런타임에서 실제로 주로 쓰는 object type:

```text
session
agent
user_request
prompt
llm_call
llm_response
llm_model
provider
error
outcome
```

## 6. SQLite OCEL Store

파일:

```text
src/chanta_core/ocel/schema.py
src/chanta_core/ocel/store.py
```

기본 DB 경로:

```text
data/ocel/chanta_core_ocel.sqlite
```

표준 지향 OCEL tables:

```text
event
object
event_object
object_object
event_map_type
object_map_type
```

ChantaCore operational tables:

```text
chanta_event_payload
chanta_object_state
chanta_event_object_relation_ext
chanta_object_object_relation_ext
chanta_raw_event_mirror
```

`OCELStore` 주요 메서드:

```text
initialize()
append_record(record, raw_event=None)
append_records(records)
fetch_event_count()
fetch_object_count()
fetch_event_object_relation_count()
fetch_object_object_relation_count()
fetch_recent_events(limit=20)
fetch_events_by_session(session_id)
fetch_objects_by_type(object_type)
fetch_related_objects_for_event(event_id)
```

동작:

- parent directory를 자동 생성한다.
- insert 전에 DB를 자동 initialize한다.
- object는 `INSERT OR REPLACE`로 upsert한다.
- event는 `event` table에는 `INSERT OR IGNORE`, payload table에는 `INSERT OR REPLACE`한다.
- dict attributes는 `json.dumps(..., ensure_ascii=False, sort_keys=True)`로 저장한다.
- `raw_event`가 주어지면 `chanta_raw_event_mirror`에 원본 debug mirror를 저장한다.

## 7. OCELFactory

파일: `src/chanta_core/ocel/factory.py`

`OCELFactory`는 runtime event를 `OCELRecord`로 만든다.

지원 event type:

```text
user_request_received
agent_run_started
prompt_assembled
llm_call_started
llm_response_received
agent_run_completed
agent_run_failed
```

stable object id 예시:

```text
session:<session_id>
agent:<agent_id>
request:<short_hash>
prompt:<short_hash>
provider:<provider_name>
model:<short_hash(model_id)>
```

unique object id 예시:

```text
llm_call:<uuid>
response:<uuid>
error:<uuid>
outcome:<uuid>
```

helper:

```text
utc_now_iso()
short_hash(text)
new_event_id(prefix="evt")
new_object_id(prefix)
```

현재 relation qualifier는 `schema.py`의 `EVENT_OBJECT_QUALIFIERS`, `OBJECT_OBJECT_QUALIFIERS`에 정의되어 있다.

## 8. TraceService 통합

파일: `src/chanta_core/traces/trace_service.py`

v0.3에서 `TraceService`는 두 가지 일을 한다.

1. `AgentRunResult` 호환성을 위해 기존 `AgentEvent`를 반환한다.
2. canonical persistence를 위해 `OCELFactory -> OCELStore`로 `OCELRecord`를 저장한다.

기존 JSONL mirror:

```text
data/traces/agent_events.jsonl
```

JSONL은 v0.3에서 canonical store가 아니다. canonical persistence는 SQLite OCELStore다. JSONL은 debug/raw mirror 성격으로 남아 있다.

public methods:

```text
record_user_request_received(...)
record_run_started(...)
record_prompt_assembled(...)
record_llm_call_started(...)
record_llm_response_received(...)
record_run_completed(...)
record_run_failed(...)
```

기존 v0.2 호환:

- `record_run_started`
- `record_prompt_assembled`
- `record_llm_response_received`
- `record_run_completed`
- `record_run_failed`

위 메서드는 계속 존재한다.

## 9. AgentRuntime 통합

파일: `src/chanta_core/runtime/agent_runtime.py`

v0.3의 `AgentRuntime.run(...)` event emission sequence:

```text
1. user_request_received
2. agent_run_started
3. prompt_assembled
4. llm_call_started
5. llm_response_received
6. agent_run_completed
```

LLM call이 실패하면:

```text
agent_run_failed
```

이 기록되고, `OCELFactory.agent_run_failed(...)`를 통해 `error` object가 SQLite OCELStore에 저장된다. 예외는 삼키지 않고 다시 raise한다.

`AgentRunResult` shape는 유지된다.

```text
session_id
agent_id
user_input
response_text
events
metadata
```

## 10. OCPX Foundation

파일:

```text
src/chanta_core/ocpx/models.py
src/chanta_core/ocpx/loader.py
src/chanta_core/ocpx/engine.py
src/chanta_core/ocpx/validators.py
```

OCPX는 v0.3에서 heavy process mining algorithm을 구현하지 않는다. 목적은 OCELStore를 읽을 수 있는 object-centric process read model foundation을 제공하는 것이다.

dataclass:

```text
OCPXEventView
OCPXObjectView
OCPXProcessView
```

`OCPXLoader`:

```text
load_session_view(session_id)
load_recent_view(limit=20)
```

`OCPXEngine`:

```text
summarize_view(view)
count_events_by_type(view)
count_objects_by_type(view)
```

`OCPXValidator`:

```text
validate_process_view(view)
```

현재 의도적으로 사용하지 않는 것:

```text
pm4py
ocpa
networkx
pandas
numpy
```

## 11. PIG Foundation

파일:

```text
src/chanta_core/pig/models.py
src/chanta_core/pig/builder.py
src/chanta_core/pig/diagnostics.py
src/chanta_core/pig/recommendations.py
src/chanta_core/pig/service.py
```

PIG는 Process Intelligence Graph / Guide layer다. 이름 자체에 Graph가 포함되므로 `PIGGraphBuilder` 같은 이름은 사용하지 않는다.

현재 public 중심 API:

```text
PIGBuilder
PIGService
```

`PIGBuilder`:

```text
build_from_ocpx_view(view) -> PIGGraph
build_guide_from_view(view) -> dict[str, Any]
```

`PIGService`:

```text
analyze_session(session_id) -> dict[str, Any]
analyze_recent(limit=20) -> dict[str, Any]
```

dataclass:

```text
PIGNode
PIGEdge
PIGGraph
PIGDiagnostic
PIGRecommendation
```

diagnostics:

```text
no_events
no_objects
events_without_related_objects
```

recommendations:

```text
check_trace_emission
check_object_mapping
improve_event_object_relations
```

현재 PIG는 heavy graph algorithm을 수행하지 않는다. `networkx`도 사용하지 않는다.

## 12. Export, Import, Validation, Query

OCEL export:

```text
src/chanta_core/ocel/export.py
OCELExporter.export_sqlite_copy(target_path)
OCELExporter.export_json_stub(target_path)
```

v0.3에서 SQLite store가 canonical이다. JSON OCEL export는 stub이며 future work로 남겨져 있다.

OCEL import:

```text
src/chanta_core/ocel/importers.py
OCELImporter.import_sqlite(source_path)
```

v0.3에서는 safe placeholder 성격이다. full import/conformance는 future work다.

OCEL validation:

```text
src/chanta_core/ocel/validators.py
OCELValidator.validate_structure()
OCELValidator.validate_minimum_counts()
OCELValidator.validate_session_trace(session_id)
```

OCEL query:

```text
src/chanta_core/ocel/query.py
OCELQueryService.session_summary(session_id)
OCELQueryService.recent_events(limit=20)
OCELQueryService.object_type_counts()
```

## 13. Scripts

v0.3에서 추가된 scripts:

```text
scripts/test_ocel_runtime.py
scripts/test_ocpx_loader.py
scripts/test_pig_imports.py
```

기존 script:

```text
scripts/test_llm_client.py
scripts/test_agent_runtime.py
```

`scripts/test_agent_runtime.py`는 v0.3에서 event list가 6개로 늘어난다.

예상 event list:

```text
[
  'user_request_received',
  'agent_run_started',
  'prompt_assembled',
  'llm_call_started',
  'llm_response_received',
  'agent_run_completed'
]
```

`scripts/test_ocel_runtime.py`는 runtime을 실제로 실행한 뒤 OCELStore count와 validator 결과를 출력한다.

확인된 출력 요지:

```text
event_count: 12
object_count: 15
event_object_relations: 46
object_object_relations: 14
validation: {'valid': True, 'required_tables_exist': True, 'missing_tables': [], 'table_count': 12}
session_trace: {'valid': True, 'session_events_count': 6, ...}
```

위 count는 해당 시점에 runtime script가 두 번 실행된 SQLite 상태 기준이다. clean DB에서는 숫자가 달라진다.

## 14. Tests

v0.3에서 추가 또는 확장된 tests:

```text
tests/test_imports.py
tests/test_ocel_store.py
tests/test_ocpx_foundation.py
tests/test_pig_foundation.py
```

`tests/test_ocel_store.py`:

- temp SQLite path를 사용한다.
- simple `OCELRecord`를 append한다.
- event/object/event_object_relation count를 검증한다.

`tests/test_ocpx_foundation.py`:

- temp OCELStore에 simple record를 넣는다.
- `OCPXLoader.load_recent_view(...)`로 read model을 만든다.
- `OCPXEngine.summarize_view(...)` 결과를 확인한다.

`tests/test_pig_foundation.py`:

- temp OCELStore에서 OCPX view를 만든다.
- `PIGBuilder`와 `PIGService`를 검증한다.

`tests/test_imports.py`에는 다음 계층 import가 포함된다.

```text
OCELObject
OCELEvent
EventObjectRelation
ObjectObjectRelation
OCELRecord
OCELStore
OCELFactory
OCELValidator
OCELQueryService
OCPXLoader
OCPXEngine
OCPXProcessView
PIGService
PIGBuilder
PIGGraph
PIGDiagnosticService
PIGRecommendationService
```

## 15. 검증 결과

실행 확인 명령:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe scripts\test_llm_client.py
.\.venv\Scripts\python.exe scripts\test_agent_runtime.py
.\.venv\Scripts\python.exe scripts\test_ocel_runtime.py
.\.venv\Scripts\python.exe scripts\test_ocpx_loader.py
.\.venv\Scripts\python.exe scripts\test_pig_imports.py
.\.venv\Scripts\python.exe -m pytest tests\test_imports.py tests\test_ocel_store.py tests\test_ocpx_foundation.py tests\test_pig_foundation.py
```

확인된 상태:

```text
editable install: passed
scripts/test_llm_client.py: passed
scripts/test_agent_runtime.py: passed
scripts/test_ocel_runtime.py: passed
scripts/test_ocpx_loader.py: passed
scripts/test_pig_imports.py: passed
pytest foundation tests: passed
```

pytest 확인 출력:

```text
collected 4 items
tests/test_imports.py .
tests/test_ocel_store.py .
tests/test_ocpx_foundation.py .
tests/test_pig_foundation.py .
4 passed
```

PIG naming 정리 후 재확인:

```text
tests/test_imports.py .
tests/test_ocpx_foundation.py .
tests/test_pig_foundation.py .
3 passed
```

## 16. Git Ignore와 생성물

`.gitignore`에 포함된 관련 항목:

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
```

확인된 ignored 상태:

```text
!! data/
!! .pytest-tmp/
```

확인된 생성 SQLite:

```text
data/ocel/chanta_core_ocel.sqlite
.pytest-tmp/.../test.sqlite
```

위 파일들은 ignored 상태이며 Git 추적 대상으로 올라오지 않았다.

## 17. 현재 주의점

1. `src/chanta_core.egg-info`와 `__pycache__` 일부가 작업 트리에 보인다.

이는 v0.3 기능 자체와는 별개지만, commit 정리 단계에서 별도 판단이 필요하다. 이미 추적 중인 egg-info 또는 pycache 파일은 `.gitignore`만으로 사라지지 않는다.

2. `data/`는 런타임 검증 과정에서 생성된다.

`data/ocel/chanta_core_ocel.sqlite`는 v0.3 동작 확인의 결과물이며, 커밋 대상이 아니다.

3. JSONL trace는 canonical이 아니다.

v0.3의 canonical trace persistence는 SQLite OCELStore다. JSONL은 debug/raw mirror로만 이해해야 한다.

4. OCEL 2.0 완전 호환 export는 아직 구현되지 않았다.

v0.3은 OCEL-oriented canonical foundation이다. pm4py/ocpa compatibility는 future-facing이며, standards-oriented export/import 계층을 통해 달성해야 한다.

5. OCPX와 PIG는 foundation이다.

OCPX는 아직 heavy process mining algorithm을 구현하지 않는다. PIG도 아직 full process intelligence reasoning이나 graph algorithm을 수행하지 않는다.

## 18. 복원 절차

새 환경에서 v0.3 상태를 복원하는 보수적 절차:

```powershell
cd <CHANTA_CORE_REPO>
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e .
```

`.env` 준비:

```powershell
Copy-Item .env.example .env
```

LM Studio 사용 시 `.env`에 최소 설정:

```dotenv
CHANTA_LLM_PROVIDER=lm_studio
LM_STUDIO_BASE_URL=http://localhost:1234/v1
LM_STUDIO_API_KEY=lm-studio
LM_STUDIO_MODEL=<LM Studio에서 실제 로드된 모델 id>
CHANTA_LLM_TIMEOUT_SECONDS=120
```

검증:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_imports.py tests\test_ocel_store.py tests\test_ocpx_foundation.py tests\test_pig_foundation.py
.\.venv\Scripts\python.exe scripts\test_agent_runtime.py
.\.venv\Scripts\python.exe scripts\test_ocel_runtime.py
.\.venv\Scripts\python.exe scripts\test_ocpx_loader.py
.\.venv\Scripts\python.exe scripts\test_pig_imports.py
```

## 19. 다음 작업 후보

근거가 있는 다음 작업 후보:

- OCEL JSON export를 실제 OCEL 2.0 JSON schema에 맞춰 구현한다.
- SQLite schema에 primary/unique constraints와 indexes를 추가할지 결정한다.
- `event_map_type`, `object_map_type`을 실제 export mapping에 사용한다.
- OCPX에 session/object type별 filtered view를 추가한다.
- PIG diagnostics를 relation coverage, missing outcome, failed run pattern까지 확장한다.
- `AgentRuntime`의 LLM failure unit test를 fake LLMClient로 추가한다.
- `egg-info`, `__pycache__` 추적 상태를 별도 commit에서 정리할지 결정한다.

## 20. 결론

ChantaCore v0.3은 v0.2의 LLMClient/AgentRuntime 실행 경로를 유지하면서, runtime trace를 OCEL-oriented event/object/relation record로 변환해 SQLite에 저장하는 Process Intelligence foundation을 추가한 상태다. 현재 canonical trace persistence는 `OCELStore`의 SQLite DB이며, `OCPXLoader`는 그 데이터를 process view로 읽고, `PIGBuilder`와 `PIGService`는 그 view에서 기초 graph/guide/diagnostic/recommendation 출력을 만든다.

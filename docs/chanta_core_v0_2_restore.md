# ChantaCore v0.2 Restore Notes

작성일: 2026-05-01  
작성자: ChantaCore Maintainers  
대상 경로: `<CHANTA_CORE_REPO>`  
복원 기준 이름: `ChantaCore v0.2`

## 1. 목적

이 문서는 ChantaCore v0.2를 나중에 복원하거나 이어서 개발할 수 있도록 현재 구현 상태를 기록한다.

v0.2의 목표는 기존 LLMClient/LM Studio 연동 위에 trace-aware agent runtime skeleton을 얹는 것이다. 전체 프로젝트를 몇 개 파일로 평면화하지 않고, ChantaResearchGroup agent들의 공유 runtime core가 될 수 있도록 주요 기능 범주별 디렉터리를 먼저 만든다.

v0.2에서 깊게 구현한 실행 경로는 다음이다.

```text
AgentRuntime
  -> PromptAssemblyService
  -> LLMClient
  -> TraceService / AgentEventStore
  -> AgentRunResult
```

다음 영역은 v0.2에서 import 가능한 최소 골격만 둔다.

```text
memory
skills
missions
delegation
```

## 2. 근거와 유효기간

이 문서의 사실 설명은 2026-05-01에 로컬 저장소에서 직접 확인한 파일 내용과 명령 실행 결과를 근거로 한다.

확인에 사용한 주요 명령:

```powershell
git status --short
rg --files src\chanta_core scripts tests docs
Get-Content -Raw pyproject.toml
Get-Content -Raw src\chanta_core\runtime\agent_runtime.py
.\.venv\Scripts\python.exe -m pytest tests\test_imports.py
.\.venv\Scripts\python.exe -m chanta_core show-config
.\.venv\Scripts\python.exe -B -c "import chanta_core; print(chanta_core.__version__)"
```

판단 철회 기준:

- 이 문서 작성 이후 v0.2 관련 파일이 수정되면 세부 구현 설명은 갱신해야 한다.
- `.env`의 모델명, LM Studio 서버 상태, 로컬 모델 설정이 바뀌면 LLM 호출 검증 결과는 재검증해야 한다.
- v0.2 변경분이 커밋되면 Git 기준점 설명을 새 커밋 SHA로 갱신해야 한다.
- `egg-info`와 `__pycache__` 정리 여부가 바뀌면 작업 트리 상태 설명은 더 이상 맞지 않는다.

유효기간:

- 구조와 코드 설명은 이 문서가 작성된 작업 트리 상태가 유지되는 동안 유효하다.
- 실행 가능성 설명은 Python 3.11.9 가상환경, 설치된 의존성, LM Studio endpoint 상태가 유지되는 동안만 강하게 유효하다.

## 3. Git 상태

확인 시점의 브랜치와 HEAD:

```text
branch: main
HEAD: 265d9bc3c5afc62ab80cf4d39c78d69f716a366d
```

중요:

- v0.2 변경분은 확인 시점에 아직 커밋되지 않은 작업 트리 변경이다.
- 따라서 `HEAD`는 v0.1 커밋을 가리키고 있고, v0.2는 파일 변경분으로 존재한다.

확인 시점의 주요 변경 상태:

```text
 M pyproject.toml
 M src/chanta_core/__init__.py
 M src/chanta_core/__main__.py
 M src/chanta_core/cli.py
 M src/chanta_core/llm/client.py
 M src/chanta_core/llm/types.py
 M src/chanta_core/runtime/chat_service.py
 M src/chanta_core/settings/llm_settings.py
 M src/chanta_core/traces/__init__.py
?? scripts/test_agent_runtime.py
?? tests/
?? src/chanta_core/agents/default_agent.py
?? src/chanta_core/agents/profile.py
?? src/chanta_core/cli/
?? src/chanta_core/delegation/
?? src/chanta_core/llm/errors.py
?? src/chanta_core/memory/
?? src/chanta_core/missions/
?? src/chanta_core/prompts/
?? src/chanta_core/runtime/agent_runtime.py
?? src/chanta_core/runtime/execution_context.py
?? src/chanta_core/runtime/run_result.py
?? src/chanta_core/skills/
?? src/chanta_core/traces/event.py
?? src/chanta_core/traces/event_store.py
?? src/chanta_core/traces/trace_service.py
```

주의:

- `pip install -e .`와 Python 실행 때문에 기존에 Git 추적 중이던 `src/chanta_core.egg-info/*`와 일부 `__pycache__/*.pyc`도 갱신되었다.
- `.env`와 `.venv`는 v0.2 구현 대상으로 수정하지 않았다.
- `docs/chanta_core_v0_1_restore.md`와 `sou_of_vera.md`는 v0.2 구현 이전부터 미추적 상태로 존재했다.

## 4. 패키지 메타데이터

`pyproject.toml`의 v0.2 핵심 내용:

```toml
[project]
name = "chanta-core"
version = "0.2.0"
description = "Trace-aware runtime core for ChantaResearchGroup agents."
requires-python = ">=3.10"
dependencies = [
    "openai>=2.33.0",
    "python-dotenv>=1.2.2",
    "pytest>=8.0.0",
]

[project.scripts]
chanta-cli = "chanta_core.cli.main:main"
```

v0.1과 달라진 점:

- 패키지 버전이 `0.2.0`으로 올라갔다.
- `openai`, `python-dotenv`, `pytest` 의존성이 명시되었다.
- CLI entry point가 `chanta_core.cli.main:main`으로 이동했다.

확인 결과:

```powershell
.\.venv\Scripts\python.exe -B -c "import chanta_core; print(chanta_core.__version__)"
```

출력:

```text
0.2.0
```

## 5. 목표 디렉터리 구조

v0.2 기준 주요 구조:

```text
src/chanta_core/
  settings/
  llm/
  runtime/
  agents/
  prompts/
  traces/
  memory/
  skills/
  missions/
  delegation/
  cli/
```

확인된 파일 목록:

```text
src/chanta_core/settings/__init__.py
src/chanta_core/settings/app_settings.py
src/chanta_core/settings/llm_settings.py

src/chanta_core/llm/__init__.py
src/chanta_core/llm/client.py
src/chanta_core/llm/messages.py
src/chanta_core/llm/types.py
src/chanta_core/llm/errors.py
src/chanta_core/llm/lm_studio_client.py
src/chanta_core/llm/schemas.py

src/chanta_core/runtime/__init__.py
src/chanta_core/runtime/execution_context.py
src/chanta_core/runtime/run_result.py
src/chanta_core/runtime/chat_service.py
src/chanta_core/runtime/agent_runtime.py

src/chanta_core/agents/__init__.py
src/chanta_core/agents/profile.py
src/chanta_core/agents/default_agent.py

src/chanta_core/prompts/__init__.py
src/chanta_core/prompts/assembly.py
src/chanta_core/prompts/templates.py

src/chanta_core/traces/__init__.py
src/chanta_core/traces/event.py
src/chanta_core/traces/event_store.py
src/chanta_core/traces/trace_service.py

src/chanta_core/memory/__init__.py
src/chanta_core/memory/memory_record.py
src/chanta_core/memory/memory_store.py

src/chanta_core/skills/__init__.py
src/chanta_core/skills/skill.py
src/chanta_core/skills/registry.py
src/chanta_core/skills/executor.py

src/chanta_core/missions/__init__.py
src/chanta_core/missions/mission.py
src/chanta_core/missions/mission_runtime.py

src/chanta_core/delegation/__init__.py
src/chanta_core/delegation/packet.py
src/chanta_core/delegation/result.py

src/chanta_core/cli/__init__.py
src/chanta_core/cli/main.py
src/chanta_core/cli.py
```

주의:

- `src/chanta_core/cli.py`는 구 CLI 구현을 유지하지 않고 새 `src/chanta_core/cli/main.py`로 위임하는 compatibility shim 역할을 한다.
- `src/chanta_core/llm/lm_studio_client.py`와 `schemas.py`는 v0.1 잔여 구조가 남아 있다. v0.2의 주 실행 경로는 `LLMClient`이다.

## 6. Runtime 실행 경로

파일: `src/chanta_core/runtime/agent_runtime.py`

핵심 클래스:

```python
class AgentRuntime:
    def run(
        self,
        user_input: str,
        session_id: str | None = None,
    ) -> AgentRunResult:
        ...
```

실행 순서:

1. `load_default_agent_profile()`로 기본 `AgentProfile`을 준비한다.
2. `ExecutionContext.create(...)`로 실행 context를 만든다.
3. `TraceService.record_run_started(context)`를 기록한다.
4. `PromptAssemblyService.assemble(context, profile)`로 system/user messages를 만든다.
5. `TraceService.record_prompt_assembled(context, messages)`를 기록한다.
6. `LLMClient.chat_messages(...)`로 local LLM provider를 호출한다.
7. `TraceService.record_llm_response_received(context, response_text)`를 기록한다.
8. `TraceService.record_run_completed(context)`를 기록한다.
9. `AgentRunResult`를 반환한다.

실패 처리:

- LLM 호출 또는 중간 단계에서 예외가 발생하면 `agent_run_failed` 이벤트를 기록한다.
- 그 뒤 예외를 삼키지 않고 다시 raise한다.

## 7. ExecutionContext

파일: `src/chanta_core/runtime/execution_context.py`

역할:

- 한 번의 agent run에 필요한 session, agent, user input, 생성 시각, metadata를 보관한다.

필드:

```text
session_id: str
agent_id: str
user_input: str
created_at: str
metadata: dict[str, Any]
```

보조 함수:

```text
create_session_id()
utc_now_iso()
ExecutionContext.create(...)
```

현재 session id는 `uuid4()` 문자열로 생성된다.

## 8. AgentProfile

파일:

```text
src/chanta_core/agents/profile.py
src/chanta_core/agents/default_agent.py
```

필드:

```text
agent_id
name
role
system_prompt
default_temperature
max_tokens
```

기본 profile:

```text
agent_id: chanta_core_default
name: ChantaCore Default Agent
role: trace-aware local runtime agent
default_temperature: 0.7
max_tokens: 384
```

system prompt 요지:

```text
ChantaCore이며, local LLM provider를 통해 실행되는 trace-aware runtime agent다. 명확하고 간결하게 답한다.
```

## 9. PromptAssemblyService

파일: `src/chanta_core/prompts/assembly.py`

역할:

- `ExecutionContext`와 `AgentProfile`을 받아 `list[ChatMessage]`로 변환한다.

현재 출력 형태:

```python
[
    {"role": "system", "content": profile.system_prompt},
    {"role": "user", "content": context.user_input},
]
```

`ChatMessage` 타입은 `chanta_core.llm.types`의 기존 타입을 사용한다.

## 10. LLM 계층

파일:

```text
src/chanta_core/llm/client.py
src/chanta_core/llm/messages.py
src/chanta_core/llm/types.py
src/chanta_core/llm/errors.py
```

`LLMClient`는 기존 v0.1의 OpenAI SDK 기반 구조를 유지하되 다음이 보완되었다.

- `timeout=self.settings.timeout_seconds` 반영
- 기본 `max_tokens`를 `384`로 조정
- `create_llm_client(...)` compatibility helper 추가

`scripts/test_llm_client.py`가 사용하는 경로:

```python
from chanta_core.llm import LLMClient

llm = LLMClient()
response = llm.chat(
    system_message="You are ChantaCore's local LLM connection test.",
    user_message="Say hello in one short sentence.",
)
```

주의:

- 현재 LM Studio/Qwen 조합에서는 짧은 completion에서 `content`가 비어 있고 `reasoning_content`가 먼저 채워지는 경우가 관찰되었다.
- 이 현상은 LLM 서버와 모델 출력 방식에 의존한다. v0.2의 `LLMClient`는 현재 `message.content`만 반환한다.

## 11. Settings

파일:

```text
src/chanta_core/settings/app_settings.py
src/chanta_core/settings/llm_settings.py
```

`LLMSettings` 필드:

```text
provider: str
base_url: str
api_key: str
model: str
timeout_seconds: float = 60.0
```

호환 alias:

```python
LLMProviderSettings = LLMSettings
```

지원 provider:

```text
lm_studio
ollama
```

확인 시점의 `show-config` 결과:

```text
env_file=<CHANTA_CORE_REPO>\.env
provider=lm_studio
base_url=http://localhost:1234/v1
model=qwen3.6-35b-a3b:2
api_key=set
timeout_seconds=120.0
```

중요한 관찰:

- 확인 시점의 `.env`는 `LM_STUDIO_MODEL=qwen3.6-35b-a3b:2` 계열로 읽힌다.
- 별도 확인에서 LM Studio `/v1/models` endpoint는 `qwen3.6-35b-a3b`를 반환했다.
- 따라서 CLI/스크립트 호출 시 모델명이 맞지 않으면 shell 환경변수로 `LM_STUDIO_MODEL=qwen3.6-35b-a3b`를 덮어써야 할 수 있다.

## 12. Trace 계층

파일:

```text
src/chanta_core/traces/event.py
src/chanta_core/traces/event_store.py
src/chanta_core/traces/trace_service.py
```

`AgentEvent` 필드:

```text
event_id
event_type
session_id
agent_id
timestamp
payload
```

`AgentEvent.to_dict()`는 JSON 직렬화 가능한 dict를 반환한다.

`AgentEventStore` 기본 저장 위치:

```text
data/traces/agent_events.jsonl
```

동작:

- parent directory를 자동 생성한다.
- UTF-8로 append한다.
- 한 줄에 JSON object 하나를 기록한다.

`TraceService`가 기록하는 event type:

```text
agent_run_started
prompt_assembled
llm_response_received
agent_run_completed
agent_run_failed
```

실패 경로 확인:

- LLM timeout 상황에서 `agent_run_failed`가 JSONL에 기록되는 것을 확인했다.
- 예시 payload에는 `error_type: APITimeoutError`, `error: Request timed out.`가 들어갔다.

## 13. AgentRunResult

파일: `src/chanta_core/runtime/run_result.py`

필드:

```text
session_id
agent_id
user_input
response_text
events
metadata
```

`events`는 해당 run 중 생성된 `AgentEvent` 목록이다.

## 14. ChatService

파일: `src/chanta_core/runtime/chat_service.py`

역할:

- `AgentRuntime` 위의 얇은 wrapper다.

메서드:

```python
chat(user_input: str, session_id: str | None = None) -> str
run(user_input: str) -> str
```

`run(...)`은 v0.1 계열 호환성을 위해 `chat(...)`을 호출한다.

## 15. Placeholder 범주

v0.2에서 heavy behavior는 구현하지 않고 import 가능한 최소 골격만 둔 범주:

```text
memory
skills
missions
delegation
```

대표 클래스:

```text
MemoryRecord
MemoryStore
Skill
SkillRegistry
SkillExecutor
Mission
MissionRuntime
DelegationPacket
DelegationResult
```

현재 성격:

- future persistent memory
- future skill discovery/execution
- future mission orchestration
- future agent-to-agent delegation

현재 이 범주들은 runtime main path에 연결되어 있지 않다.

## 16. CLI

새 CLI 진입점:

```text
src/chanta_core/cli/main.py
```

패키지 실행:

```powershell
.\.venv\Scripts\python.exe -m chanta_core show-config
.\.venv\Scripts\python.exe -m chanta_core ask "Say hello in one sentence."
.\.venv\Scripts\python.exe -m chanta_core repl
```

editable install 후 console script:

```powershell
chanta-cli show-config
chanta-cli ask "Say hello in one sentence."
chanta-cli repl
```

현재 CLI는 `AgentRuntime`을 경유한다. 따라서 `ask`와 `repl` 호출은 trace event를 `data/traces/agent_events.jsonl`에 기록한다.

모델명 보정이 필요한 경우:

```powershell
$env:LM_STUDIO_MODEL="qwen3.6-35b-a3b"
.\.venv\Scripts\python.exe -m chanta_core ask "Say hello from ChantaCore in one sentence."
```

## 17. 테스트와 검증

추가된 스크립트:

```text
scripts/test_agent_runtime.py
```

동작:

- `.env`를 로드한다.
- `AgentRuntime()`을 생성한다.
- 한 문장 prompt를 실행한다.
- 응답, session id, event type 목록을 출력한다.

추가된 import test:

```text
tests/test_imports.py
```

검증 대상:

```text
LLMClient
AgentRuntime
ChatService
AgentProfile
PromptAssemblyService
AgentEvent
TraceService
MemoryRecord
Skill
Mission
DelegationPacket
```

확인된 import test 결과:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_imports.py
```

출력 요지:

```text
collected 1 item
tests\test_imports.py . [100%]
1 passed
```

확인된 runtime script 결과:

```powershell
$env:LM_STUDIO_MODEL="qwen3.6-35b-a3b"
$env:CHANTA_LLM_TIMEOUT_SECONDS="180"
.\.venv\Scripts\python.exe scripts\test_agent_runtime.py
```

출력 요지:

```text
Greetings from the ChantaCore trace-aware runtime agent.
session_id: <uuid>
events: ['agent_run_started', 'prompt_assembled', 'llm_response_received', 'agent_run_completed']
```

기존 LLMClient script:

```powershell
$env:LM_STUDIO_MODEL="qwen3.6-35b-a3b"
$env:CHANTA_LLM_TIMEOUT_SECONDS="180"
.\.venv\Scripts\python.exe scripts\test_llm_client.py
```

확인 결과:

- 종료 코드 0으로 완료되었다.
- 다만 확인 시점에는 출력 텍스트가 비어 있었다.
- 근거상 코드 import/호출 실패라기보다 현재 LM Studio/Qwen 응답이 `message.content` 대신 reasoning 계열 필드에 오래 머무르는 동작과 관련된 것으로 보인다.

## 18. 복원 절차

v0.2가 커밋된 뒤라면 해당 커밋으로 checkout하는 것이 가장 정확하다.

v0.2가 아직 커밋되지 않은 상태를 복원하려면 다음 파일 변경분이 필요하다.

```text
pyproject.toml
src/chanta_core/__init__.py
src/chanta_core/__main__.py
src/chanta_core/cli.py
src/chanta_core/settings/*
src/chanta_core/llm/client.py
src/chanta_core/llm/types.py
src/chanta_core/llm/errors.py
src/chanta_core/runtime/*
src/chanta_core/agents/*
src/chanta_core/prompts/*
src/chanta_core/traces/*
src/chanta_core/memory/*
src/chanta_core/skills/*
src/chanta_core/missions/*
src/chanta_core/delegation/*
src/chanta_core/cli/*
scripts/test_agent_runtime.py
tests/test_imports.py
```

환경 복원:

```powershell
cd <CHANTA_CORE_REPO>
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e .
```

확인:

```powershell
.\.venv\Scripts\python.exe -B -c "import chanta_core; print(chanta_core.__version__)"
.\.venv\Scripts\python.exe -m chanta_core show-config
.\.venv\Scripts\python.exe -m pytest tests\test_imports.py
```

LM Studio 호출 확인:

```powershell
$env:LM_STUDIO_MODEL="qwen3.6-35b-a3b"
$env:CHANTA_LLM_TIMEOUT_SECONDS="180"
.\.venv\Scripts\python.exe scripts\test_agent_runtime.py
```

## 19. 알려진 주의점

1. v0.2는 확인 시점에 아직 커밋되지 않았다.

따라서 Git SHA 하나만으로는 v0.2를 복원할 수 없다. 커밋 전에는 작업 트리 변경분 자체가 복원 단위다.

2. `.env`의 모델명과 LM Studio가 노출하는 모델명이 다를 수 있다.

확인 시점:

```text
.env model: qwen3.6-35b-a3b:2
/v1/models id: qwen3.6-35b-a3b
```

3. `egg-info`와 `__pycache__`가 Git 추적 대상에 남아 있다.

이는 v0.2 구현의 핵심 논리와는 별개지만, 커밋 정리 시 별도 판단이 필요하다.

4. `LLMClient`는 아직 `message.content`만 반환한다.

현재 Qwen/LM Studio 조합에서는 reasoning field가 길게 생성되어 짧은 출력 테스트가 빈 문자열로 끝날 수 있다. 이 문제를 고치려면 OpenAI SDK response의 `reasoning_content` 처리 정책을 별도 설계해야 한다.

5. `memory`, `skills`, `missions`, `delegation`은 의도적으로 얕다.

v0.2의 목표는 runtime skeleton과 trace path다. 위 범주들은 구조 선점과 import 가능성 확보가 목적이다.

## 20. 다음 작업 후보

근거가 있는 다음 후보:

- v0.2 변경분 커밋 생성
- Git 추적 중인 `__pycache__`, `egg-info` 정리 여부 결정
- `.env.example`에 현재 권장 LM Studio model naming 주석 추가
- `LLMClient`의 빈 content 문제를 response schema 기준으로 조사
- `tests/test_imports.py` 외에 `AgentRuntime`을 fake LLMClient로 검증하는 unit test 추가
- trace event payload에서 prompt 전문을 저장할지, privacy-safe summary를 저장할지 정책 결정

## 21. 결론

ChantaCore v0.2는 v0.1의 LLMClient/LM Studio 연동을 유지하면서, `AgentRuntime`, `PromptAssemblyService`, `TraceService`, `AgentEventStore`, `AgentRunResult`로 이어지는 trace-aware runtime skeleton을 추가한 상태다. 확인 시점 기준 import test와 config path는 통과했고, LM Studio 모델명을 실제 `/v1/models` 값으로 보정하면 `scripts/test_agent_runtime.py`도 정상적으로 응답과 trace event 목록을 반환한다.

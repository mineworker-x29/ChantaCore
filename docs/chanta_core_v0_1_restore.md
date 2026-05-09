# ChantaCore v0.1 Restore Notes

작성일: 2026-05-01  
작성자: ChantaCore Maintainers  
대상 경로: `D:\ChantaResearchGroup\ChantaCore`  
복원 기준 이름: `ChantaCore v0.1`

## 1. 목적

이 문서는 ChantaCore v0.1의 현재 저장소 상태를 나중에 최대한 같은 형태로 복원하기 위한 기록이다.

이 문서는 다음을 복원 대상으로 삼는다.

- Python 패키지 구조
- CLI 진입점
- LM Studio 또는 Ollama 같은 OpenAI-compatible endpoint 연동 의도
- 현재 구현된 코드의 실제 상태
- 현재 확인된 결함과 불일치
- 로컬 가상환경에서 관찰된 의존성 상태

이 문서는 다음을 복원 대상으로 삼지 않는다.

- `.env`의 실제 비밀값
- `.venv` 디렉터리 자체
- 로컬 캐시와 빌드 산출물의 재생성 가능하지 않은 내부 상태

## 2. 근거와 유효기간

이 문서의 사실 설명은 2026-05-01에 저장소에서 직접 확인한 결과를 근거로 한다.

확인에 사용한 주요 명령은 다음과 같다.

```powershell
Get-ChildItem -Force
rg --files
git status --short
git log --oneline -5
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
git remote -v
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -B -m chanta_core show-config
.\.venv\Scripts\pip.exe freeze
```

판단 철회 기준:

- 이 문서 작성 이후 파일 내용, Git 커밋, 의존성, `.env` 값, 가상환경이 바뀌면 이 문서의 상태 설명은 더 이상 현재 상태 설명이 아니다.
- 원격 저장소의 `main` 브랜치가 강제 갱신되거나, 로컬 미추적 파일이 추가/삭제되면 복원 절차 일부는 재검증해야 한다.
- 여기 적힌 결함은 현재 코드 기준의 정적 확인과 최소 실행 확인에 근거한다. 코드가 수정되면 결함 판단도 철회 또는 갱신해야 한다.

유효기간:

- 저장소 상태 기록으로서는 커밋 `265d9bc3c5afc62ab80cf4d39c78d69f716a366d`와 이 문서가 함께 보존되는 동안 유효하다.
- 실행 가능성 기록으로서는 로컬 `.venv`와 패키지 버전이 유지되는 동안만 강하게 유효하다.

## 3. Git 상태

확인 시점의 브랜치와 커밋:

```text
branch: main
HEAD: 265d9bc3c5afc62ab80cf4d39c78d69f716a366d
remote: origin https://github.com/mineworker-x29/ChantaCore.git
```

최근 커밋:

```text
265d9bc Bootstrap ChantaCore v0.1: LLM Client + lm studio integration
f7ad2ca Remove virtual enviroment from repository
cc3f751 Initialize ChantaCore
66dedf3 Initial commit
```

확인 시점의 작업 트리 상태:

```text
 M src/chanta_core/llm/__pycache__/types.cpython-311.pyc
?? sou_of_vera.md
```

주의:

- `__pycache__`와 `*.pyc`는 `.gitignore`에 포함되어 있지만, 일부 바이트코드 파일은 이미 Git 추적 대상이었다.
- `.env`도 `.gitignore`에는 제외 대상으로 적혀 있지만, 확인 시점에는 Git 추적 대상에 포함되어 있었다.
- `sou_of_vera.md`는 확인 시점에 미추적 파일이었다.

## 4. 저장소 최상위 구조

확인 시점의 최상위 항목:

```text
.git/
.venv/
scripts/
src/
.env
.env.example
.gitignore
pyproject.toml
README.md
sou_of_vera.md
```

핵심 파일 목록:

```text
README.md
pyproject.toml
.env.example
scripts/test_llm_client.py
src/chanta_core/__init__.py
src/chanta_core/__main__.py
src/chanta_core/cli.py
src/chanta_core/agents/placeholder.py
src/chanta_core/llm/__init__.py
src/chanta_core/llm/client.py
src/chanta_core/llm/lm_studio_client.py
src/chanta_core/llm/messages.py
src/chanta_core/llm/schemas.py
src/chanta_core/llm/types.py
src/chanta_core/runtime/chat_service.py
src/chanta_core/runtime/placeholder.py
src/chanta_core/settings/app_settings.py
src/chanta_core/settings/llm_settings.py
src/chanta_core/traces/placeholder.py
```

## 5. 패키지 메타데이터

`pyproject.toml` 기준:

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "chanta-core"
version = "0.1.0"
description = "CLI utilities for ChantaCore LLM integrations."
readme = "README.md"
requires-python = ">=3.10"
authors = [{ name = "ChantaCore" }]
dependencies = []

[project.scripts]
chanta-cli = "chanta_core.cli:main"

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]
```

중요한 관찰:

- 패키지 버전은 `0.1.0`이다.
- 콘솔 명령은 `chanta-cli`이다.
- `src/` layout을 사용한다.
- 선언된 런타임 의존성은 빈 배열이다.
- 하지만 실제 코드와 스크립트는 `openai`, `python-dotenv` 계열 패키지를 사용한다. 따라서 복원 시 `pyproject.toml`만으로는 현재 로컬 실행 환경이 재현되지 않는다.

## 6. 로컬 Python 환경

확인 시점에 시스템 `python` 명령은 PATH에서 찾을 수 없었다.

```text
python : 'python' 용어가 cmdlet, 함수, 스크립트 파일 또는 실행할 수 있는 프로그램 이름으로 인식되지 않습니다.
```

저장소 내부 가상환경의 Python:

```text
.\.venv\Scripts\python.exe --version
Python 3.11.9
```

확인된 주요 패키지:

```text
openai==2.33.0
python-dotenv==1.2.2
dotenv==0.9.9
httpx==0.28.1
pydantic==2.13.3
```

확인 시점의 전체 `pip freeze`:

```text
annotated-types==0.7.0
anyio==4.13.0
certifi==2026.4.22
-e git+https://github.com/mineworker-x29/ChantaCore.git@265d9bc3c5afc62ab80cf4d39c78d69f716a366d#egg=chanta_core
colorama==0.4.6
distro==1.9.0
dotenv==0.9.9
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
idna==3.13
jiter==0.14.0
openai==2.33.0
pydantic==2.13.3
pydantic_core==2.46.3
python-dotenv==1.2.2
sniffio==1.3.1
tqdm==4.67.3
typing-inspection==0.4.2
typing_extensions==4.15.0
```

복원 명령 예시:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pip install openai==2.33.0 python-dotenv==1.2.2 dotenv==0.9.9
```

`py` launcher가 없는 환경에서는 Python 3.11 실행 파일 경로를 직접 사용해야 한다.

## 7. 환경 변수와 `.env`

`.env.example`에는 다음 키가 있다.

```dotenv
CHANTA_LLM_PROVIDER=

LM_STUDIO_BASE_URL=
LM_STUDIO_API_KEY=
LM_STUDIO_MODEL=
CHANTA_LLM_TIMEOUT_SECONDS=

OLLAMA_BASE_URL=
OLLAMA_API_KEY=
OLLAMA_MODEL=
```

`.env` 파일도 존재하며, 확인 시점에는 위 계열의 키들이 있었다. 단, 실제 값은 비밀 또는 로컬 환경 의존 값일 수 있으므로 이 문서에 기록하지 않는다.

코드 기준 기본값:

```text
CHANTA_LLM_PROVIDER 기본값: lm_studio
LM_STUDIO_BASE_URL 기본값: http://localhost:1234/v1
LM_STUDIO_API_KEY 기본값: lm-studio
LM_STUDIO_MODEL 기본값: 빈 문자열
OLLAMA_BASE_URL 기본값: http://localhost:11434/v1
OLLAMA_API_KEY 기본값: ollama
OLLAMA_MODEL 기본값: 빈 문자열
```

주의:

- `CHANTA_LLM_TIMEOUT_SECONDS`는 `.env.example`과 일부 코드에서 언급되지만, 현재 `src/chanta_core/settings/llm_settings.py`의 `LLMProviderSettings`에는 `timeout_seconds` 필드가 없다.
- 따라서 timeout 설정은 현재 구현 상태에서 일관되게 동작한다고 볼 수 없다.

## 8. 코드 구성

### 8.1 패키지 진입점

`src/chanta_core/__init__.py`:

```python
__version__ = "0.1.0"
```

`src/chanta_core/__main__.py`:

```python
from chanta_core.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
```

의도:

- `python -m chanta_core ...` 형태 실행을 지원하려는 구조이다.

현재 확인:

- 패키지 버전 import는 성공한다.
- `python -m chanta_core show-config`는 현재 ImportError로 실패한다.

### 8.2 CLI

파일: `src/chanta_core/cli.py`

제공하려는 명령:

```text
chanta-cli ask [prompt]
chanta-cli repl
chanta-cli show-config
python -m chanta_core ...
```

주요 옵션:

```text
--system
--model
--base-url
--api-key
--temperature
--max-tokens
```

동작 의도:

- `ask`: 단발 prompt 전송. prompt 인자가 없으면 stdin에서 읽는다.
- `repl`: 대화형 세션. `/exit`, `/reset` 지원.
- `show-config`: 로딩된 설정 출력.

현재 결함:

- `cli.py`는 `chanta_core.llm.client.create_llm_client`를 import하지만, 해당 함수는 현재 존재하지 않는다.
- `cli.py`는 `LLMSettings`, `ChatRequest`를 사용하지만 현재 실제 정의와 맞지 않는다.
- 따라서 CLI는 현재 상태 그대로는 import 단계에서 실패한다.

확인된 오류:

```text
ImportError: cannot import name 'create_llm_client' from 'chanta_core.llm.client'
```

### 8.3 설정 계층

파일: `src/chanta_core/settings/app_settings.py`

역할:

- 현재 작업 디렉터리의 `.env` 또는 `.env.local`을 읽는다.
- 이미 존재하는 OS 환경 변수는 덮어쓰지 않는다.
- `load_llm_settings()` 결과를 `AppSettings`에 담는다.

파일: `src/chanta_core/settings/llm_settings.py`

현재 실제 정의:

```python
@dataclass(frozen=True)
class LLMProviderSettings:
    provider: str
    base_url: str
    api_key: str
    model: str
```

지원 provider:

```text
lm_studio
ollama
```

주의:

- `app_settings.py`는 `LLMSettings`를 import하지만, `llm_settings.py`에는 `LLMSettings`가 없다.
- 이 불일치는 CLI와 `lm_studio_client.py`에서도 반복된다.

### 8.4 LLM 계층

파일: `src/chanta_core/llm/client.py`

현재 실제 구현:

- `openai.OpenAI` 클라이언트를 직접 사용한다.
- `LLMProviderSettings`를 받거나 `load_llm_settings()`로 설정을 읽는다.
- model이 비어 있으면 `ValueError`를 발생시킨다.
- `chat(user_message, system_message=None, temperature=0.7, max_tokens=1024) -> str`
- `chat_messages(messages, temperature=0.7, max_tokens=1024) -> str`

파일: `src/chanta_core/llm/messages.py`

역할:

- system/user message list를 만든다.

파일: `src/chanta_core/llm/types.py`

현재 실제 정의:

```python
Role = Literal["system", "user", "assistant", "tool"]

class ChatMessage(TypedDict):
    role: Role
    content: str
```

주의:

- `ChatRequest`, `ChatResponse`는 현재 `types.py`에 정의되어 있지 않다.
- 그런데 `schemas.py`, `lm_studio_client.py`, `cli.py`는 이 이름들을 import한다.

파일: `src/chanta_core/llm/lm_studio_client.py`

현재 의도:

- 표준 라이브러리 `urllib.request`로 OpenAI-compatible `/chat/completions` endpoint를 호출하는 별도 클라이언트로 보인다.

현재 결함:

- `LLMSettings`, `ChatRequest`, `ChatResponse`가 현재 코드에 없어서 import 또는 실행이 실패할 가능성이 높다.

### 8.5 Runtime 계층

파일: `src/chanta_core/runtime/chat_service.py`

현재 코드:

```python
from __future__ import annotations
from chanta_core import LLMClient

class ChatService:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def run(self, user_input: str) -> str:
        return self.llm.chat(user_message=user_input)
```

현재 결함:

- `chanta_core.__init__`는 `LLMClient`를 export하지 않는다.
- 따라서 이 파일은 현재 그대로 import하면 실패할 가능성이 높다.

### 8.6 Placeholder 계층

현재 placeholder 파일:

```text
src/chanta_core/agents/placeholder.py
src/chanta_core/runtime/placeholder.py
src/chanta_core/traces/placeholder.py
```

의도:

- agents, runtime, traces 영역을 앞으로 확장하기 위한 디렉터리 골격으로 보인다.

## 9. README 상태

README는 다음 사용 흐름을 안내한다.

```text
1. .env.example에서 .env 생성
2. LM Studio에서 local server 실행 및 qwen3.6-35b-a3b:2 로드
3. pip install -e .
4. chanta-cli ask / repl / show-config 사용
```

주의:

- README의 한글 예시 문자열은 확인 시점에 깨진 문자로 보인다.
- README의 사용법은 현재 코드 의도와는 맞지만, 실제 CLI는 ImportError 때문에 바로 실행되지 않는다.

## 10. 복원 절차

가장 보수적인 복원 절차:

```powershell
git clone https://github.com/mineworker-x29/ChantaCore.git ChantaCore
Set-Location ChantaCore
git checkout 265d9bc3c5afc62ab80cf4d39c78d69f716a366d
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pip install openai==2.33.0 python-dotenv==1.2.2 dotenv==0.9.9
Copy-Item .env.example .env
```

그 다음 `.env`에 최소한 다음을 설정한다.

```dotenv
CHANTA_LLM_PROVIDER=lm_studio
LM_STUDIO_BASE_URL=http://localhost:1234/v1
LM_STUDIO_API_KEY=lm-studio
LM_STUDIO_MODEL=<LM Studio에서 로드한 모델 이름>
```

LM Studio 사용 시:

- LM Studio local server를 켠다.
- OpenAI-compatible API endpoint가 `http://localhost:1234/v1`에서 열려 있는지 확인한다.
- `.env`의 `LM_STUDIO_MODEL`을 실제 로드된 모델 이름과 맞춘다.

Ollama 사용 시:

```dotenv
CHANTA_LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_API_KEY=ollama
OLLAMA_MODEL=<Ollama 모델 이름>
```

다만 현재 `LLMClient`는 OpenAI Python SDK를 사용하므로, Ollama의 OpenAI-compatible endpoint가 실제로 같은 schema를 받아야 한다.

## 11. 현재 상태 검증 결과

성공한 확인:

```powershell
.\.venv\Scripts\python.exe -B -c "import sys; sys.path.insert(0, 'src'); import chanta_core; print(chanta_core.__version__)"
```

결과:

```text
0.1.0
```

실패한 확인:

```powershell
.\.venv\Scripts\python.exe -B -m chanta_core show-config
```

결과:

```text
ImportError: cannot import name 'create_llm_client' from 'chanta_core.llm.client'
```

판단:

- 패키지 자체의 최소 import는 가능하다.
- CLI 실행 경로는 현재 깨져 있다.
- 이 판단은 `cli.py`, `client.py`, `types.py`, `llm_settings.py`의 현재 내용과 위 실행 결과에 근거한다.

## 12. v0.1을 고치지 않고 그대로 보존할 때의 체크리스트

그대로 보존하려면 다음을 한다.

```powershell
git status --short
git add docs/chanta_core_v0_1_restore.md
git commit -m "Document ChantaCore v0.1 restore state"
```

이때 선택지는 있다.

- 현재 상태를 있는 그대로 기록만 한다.
- `__pycache__` 추적 문제를 별도 커밋에서 정리한다.
- CLI import 오류를 별도 작업으로 수정한다.
- 아무 것도 더 하지 않고 이 문서만 로컬에 둔다.

## 13. v0.1 이후 수리 후보

현재 근거로 볼 때 우선순위가 높은 수리 후보는 다음이다.

1. `pyproject.toml`에 실제 의존성 추가

```toml
dependencies = [
    "openai>=2.33.0",
    "python-dotenv>=1.2.2",
]
```

2. 설정 타입 통일

현재 `LLMProviderSettings`와 코드 곳곳의 `LLMSettings` 명칭이 충돌한다. 하나로 통일해야 한다.

3. `ChatRequest`, `ChatResponse` 정의 복구 또는 제거

현재 코드에는 두 갈래의 클라이언트 설계가 섞여 있다.

- `LLMClient`: OpenAI SDK 직접 사용, 문자열 반환
- `OpenAICompatibleClient`: urllib 직접 사용, `ChatRequest`/`ChatResponse` 기대

둘 중 하나를 기본 경로로 선택하고 나머지를 맞춰야 한다.

4. `create_llm_client` 구현 또는 CLI 수정

`cli.py`가 기대하는 factory 함수를 만들거나, CLI가 직접 `LLMClient`를 사용하도록 바꿔야 한다.

5. `chanta_core.__init__` export 정리

`runtime/chat_service.py`가 `from chanta_core import LLMClient`를 사용하므로, `__init__.py`에서 `LLMClient`를 export하거나 import 경로를 고쳐야 한다.

6. Git 추적 산출물 정리

이미 추적 중인 `__pycache__`와 `*.pyc`는 `.gitignore`만으로 사라지지 않는다. 별도 정리 커밋이 필요하다.

7. README 인코딩 또는 깨진 예시 문자열 수정

README의 한글 예시는 현재 읽을 수 없는 문자열로 보인다.

## 14. 결론

ChantaCore v0.1은 Python 3.11 기반의 `src/` layout 패키지이며, LM Studio/Ollama 계열 OpenAI-compatible endpoint를 CLI로 호출하려는 초기 골격까지 만들어진 상태다. 다만 현재 HEAD 기준으로 CLI 실행 경로는 import 불일치 때문에 깨져 있으며, 복원 시에는 커밋 `265d9bc3c5afc62ab80cf4d39c78d69f716a366d`, 로컬 의존성 스냅샷, `.env` 변수 구조, 그리고 위의 결함 목록을 함께 보존해야 같은 상태를 재현할 수 있다.

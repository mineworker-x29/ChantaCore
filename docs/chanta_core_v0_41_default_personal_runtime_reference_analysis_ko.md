# ChantaCore v0.41 Default Personal Runtime Reference Analysis

Chanta Minero 선생님, 이 문서는 로컬 참조 시스템을 읽기 전용으로 분석한 결과의 한국어 번역본입니다.

분석 중에는 파일 변경, 의존성 설치, provider 호출, subagent 호출, 네트워크 접근을 하지 않았습니다. 이 파일 저장은 이후 선생님의 명시적 요청에 따라 수행된 별도 작업입니다.

근거 범위는 `references/`, `docs/`, `src/`, `README.md`, `pyproject.toml` 아래의 로컬 파일입니다. OpenCode, Hermes, Schumpeter에 대한 신뢰도는 높고, OpenClaw와 Claude Code는 로컬 소스 디렉터리가 없었기 때문에 신뢰도가 낮습니다. 이 판단은 참조 스냅샷이 새로 추가되거나, 검사하지 않은 위치에 v0.41 구현이 존재할 경우 철회되어야 합니다.

## A. Executive Summary

ChantaCore v0.41이 재사용할 수 있는 핵심 패턴은 다음과 같습니다.

1. 서버 우선이 아니라 CLI 우선 설치형 런타임.
2. `doctor`와 `status`를 일급 명령으로 둔다.
3. Default Personal profile은 identity, config, policy의 묶음이지 sandbox가 아니다.
4. 설정 계층은 built-in defaults, user profile, project context, env overrides로 제한한다.
5. provider metadata와 runtime invocation을 분리한다.
6. completion 요청을 보내지 않는 안전한 provider probe를 둔다.
7. Soul, role, project prompt assembly 순서를 명시한다.
8. append-only session transcript와 PI/OCEL-native trace event를 함께 둔다.
9. write/execution tool보다 read-only skill registry를 먼저 만든다.
10. deny-first permission boundary와 denial event를 기본으로 둔다.

직접 복사하지 말아야 할 것은 다음과 같습니다.

1. OpenCode의 "permission은 sandbox가 아니다"라는 구조를 충분한 안전장치로 간주하는 것.
2. v0.41에서 OpenCode의 server, daemon, web, desktop surface를 여는 것.
3. Hermes의 gateway, cron, messaging, browser, terminal, code execution toolset 전체.
4. toolchain을 내려받는 Hermes식 auto-install bootstrap script.
5. v0.41에서 smart approval이나 permanent allowlist를 두는 것.
6. 로컬에서 검증되지 않은 OpenClaw식 고행동성 자동화.
7. Claude Code를 클론하는 것. 로컬 근거는 shared-loop 영감 정도에 한정된다.
8. v0.41에서 Schumpeter의 `code_edit` mutation surface를 여는 것.
9. trace discipline이 안정되기 전 mission-loop retry/replan autonomy를 여는 것.
10. autonomous memory mutation.

## B. Reference Systems Inspected

| system | path | inspected? | confidence | notes |
|---|---:|---:|---:|---|
| OpenCode | `references/OpenCode` | yes | high | entrypoint, provider, tools, config, agents, events, server boundary 관련 notes 확인. |
| Hermes | `references/Hermes` | yes | medium-high | source/docs 확인. local status는 runtime 미검증 상태라고 밝힘. |
| Schumpeter | `references/schumpeter` | yes | high | simple local Streamlit agent와 PI/OCEL, approval-profile docs 확인. |
| OpenClaw | `references/OpenClaw` | no | low | 디렉터리 없음. Hermes migration/docs를 통한 간접 언급만 있음. |
| Claude Code | `references/Claude Code` | no | low | 로컬 docs/source 없음. ChantaCore README에 shared-loop 영감 언급만 있음. |
| ChantaCore notes | `README.md`, `docs/versions`, `src` | yes | high | 기존 CLI와 PI/OCEL 지향성 확인. |

## C. Install / Entrypoint Findings

| system | install/entrypoint pattern | reusable for ChantaCore? | recommendation |
|---|---|---:|---|
| OpenCode | binary CLI, TUI default, `run`, `serve`, browser/desktop over shared server core | partly | `run`/CLI 형태만 빌리고 server/TUI/desktop은 보류. |
| Hermes | Python console scripts, `setup`, `doctor`, profile home, optional installer | partly | console script와 setup/doctor만 빌리고 dependency-downloading installer는 v0.41에서 거부. |
| Schumpeter | `pip install -r`, `streamlit run`, local LM Studio endpoint | partly | local-provider 단순성과 event log를 빌리고 Streamlit default runtime은 거부. |
| ChantaCore | `pip install -e .`, `chanta-cli`, `python -m chanta_core` | yes | 현재 Python package path를 최소 설치 경로로 사용. |

ChantaCore가 모방할 최소 설치 경로는 `py -m pip install -e .`, `chanta-cli doctor`, `chanta-cli init ...`, `chanta-cli run ...` 순서입니다.

## D. CLI / Command Surface Findings

| command pattern | source system | read-only? | action-taking? | ChantaCore v0.41 recommendation |
|---|---|---:|---:|---|
| `doctor` | Hermes | yes, deep probe 제외 | no | v0.41.1에서 local doctor 구현. provider probe는 분리. |
| `status` / profile status | Hermes, ChantaCore existing personal surface | yes | no | 사용자에게 보여줄 readiness view로 안정화. |
| `init` / setup | Hermes | no | config write | idempotent Default Personal init 구현. |
| `provider doctor` | Hermes, Schumpeter local endpoint | mostly | remote일 경우 network 가능 | explicit safe probe 구현. completion은 금지. |
| `run` / `ask` | OpenCode, Hermes, Schumpeter | no | provider invocation | v0.41.4에서 single-turn text runtime 구현. |
| `trace recent` | Schumpeter, ChantaCore OCEL | yes | no | v0.41.5에서 구현. |
| `serve`, gateway, daemon | OpenCode, Hermes | no | runtime exposure | v0.42+로 보류. |
| shell/edit/apply/subagent | OpenCode, Hermes, Schumpeter docs | no | yes | v0.41에서 닫아 둔다. |

## E. Profile / Config Findings

| pattern | source | benefit | risk | ChantaCore adaptation |
|---|---|---|---|---|
| Profile as separate home/config | Hermes | personal identity와 state boundary가 명확함 | sandbox로 오해될 수 있음 | `default-personal` profile에 "not a sandbox" 상태 문구를 명시. |
| Multi-source schema config | OpenCode | 예측 가능한 layering | 복잡한 override 위험 | built-in defaults, user profile, project file, env만 사용. |
| Project instruction files | Hermes/OpenCode/ChantaCore | global mutation 없이 local context 제공 | prompt injection | provenance, scan, size limit와 함께 로드. |
| Remote/org config | OpenCode | enterprise control | v0.41 범위 초과 | 보류. |

## F. Provider / Model Findings

| pattern | source | benefit | risk | v0.41 recommendation |
|---|---|---|---|---|
| Provider metadata registry | OpenCode | provider quirks를 runtime에 hardcode하지 않음 | registry sprawl | OpenAI-compatible/local 중심의 작은 static registry. |
| Auth separated from provider metadata | OpenCode/Hermes | secret leakage 감소 | env misconfig | env var 이름만 저장하고 값은 항상 redaction. |
| Local LM Studio endpoint | Schumpeter/Hermes | lightweight personal runtime 경로 | endpoint availability 변동 | optional loopback `/models` probe 지원. |
| Full completion probe | many agents | 실제 call path 확인 | token cost와 prompt leakage | `provider doctor`에서는 거부. completion은 `run`에서만 허용. |

v0.41.3의 최소 안전 provider probe는 config validation, credential presence 확인, 짧은 timeout의 optional loopback `/models` probe, trace emission입니다. user prompt/completion 전송, secret 출력, config mutation은 하지 않습니다.

## G. Prompt Assembly / Identity Findings

| pattern | source | benefit | risk | ChantaCore adaptation |
|---|---|---|---|---|
| `SOUL.md` identity | Hermes | 안정적인 persona layer | identity text 과신 | Profile Soul은 identity 전용으로 사용하고 scan/truncate. |
| `AGENTS.md` project rules | Hermes/Claude-style convention | project-local behavior | prompt injection | project context로 로드하되 safety override를 더 높은 계층에 둔다. |
| Agent profile controls tools/model/permissions | OpenCode | role과 runtime behavior 일치 | 초기 단계에서 과도한 권한 | v0.41에서는 identity와 read-only policy에만 사용. |
| Evidence-first base prompt | Schumpeter | PI-native reasoning과 잘 맞음 | 답변이 장황해질 수 있음 | ChantaCore runtime invariant로 사용. |

권장 prompt order는 safety invariant, Soul, profile role, project/domain instructions, read-only skill policy, session context, user input 순서입니다.

## H. Session / Memory Findings

| pattern | source | benefit | risk | ChantaCore adaptation |
|---|---|---|---|---|
| SQLite session DB + FTS | Hermes | searchable durable sessions | v0.41에는 무거움 | FTS/message DB는 보류. |
| JSONL event/session log | Schumpeter | 단순한 append-only audit | query 성능 약함 | 초기 transcript에 사용. |
| OCEL canonical trace | Schumpeter/ChantaCore | PI-native reconstruction | schema drift | OCEL event를 canonical로 두고 JSONL은 operational mirror로 둔다. |
| Mutable memory files/tools | Hermes | personal continuity | prompt injection/state pollution | autonomous memory mutation은 보류. |

v0.41의 최소 session store는 profile/provider/prompt bundle에 연결된 per-session append-only JSONL transcript와 OCEL trace event입니다.

## I. Tool / Skill Registry Findings

| pattern | source | benefit | risk | ChantaCore adaptation |
|---|---|---|---|---|
| Central tool registry | OpenCode | 모든 tool을 하나의 gate에서 통제 | 빠르게 과대해짐 | 작은 read-only registry만 구현. |
| Toolsets | Hermes | capability group을 사용자 설정 가능 | unsafe combination 위험 | `readonly`, `trace`, `profile`, `provider_probe`만 사용. |
| Code edit surface | Schumpeter | controlled mutation path | 여전히 mutation | v0.41에서 거부. |
| Skill delegation/subagents | OpenCode/Hermes | task scaling | context/control risk | v0.41에서 닫음. |

v0.41 read-only skills는 file excerpt, repo search, docs/reference search, profile status, config view, trace recent, provider status/probe로 제한합니다.

## J. Permission / Safety Findings

| pattern | source | benefit | risk | ChantaCore adaptation |
|---|---|---|---|---|
| allow/ask/deny rules | OpenCode | UX가 명확함 | sandbox가 아님 | deny-first gate 사용. write tool에는 아직 ask도 열지 않음. |
| Hardline dangerous command block | Hermes | catastrophic command 차단 | pattern gap | primary safety가 아니라 secondary guard로 사용. |
| Approval profiles | Schumpeter | read/propose/write separation | scope creep | v0.41 profile은 observe/read-only plus provider-run exception. |
| "No sandbox" disclosure | OpenCode | boundary가 정직함 | 사용자가 무시할 수 있음 | doctor/status에서 closed capability를 명시. |

v0.41은 apply/edit/shell/subagent/network/credential command를 기본 차단하고 `skill_invocation_denied`, `unsafe_command_denied` event를 내야 합니다.

## K. Event / Trace Findings

| pattern | source | benefit | risk | ChantaCore adaptation |
|---|---|---|---|---|
| Event bus and stream parts | OpenCode | rich reconstruction | plumbing이 과함 | event vocabulary만 빌리고 server stream은 보류. |
| JSONL append | Schumpeter | minimal observable runtime | query limit | raw/operational trace로 사용. |
| OCEL dual-write | Schumpeter v3.9 / ChantaCore | PI-native process reconstruction | mapper failure | validation test 필수. |
| Hook checked/blocked events | Schumpeter | safety evidence | event spam | gate decision과 denial 중심으로 제한. |

최소 event는 `runtime_started`, `profile_loaded`, `prompt_assembled`, `session_created`, `provider_probe_*`, `agent_loop_started`, `assistant_response_recorded`, `skill_gate_checked`, `skill_invocation_denied`, `unsafe_command_denied`, `doctor_check_completed`입니다.

## L. Subagent / Delegation Findings

| pattern | source | benefit | risk | ChantaCore adaptation |
|---|---|---|---|---|
| Task tool/subagent | OpenCode | parallel reasoning | parent-child leakage | future only. |
| Delegation toolset | Hermes | rich personal assistant behavior | unsafe autonomy | closed. |
| Mission loop/retry | Schumpeter roadmap | persistence | runaway behavior | trace/report 안정 이후 v0.42+로 보류. |

빌릴 수 있는 미래 설계 원칙은 child session context isolation, explicit budget, parent lineage, quarantined result입니다. v0.41에서는 delegation을 deny해야 합니다.

## M. Doctor / Observability Findings

| pattern | source | benefit | risk | ChantaCore adaptation |
|---|---|---|---|---|
| Hermes doctor/status | comprehensive readiness | deep mode가 side effect를 낼 수 있음 | local doctor와 provider doctor를 분리. |
| Schumpeter events tab | user-visible trace | UI dependency | CLI `trace recent`로 대체. |
| OpenCode server diagnostics | multi-client에 유용 | server 범위 초과 | 보류. |

v0.41.1 doctor는 Python/package version, cwd, writable runtime dir, profile/config paths, AGENTS/Soul presence, OCEL store, read-only registry, closed capabilities를 보여줘야 합니다.

v0.41.6 doctor는 provider readiness, session store, trace write/read, denial check까지 포함해야 합니다.

## N. Proposed ChantaCore v0.41 Architecture Delta

| version | should borrow/adapt/reject | required artifacts | required tests | risks / withdrawal conditions |
|---|---|---|---|---|
| v0.41.0 Default Personal Profile Runtime | Hermes profile idea를 빌리되 PI profile로 조정. sandbox 표현은 거부. | profile schema, default-personal loader, status model | profile load, missing config, status no-mutation | profile이 security isolation으로 오해되면 철회. |
| v0.41.1 Installable CLI Bootstrap | Hermes doctor/setup을 빌리고 기존 `chanta-cli`에 맞춤. auto-download installer는 거부. | `doctor`, `init`, `profile status`, help text | install smoke, parser tests, idempotent init | install이 외부 서비스에 의존하면 철회. |
| v0.41.2 Prompt Assembly & Session Store | Soul/AGENTS split과 evidence-first prompt를 빌림. | prompt assembler, session JSONL, OCEL session events | assembly order, truncation, provenance, append-only | prompt source 추적이 불가능하면 철회. |
| v0.41.3 Safe Provider Probe & Read-only Skill Registry | provider metadata와 doctor를 빌림. completion probe는 거부. | provider registry, `provider doctor`, read-only skill registry | no completion call, secret redaction, denied write skill | probe가 credential을 노출하거나 invocation을 요구하면 철회. |
| v0.41.4 Minimal AgentLoop | OpenCode shared loop shape를 빌리되 single-turn only로 제한. tools/subagents는 거부. | one-shot `run/ask`, provider adapter, stop condition | provider unavailable, one response, no tool escalation | loop가 자율적으로 action을 실행할 수 있으면 철회. |
| v0.41.5 Event Trace Emission & Runtime Report | Schumpeter OCEL/event taxonomy를 빌림. | trace writer, `trace recent`, runtime report | event schema, reconstruction, denial event | trace가 prompt/session/provider object를 재구성하지 못하면 철회. |
| v0.41.6 Installable Default Personal User Test Release | CLI/profile/provider/run/trace/safety-denial 결합. | release checklist, Windows test script, docs | full user flow, mock provider, unsafe denial | unsafe capability 없이 first useful response가 불가능하면 scope 재조정. |

## O. Minimal v0.41.6 User Test Flow

제안하는 Windows PowerShell 명령은 다음과 같습니다.

```powershell
Set-Location D:\ChantaResearchGroup\ChantaCore
py -m pip install -e .
chanta-cli --version

chanta-cli doctor

chanta-cli init default-personal --home "$env:LOCALAPPDATA\ChantaCore"

chanta-cli profile status --profile default-personal

chanta-cli provider doctor --profile default-personal --no-completion

chanta-cli run --profile default-personal "Summarize what ChantaCore is in three bullets."

chanta-cli trace recent --profile default-personal --limit 10

chanta-cli safety check-command --profile default-personal --command "Remove-Item -Recurse -Force C:\"
```

마지막 명령은 어떤 것도 실행하지 않아야 합니다. denial을 반환하고 denial trace event를 남기는 것이 목적입니다.

## P. Risk Register

| risk class | level | reason | mitigation / withdrawal condition |
|---|---:|---|---|
| implementation risk | medium | CLI/profile/session/provider가 여러 surface에 걸침 | v0.41은 CLI-only, single-turn으로 제한. |
| safety risk | high if write/shell tools open | 참조 시스템들이 강력한 execution system을 포함 | mutation/execution/subagents/network를 hard-close. |
| provider risk | medium | auth/env/local endpoint가 환경별로 다름 | provider doctor는 readiness만 확인하고 completion은 보내지 않음. |
| install risk | medium | local package version/docs mismatch가 관찰됨 | Windows에서 editable install과 script entrypoint 테스트. |
| user-experience risk | medium | 명령이 많으면 first-run path가 혼란스러움 | `doctor -> init -> provider doctor -> run -> trace`를 canonical path로 둠. |
| PI trace risk | medium | event taxonomy가 drift될 수 있음 | event schema test와 reconstruction test 필수. |

## Q. Final Recommendation

ChantaCore v0.41이 가장 먼저 구현해야 할 것은 CLI-only Default Personal profile, install/doctor/init/profile status, ordered Soul/Role/Domain prompt assembly, append-only session transcript, OCEL-native trace events, safe provider doctor, read-only skill registry, one-shot `run/ask`, `trace recent`, deliberate unsafe-command denial test입니다.

v0.42+로 미뤄야 할 것은 server/daemon/TUI/web, SQLite FTS session search, mutable personal memory, subagents, mission retry/replan loops, gateways, MCP-style extensions, browser/terminal/code-edit tools, approval workflows입니다.

ChantaCore가 직접 복사하면 안 되는 것은 reference system들의 broad execution posture, no-sandbox permission UX, auto-installing bootstrap scripts, gateway/messaging automation, autonomous mutation loops입니다. 이 패턴들은 ChantaCore가 먼저 traceability, denial behavior, bounded single-turn execution을 증명하기 전에는 PI-native Default Personal Runtime과 충돌합니다.

v0.41.6은 installable CLI personal runtime, read-only skills, single-turn provider use로 범위를 제한하면 실현 가능합니다. 그러나 daemon, subagents, shell/edit tools, persistent mission loops, autonomous memory까지 포함하려 한다면 v0.41.6 안에서 안전성과 PI trace boundary를 유지한 채 실현 가능하다고 보기 어렵습니다.

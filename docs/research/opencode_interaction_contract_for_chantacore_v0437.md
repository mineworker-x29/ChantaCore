# OpenCode Interaction Contract for ChantaCore v0.43.7

## 1. Executive Summary

- 확인된 핵심은 OpenCode-style UX가 더 많은 기능을 여는 문제가 아니라는 점이다. 핵심은 런타임 상태, 이벤트, 도구 상태, 권한 상태, 디버그 정보를 사용자-facing 답변과 분리하는 것이다.
- ChantaCore의 현재 UX 문제는 기능 부족보다 router/renderer leakage에 가깝다. 일반 대화가 summary artifact 경로로 흘러가고, artifact envelope와 debug metadata가 기본 응답에 노출된다.
- OpenCode 참고 자료에서 가장 중요한 패턴은 `session -> message -> part -> event -> renderer`의 분리다. 내부에는 text/reasoning/tool/step/error/permission 상태가 저장되지만, 화면에는 렌더러가 선택한 형태만 보인다.
- ChantaCore v0.43.7은 OpenCode의 coding-agent 기능을 복사하면 안 된다. shell, edit, repo search, tool calling, subagent는 계속 닫힌 상태여야 한다.
- ChantaCore가 배워야 할 것은 "일반 메시지", "명령", "도구/이벤트 상태", "권한/안전 상태", "디버그/진단 표면"을 섞지 않는 상호작용 계약이다.
- 일반 텍스트 입력은 기본적으로 일반 답변으로 렌더링되어야 한다. `/summary` 같은 명시적 artifact 명령만 artifact renderer로 가야 한다.
- `넌 누구야`는 identity_question으로 라우팅되어 짧은 identity answer를 내야 한다. `업무 요약`, `type: summary`, `grounding:`, `source:`, `safety:`가 나오면 실패다.
- 저장소 상태 요청은 "v0.43에서는 저장소를 직접 읽지 않는다"는 capability boundary answer가 되어야 한다. git/shell/repo search를 실제로 수행하거나 수행했다고 암시하면 실패다.
- v0.44 Controlled Workspace Read는 이 UX repair가 통과한 뒤 설계해야 한다. 기본 대화 출력이 artifact/debug metadata로 오염된 상태에서는 workspace read를 열면 혼란과 위험이 커진다.

## 2. Sources Inspected

### Confirmed from source

| path | contains | relevance | confidence |
|---|---|---|---|
| `references/OpenCode/notes/OpenCode 기본 분석1.md` | OpenCode를 세션 기반 런타임, 도구 실행 시스템, 권한 정책, 이벤트 스트림, 다중 클라이언트 구조로 종합한 분석 | OpenCode를 기능 목록이 아니라 runtime/UI boundary reference로 볼 근거 | 높음 |
| `references/OpenCode/notes/opencode-overview.md` | monorepo 구조, CLI/TUI/server/app/desktop/SDK/plugin 패키지 개요 | OpenCode의 runtime core와 client shell 분리 근거 | 높음 |
| `references/OpenCode/notes/03_user_request_to_response_flow.md` | TUI/app/run 입력이 `session.prompt`, `session.command`, `session.shell`로 분기되고, MessageV2 part와 event로 저장되는 흐름 | plain prompt와 command/shell 경계, message part 저장/렌더링 분리 근거 | 높음. 단 일부 한글 주석은 인코딩 깨짐 |
| `references/OpenCode/notes/05_tool_system_analysis.md` | Tool.Def, ToolRegistry, Permission.ask/reply, tool lifecycle event 정리 | tool/event state가 내부 상태로 관리된다는 근거 | 높음 |
| `references/OpenCode/notes/08_client_server_boundary.md` | HTTP/JSON, SSE, WebSocket, SDK, TUI worker-RPC 경계 | runtime event와 UI client rendering이 분리된다는 근거 | 높음 |
| `references/OpenCode/upstream/opencode/packages/opencode/src/session/message-v2.ts` | text, reasoning, tool, step, patch, subtask 등 message part schema와 message.part events | "assistant output"과 "runtime parts"가 구조적으로 분리됨 | 높음 |
| `references/OpenCode/upstream/opencode/packages/opencode/src/session/processor.ts` | LLM stream event를 text/reasoning/tool/step part로 반영하고 session.error/status를 publish | 내부 event 처리와 최종 렌더링 분리 근거 | 높음 |
| `references/OpenCode/upstream/opencode/packages/opencode/src/session/index.ts` | message/part update, part delta, session error/status event publication | process evidence를 저장하되 사용자 응답과 별도 관리하는 구조 | 높음 |
| `references/OpenCode/upstream/opencode/packages/opencode/src/cli/cmd/run.ts` | non-TUI run mode에서 text part, tool part, error, permission.asked를 별도 처리 | 일반 텍스트와 tool/error/permission 출력이 별도 경로라는 근거 | 중간-높음 |
| `references/OpenCode/upstream/opencode/packages/opencode/src/cli/cmd/tui/context/sync.tsx` | permission, session_status, message.part.updated/delta/removal을 sync store에 반영 | UI가 event store를 보고 렌더링한다는 근거 | 높음 |
| `references/OpenCode/upstream/opencode/packages/opencode/src/cli/cmd/tui/routes/session/index.tsx` | TextPart와 ToolPart를 서로 다른 컴포넌트로 렌더링하고, 성공한 tool detail은 조건부 숨김 | message part별 renderer 분리 근거 | 중간. 전체 UI 세부는 완전 감사하지 않음 |
| `references/OpenCode/upstream/opencode/packages/opencode/src/permission/index.ts` | allow/deny/ask, permission.asked/replied, DeniedError/Rejection | permission state가 normal answer text와 별도 이벤트로 처리됨 | 높음 |
| `src/chanta_core/external_harness/opencode_profile.py` | OpenCode surface/capability/risk taxonomy, prohibited runtime actions | ChantaCore가 OpenCode를 capability clone이 아니라 observation/reference로 다뤄온 기존 근거 | 높음 |
| `docs/versions/v0.32/v0.32.1_opencode_style_harness_observation_profile.md` | OpenCode-style harness observation profile과 no-execution boundary | OpenCode 참조 시 shell/edit/tool/runtime 실행을 열지 말아야 한다는 기존 정책 | 높음 |
| `docs/chanta_core_v0_41_default_personal_runtime_reference_analysis_ko.md` | OpenCode에서 CLI/run, config, provider, tool, permission, event pattern을 일부 차용하되 server/TUI/desktop은 유보하자는 분석 | ChantaCore 기존 방향과 이번 UX 분석의 연결점 | 중간. 파일 일부가 인코딩상 깨져 보임 |
| `src/chanta_core/personal_runtime/default_personal_business_ux.py` | v0.42.9 default vs debug output policy, debug disclosure policy, runtime identity answer policy | ChantaCore 내부에도 이미 clean default 원칙이 있었음을 확인 | 높음 |
| `src/chanta_core/personal_runtime/default_personal_work_artifacts.py` | `_render_artifact`가 `type:`, `grounding:`, `confidence:`, `source:`, `safety:`를 기본 출력에 포함 | 현재 관찰된 bad output의 직접 원인 중 하나 | 높음 |
| `src/chanta_core/personal_runtime/default_personal_work_session.py` | work-session command parser/dispatcher, v0.43.7 후보 router integration, explicit command handling | plain input과 slash command 경계 분석에 필요 | 높음 |
| `src/chanta_core/personal_runtime/default_personal_grounded_synthesis.py` | grounded artifact 렌더링에서 evidence ids와 raw safety footer 노출 | grounded artifact metadata disclosure 정책 설계에 필요 | 높음 |
| `docs/versions/v0.43/v0.43.0_business_work_session_pilot_restore.md` | `/summary`, `/todo`, `/memo`, `/decision`, `/handoff` 등 business artifact command contract | artifact command가 명시적이어야 한다는 기준 | 높음 |
| `docs/versions/v0.43/v0.43.1_business_flow_artifact_quality_restore.md` | business artifact model, sections, grounding classes, confidence, source summary, verification flags | artifact 내부 구조와 사용자 출력 분리 필요성 | 높음 |
| `docs/versions/v0.43/v0.43.7_default_conversation_router_minimal_output_restore.md` | v0.43.7 후보 restore 문서 | 현재 작업트리에 이미 후보 해결책이 있음을 확인. 이번 문서는 그 배경 분석용 | 높음 |
| `tests/test_v0437_default_conversation_router_minimal_output.py` | intent classification, identity answer, repository status boundary, renderer suppression tests | acceptance-test gap을 메우는 테스트 방향 확인 | 높음 |

### Interpretation

- OpenCode는 사용자에게 내부 객체를 그대로 dump하지 않는다. 내부적으로는 message parts/events/permission state가 풍부하지만, normal chat stream에는 선택된 renderer output만 보인다.
- OpenCode의 tool/event UI는 ChantaCore가 당장 따라 할 기능이 아니다. 그러나 "내부 상태는 구조화하고, 기본 응답에는 필요한 것만 렌더링한다"는 계약은 ChantaCore v0.43.7에 바로 적용 가능하다.
- ChantaCore v0.42.9의 clean default 원칙과 v0.43.1 artifact envelope 사이에 일관성 단절이 생겼다. v0.43.7은 새 기능보다 이 단절을 복구하는 패치로 보는 것이 맞다.

### Hypothesis

- 사용자가 느낀 "template/debug generator" 감각은 provider 답변 품질보다 output composition failure의 영향이 더 크다. 즉 provider가 잘 대답해도 artifact wrapper가 붙으면 실패한다.
- v0.44 workspace read를 열기 전에 이 렌더링 계약을 고치지 않으면, 실제 read evidence까지 normal answer에 섞여 더 큰 UX/안전 혼란을 만들 가능성이 높다.

### Unknown / needs verification

- OpenCode 현재 최신 upstream이 로컬 snapshot 이후 어떻게 바뀌었는지는 이 분석에서 확인하지 않았다. 이 문서는 로컬 `references/OpenCode` 기준이다.
- OpenCode TUI의 모든 세부 렌더링 조건은 완전 감사하지 않았다. 다만 TextPart/ToolPart/permission/session status가 분리되어 있다는 구조는 확인했다.
- ChantaCore 현재 작업트리에는 v0.43.7 후보 구현이 존재하지만, 실제 수동 acceptance transcript가 통과했는지는 이 분석에서 실행하지 않았다.

## 3. OpenCode Interaction Model

OpenCode의 상호작용 모델은 단일 문자열 응답 모델이 아니다. 확인된 구조는 다음에 가깝다.

- session: 대화와 작업 상태의 상위 컨테이너다. session status는 busy, idle 같은 별도 이벤트로 관리된다.
- user message: 사용자의 입력은 message와 parts로 저장된다. 파일/리소스가 붙을 수 있고, 단순 텍스트도 text part가 된다.
- assistant message: assistant 답변도 단일 문자열이 아니라 여러 part의 집합이다.
- message parts: text, reasoning, tool, step-start, step-finish, patch, subtask 같은 part type이 있다.
- events: message.updated, message.part.updated, message.part.delta, message.part.removed, session.error, session.status, permission.asked/replied 등이 별도 event stream으로 흐른다.
- tool execution state: tool call은 pending/running/completed/error 상태와 input/output/metadata를 가진 part로 저장된다.
- permission state: permission request는 answer text가 아니라 permission.asked 이벤트와 pending request store로 관리된다.
- rendering layer: TUI/run/app은 stored message parts와 events를 보고 text/tool/error/status/permission을 별도 방식으로 렌더링한다.
- status/debug surfaces: session.status, permission list, tool details, errors는 normal assistant text와 같은 층위가 아니다.

ChantaCore에 중요한 해석은 다음이다. Process Intelligence-native runtime은 내부 evidence를 많이 저장해야 한다. 하지만 저장된 evidence가 곧 기본 사용자 출력이어서는 안 된다. OpenCode식으로 말하면 `V043BusinessArtifactEnvelope`는 session/message/object state이고, 사용자에게 보이는 것은 renderer가 고른 projection이어야 한다.

## 4. OpenCode User-Facing Rendering Contract

### What is shown in the normal chat stream?

확인된 범위에서 normal chat stream의 중심은 assistant text part다. OpenCode run mode는 `message.part.updated`를 보다가 `part.type === "text"`이고 완료된 경우 text를 출력한다. TUI도 TextPart를 별도 renderer로 표시한다.

ChantaCore 번역: 기본 대화에는 assistant answer만 보여야 한다. artifact type, grounding class, confidence, source summary, safety flags는 기본 대화 본문이 아니다.

### What is hidden from the normal chat stream?

OpenCode 내부에는 reasoning part, tool part, step metadata, permission state, session status, error object가 있지만, 이것이 전부 assistant text로 합쳐지지는 않는다. tool part는 tool renderer로, permission은 permission UI/state로, error는 error path로 간다.

ChantaCore 번역: grounding/source/safety/trace/run/session metadata는 보관하되 기본 답변에 raw key-value로 붙이지 않는다.

### When are tool/event/debug details shown?

OpenCode에서는 tool part나 permission request가 발생했을 때 별도 UI 경로로 보인다. TUI에는 tool별 컴포넌트가 있고, run mode도 tool part를 text part와 별도로 처리한다. debug/status성 정보는 session.status, event sync, route/API에서 다뤄진다.

ChantaCore 번역: `/what-happened`, `/report`, `/trace`, `/artifact last --debug`, `/grounding-check`, `/evidence used` 같은 명시 표면에서만 metadata를 보여준다.

### How are errors shown?

OpenCode run mode는 `session.error` 이벤트를 별도로 받아 `UI.error(...)`로 출력한다. tool error도 tool part state로 처리된다.

ChantaCore 번역: provider parse failure, unavailable capability, no evidence, denied action은 artifact wrapper가 아니라 ErrorRenderer 또는 StatusRenderer가 짧고 명확히 처리해야 한다.

### How are unavailable capabilities shown?

OpenCode는 permission system과 command/tool boundary를 통해 허용되지 않는 요청을 별도 상태로 처리한다. ChantaCore는 아직 tool execution을 열지 않으므로 더 단순해야 한다. "저장소를 읽지 않았다", "shell은 닫혀 있다"처럼 capability boundary answer를 제공하되 raw safety footer는 붙이지 않는다.

### How are status/diagnostics accessed?

OpenCode의 status는 event/API/UI state로 접근된다. ChantaCore의 대응 표면은 `/what-happened`, `/report`, `chanta-cli run-report`, `chanta-cli trace`, provider status, pilot/polish report다.

### How does OpenCode avoid dumping internal objects into normal response text?

핵심은 내부 상태가 text body와 별도 type을 가진다는 점이다. tool output, permission state, step metadata가 모두 assistant text에 문자열로 붙는 구조가 아니다. ChantaCore도 artifact envelope를 직접 render text로 쓰지 말고, renderer projection을 거쳐야 한다.

## 5. OpenCode Intent / Command Boundary

OpenCode 참고 자료에서 확인되는 입력 경계는 다음과 같다.

- plain natural-language prompt: `session.prompt` 경로.
- slash command or explicit command: `session.command` 경로.
- shell action: `session.shell` 경로. ChantaCore v0.43.7에서는 열면 안 되는 경로다.
- status/debug request: session/status/event/API 또는 command surface에서 처리.
- permission request: `permission.asked` event와 permission reply route.
- tool action: model/tool lifecycle part와 permission gate.
- error path: `session.error` 또는 tool error state.

ChantaCore 제안 route type:

| route type | 입력 예 | renderer | provider default | high-risk capability |
|---|---|---|---|---|
| `identity_question` | `넌 누구야`, `ChantaCore가 뭐야` | MinimalConversationRenderer | no | closed |
| `capability_question` | `무엇을 할 수 있어?` | MinimalConversationRenderer 또는 StatusRenderer | no | closed |
| `runtime_status_question` | `지금 너의 상태 체크해봐` | StatusRenderer | no | closed |
| `repository_status_request` | `저장소 상태 점검해줘`, `git 상태 봐줘` | Error/Status boundary answer | no | closed |
| `general_chat` | 일반 대화 | MinimalConversationRenderer | optional only if existing chat path requires, not artifact | closed |
| `explicit_artifact_command` | `/summary`, `/memo`, `/decision`, `/handoff` | ArtifactRenderer | existing explicit flow only | closed |
| `evidence_command` | `/recall`, `/evidence`, `/use-evidence` | EvidenceRenderer | no by default except existing bounded behavior | closed |
| `grounded_command` | `/grounded-summary`, `/grounding-check` | GroundedArtifactRenderer or DiagnosticRenderer | explicit only | closed |
| `pilot_command` | `/pilot score`, `/polish report`, `/v044 readiness` | Report/StatusRenderer | no | closed |
| `debug_or_report_command` | `/what-happened`, `/report`, `/trace`, `--debug` | DebugRenderer/DiagnosticRenderer | no unless existing report uses bounded data | closed |
| `unknown` | 빈 입력 또는 미분류 | ErrorRenderer or minimal help | no | closed |

중요 불변식: plain text는 "요약해줘"처럼 명확한 요약 요청이 아니면 summary artifact로 가지 않는다. slash command 없이 artifact mode로 들어가는 예외는 아주 좁아야 하며 acceptance test로 고정해야 한다.

## 6. ChantaCore Current UX Failure Analysis

사용자 관찰 사례:

```text
User:
넌 누구야

Bad output:
업무 요약
type: summary

## 핵심 요약

## 핵심 요약
...
grounding: data_based_interpretation; confidence: medium
source: provider output over explicit user/session context
safety: shell=false; subagent=false; workspace_mutated=false; memory_mutated=false; production_certified=false
```

### Failure classification

| failure | classification | source basis | why it is bad |
|---|---|---|---|
| plain text가 summary artifact로 감김 | router failure | v0.43.0은 `/summary`를 명시 command로 정의했지만, observed behavior는 plain identity question을 summary flow로 처리 | 사용자는 질문했는데 보고서 템플릿을 받는다 |
| `업무 요약`, `type: summary`가 보임 | artifact-envelope leakage | `default_personal_work_artifacts.py`의 `_render_artifact`가 title과 `type:`을 기본 rendered_text에 포함 | internal artifact type이 normal answer에 노출된다 |
| `grounding:`, `confidence:`, `verification_required:` 노출 | debug disclosure failure | `_render_artifact`가 section마다 grounding/confidence/verification을 raw line으로 출력 | 검토용 metadata가 기본 대화 본문이 된다 |
| `source:` 노출 | debug disclosure failure | `_render_artifact`가 `source_summary`를 raw line으로 출력 | source는 중요하지만 기본 답변에서는 자연어/각주/명시 명령 표면이어야 한다 |
| raw `safety: shell=false...` footer | debug disclosure failure | `_render_artifact`와 grounded renderer가 safety footer를 붙임 | 안전성을 말하는 방식이 사용자-facing 답변을 오염시킨다 |
| `## 핵심 요약` 중복 | renderer failure + prompt/template failure | provider output에 heading이 이미 있는데 artifact renderer도 section heading을 추가할 수 있음 | 템플릿 생성기처럼 보인다 |
| `알 수 없음` 빈 섹션 반복 | prompt/template failure + renderer failure | v0.43 artifact defaults가 required sections를 unknown으로 채움 | unknown을 보존해야 할 때와 숨겨야 할 때를 구분하지 못한다 |
| repository status request가 summary artifact로 감김 | router failure + unavailable capability response failure | 저장소 읽기/repo search는 닫혀 있는데 일반 summary로 처리 | 사용자는 실제 점검 여부를 오해할 수 있다 |
| normal answer/report/debug 구분 불가 | renderer architecture failure | artifact envelope, safety footer, PI metadata가 같은 text stream에 붙음 | 사용자가 "답변"과 "진단 로그"를 구분하지 못한다 |
| 이런 케이스가 늦게 발견됨 | acceptance-test gap | v0.42.9 clean default tests는 있었으나 v0.43 artifact flow가 그 원칙을 깨는 golden transcript가 부족 | v0.43.7에는 transcript tests가 필요하다 |

## 7. OpenCode-to-ChantaCore UX Translation

| OpenCode pattern | Why it matters | ChantaCore equivalent | Required v0.43.7 behavior | Testable acceptance criterion |
|---|---|---|---|---|
| text part와 tool part가 다른 type | assistant answer와 runtime action state가 섞이지 않음 | conversation answer vs artifact/evidence/debug object 분리 | plain text는 MinimalConversationRenderer로 간다 | `넌 누구야` 출력에 `type: summary` 없음 |
| session event stream | 내부 상태를 추적하되 답변 본문에 dump하지 않음 | trace/run/report evidence | trace는 `/what-happened`/`/report`에서만 노출 | default answer에 `run_id`, `trace`, raw safety footer 없음 |
| permission.asked event | 권한 요청이 text answer가 아니라 별도 상태 | safety boundary / unavailable capability answer | repo/shell/edit 요청은 짧은 boundary answer | repo status가 "점검 완료"라고 말하지 않음 |
| command route와 prompt route 분리 | slash command는 명령, plain prompt는 대화 | slash command parser + intent router | `/summary`만 artifact renderer로 간다 | plain identity/status는 summary command result가 아님 |
| tool renderer 조건부 표시 | tool 상태는 필요할 때 별도 UI로 표시 | evidence/grounding/debug/report renderer | evidence ids는 grounded/evidence 명령에서만 표시 | plain answer에 evidence id/raw source 없음 |
| error path 분리 | 오류가 내부 객체 dump가 되지 않음 | ErrorRenderer | no repo read는 간단한 unavailable response | repository request가 stack/debug/report가 아님 |
| status API/sync store | status는 answer body가 아니라 status surface | `/status`, provider status, pilot readiness | runtime status는 StatusRenderer | status request가 artifact title로 시작하지 않음 |
| message part vs rendered text separation | 저장 형식과 화면 형식이 다름 | ArtifactEnvelope vs rendered projection | envelope는 저장, renderer는 출력 | `_render_artifact` raw output을 직접 default로 쓰지 않음 |
| internal trace vs user answer separation | process reviewability와 UX를 동시에 만족 | PI records vs default answer | PI metadata는 report/debug에 보존 | `/what-happened`에는 metadata 허용, plain answer에는 금지 |

## 8. ChantaCore v0.43.7 Interaction Contract

### Plain conversation

Plain text input must not become summary artifact by default.

규칙:

- `/summary` 또는 명확한 "요약해줘" 요청이 아니면 summary artifact로 라우팅하지 않는다.
- 일반 대화는 MinimalConversationRenderer를 사용한다.
- 기본 출력은 짧고, 사용자가 읽을 답변만 포함한다.
- 내부 artifact class name, type label, grounding/source/safety raw line을 포함하지 않는다.

### Identity question

`넌 누구야` expected route: `identity_question`.

Expected default output:

```text
저는 ChantaCore default-personal runtime에서 동작하는 업무 보조 에이전트입니다.
대화 기반 업무 정리, 요약, TODO 추출, 의사결정 정리, 인수인계문 작성, 로컬 노트/근거 조회를 도와드릴 수 있습니다.
현재는 저장소 직접 읽기, 파일 수정, 셸 실행, repo search는 열려 있지 않습니다.
```

Must not include:

- `업무 요약`
- `type: summary`
- `grounding:`
- `confidence:`
- `verification_required:`
- `source:`
- `safety:`
- raw `shell=false`
- raw `production_certified=false`
- duplicated headings
- empty sections

### Repository status request

`지금 ChantaCore 저장소 상태도 점검해줘` expected route: `repository_status_request`.

Expected default output:

```text
현재 v0.43에서는 ChantaCore가 저장소 파일을 직접 읽거나 git 상태를 확인하지 않습니다.
저장소 상태 점검은 v0.44 Controlled Workspace Read에서 read-only 범위로 설계할 예정입니다.

지금 가능한 점검:
* 현재 세션 상태
* provider 상태
* trace/run-report
* local note/evidence
* pilot readiness
```

Must not:

- claim repository inspection
- call shell
- call git
- search repo
- suggest it already checked files
- wrap as summary artifact

### Explicit artifact command

`/summary`, `/memo`, `/decision`, `/handoff` may use structured artifact rendering.

Allowed:

- artifact title, concise headings, bullets
- fact/assumption/unknown separation when useful
- evidence references when explicitly grounded

Hidden by default:

- raw grounding metadata
- raw source metadata
- raw safety footer
- raw run/session/debug fields

### Debug/report commands

Debug/report/trace commands may show metadata.

Allowed only in debug/report/trace:

- grounding
- confidence
- verification_required
- source summary
- provider mode
- run_id/session_id
- response_parse_status
- safety flags
- trace ids

## 9. Renderer Architecture Recommendation

| renderer | input type | output style | metadata visibility | safety visibility | when used | when not used |
|---|---|---|---|---|---|---|
| MinimalConversationRenderer | identity/capability/general plain answer | 1-5 short lines, no template envelope | hidden | brief closed-capability sentence only when relevant | plain text, identity, simple capability | explicit artifact/report/debug |
| ArtifactRenderer | V043BusinessArtifact or business flow output | structured business artifact | hidden by default | hidden by default | `/summary`, `/memo`, `/decision`, `/handoff`, `/artifact last` | plain identity/status/general chat |
| GroundedArtifactRenderer | grounded synthesis result with evidence pack | structured artifact with human-readable citations | evidence ids visible only because user requested grounded output | hidden by default | `/grounded-summary`, `/grounded-decision` | non-grounded plain chat |
| DiagnosticRenderer | run report, pilot report, grounding check, what-happened | diagnostic sections and counts | visible as user-requested diagnostics | visible as summarized status | `/what-happened`, `/grounding-check`, `/pilot report` | plain conversation |
| DebugRenderer | raw-ish debug/result objects | key-value metadata, bounded | visible | structured safety summary visible | `--debug`, `/artifact last --debug`, `/run-report`, `/trace` | default answers |
| ErrorRenderer | unavailable/denied/failed operations | short explanation + next available actions | hidden unless debug requested | may mention closed capability briefly | repo status unavailable, no evidence, provider empty response | successful artifact/default answer |
| StatusRenderer | runtime/provider/session/pilot status | compact status card | limited, user-facing | high-risk capabilities summarized | `/status`, provider status, `/v044 readiness` | artifact content |

Recommendation:

- `rendered_text` should be projection output, not the whole internal object.
- Artifact envelope should keep PI evidence, but default renderer should not print every field.
- Safety should be a policy object and report/debug surface, not a raw footer on every answer.

## 10. Metadata Disclosure Policy

| metadata | default plain chat | explicit artifact | grounded artifact | debug/report/trace |
|---|---|---|---|---|
| grounding | hidden | hidden by default | may be summarized as "근거 기반/추정" only if useful | visible |
| confidence | hidden | hidden by default | hidden or summarized, not raw key-value | visible |
| verification_required | hidden | hidden by default unless artifact needs "확인 필요" | visible as human-readable unsupported/unknown | visible |
| source | hidden | hidden by default | evidence ids/source labels visible if requested | visible |
| provider | hidden unless status requested | hidden | hidden | visible |
| run_id | hidden by default | hidden by default | hidden by default | visible |
| session_id | hidden by default | hidden by default | hidden by default | visible |
| response_parse_status | hidden | hidden | hidden | visible |
| safety flags | hidden; brief boundary sentence only when relevant | hidden | hidden | visible as structured summary |
| production_certified | never raw in normal chat | hidden | hidden | visible as `false` in safety/debug |
| evidence ids | hidden unless user asked evidence/grounded | hidden | visible because grounded output requires citations | visible |
| trace ids | hidden | hidden | hidden | visible |

Non-negotiable rule:

- No normal chat answer should contain raw key-value spam such as `grounding: ...`, `source: ...`, `safety: shell=false...`.
- Evidence and safety details must remain stored for PI review, but stored is not the same as rendered.

## 11. Golden Transcript Requirements

### 1. `넌 누구야`

- expected route: `identity_question`
- expected renderer: MinimalConversationRenderer
- expected output:

```text
저는 ChantaCore default-personal runtime에서 동작하는 업무 보조 에이전트입니다.
대화 기반 업무 정리, 요약, TODO 추출, 의사결정 정리, 인수인계문 작성, 로컬 노트/근거 조회를 도와드릴 수 있습니다.
현재는 저장소 직접 읽기, 파일 수정, 셸 실행, repo search는 열려 있지 않습니다.
```

- forbidden output strings:
  - `업무 요약`
  - `type: summary`
  - `grounding:`
  - `confidence:`
  - `verification_required:`
  - `source:`
  - `safety:`
  - `shell=false`
  - `production_certified=false`
  - `## 배경 / 맥락`
  - `알 수 없음`
  - duplicate `## 핵심 요약`

### 2. `무엇을 할 수 있어?`

- expected route: `capability_question`
- expected renderer: MinimalConversationRenderer or StatusRenderer
- expected output:

```text
대화 기반 업무 정리, 요약, TODO 추출, 메모, 의사결정 정리, 인수인계문 작성, 로컬 노트/근거 조회, grounded summary, pilot/readiness 점검을 도와드릴 수 있습니다.
저장소 직접 읽기, repo search, 셸 실행, 파일 수정, subagent 실행은 아직 열려 있지 않습니다.
```

- forbidden output strings: same as plain/default forbidden strings.

### 3. `지금 너의 상태를 체크해봐. 저장소 기준.`

- expected route: `repository_status_request` if "저장소 기준" dominates; otherwise `runtime_status_question` plus repository boundary note
- expected renderer: StatusRenderer
- expected output:

```text
현재 세션/런타임 상태는 work-session 표면에서 확인할 수 있지만, v0.43에서는 저장소 파일이나 git 상태를 직접 읽지 않습니다.
저장소 기준 점검은 v0.44 Controlled Workspace Read에서 read-only 범위로 설계해야 합니다.
지금은 provider 상태, trace/run-report, local note/evidence, pilot readiness를 확인할 수 있습니다.
```

- forbidden output strings: `업무 요약`, `type: summary`, `git status checked`, `저장소를 확인했습니다`, raw metadata.

### 4. `지금 ChantaCore 저장소 상태도 점검해줘`

- expected route: `repository_status_request`
- expected renderer: ErrorRenderer or StatusRenderer
- expected output:

```text
현재 v0.43에서는 ChantaCore가 저장소 파일을 직접 읽거나 git 상태를 확인하지 않습니다.
저장소 상태 점검은 v0.44 Controlled Workspace Read에서 read-only 범위로 설계할 예정입니다.

지금 가능한 점검:
* 현재 세션 상태
* provider 상태
* trace/run-report
* local note/evidence
* pilot readiness
```

- forbidden output strings: `업무 요약`, `type: summary`, `grounding:`, `source:`, `safety:`, `shell=false`, `git 상태를 확인했습니다`.

### 5. `/summary 오늘 v0.43.7 UX repair를 테스트하고 있어`

- expected route: `explicit_artifact_command`
- expected renderer: ArtifactRenderer
- expected output:

```text
업무 요약

## 핵심 요약
오늘 v0.43.7 UX repair를 테스트하고 있으며, 핵심 목적은 일반 대화가 summary artifact로 감기는 문제를 확인하는 것입니다.

## 다음 액션
* identity/status/repository-status 입력이 minimal renderer로 가는지 확인합니다.
* `/artifact last`, `/what-happened`, `/v044 readiness`에서 metadata 표면이 분리되는지 확인합니다.
```

- forbidden output strings:
  - `type: summary`
  - `grounding:`
  - `confidence:`
  - `verification_required:`
  - `source:`
  - `safety:`
  - duplicate `## 핵심 요약`
  - empty `## 배경 / 맥락\n알 수 없음`

### 6. `/artifact last`

- expected route: `explicit_artifact_command`
- expected renderer: ArtifactRenderer
- expected output:

```text
업무 요약

## 핵심 요약
최근 명시적으로 생성한 업무 산출물을 보여줍니다.
```

- forbidden output strings by default: raw `type:`, `grounding:`, `source:`, `safety:`.
- debug variant: `/artifact last --debug` may show metadata.

### 7. `/what-happened`

- expected route: `debug_or_report_command`
- expected renderer: DiagnosticRenderer
- expected output:

```text
최근 세션에서 실행된 명령과 생성된 산출물, provider 호출 여부, trace/run-report 상태를 요약합니다.
세부 run/session/trace 정보는 이 명령에서는 표시될 수 있습니다.
```

- forbidden output strings: none of the default-forbidden strings are globally forbidden here, because this is a diagnostic surface. But output must be structured and bounded, not accidental artifact wrapper.

### 8. `/v044 readiness`

- expected route: `pilot_command`
- expected renderer: StatusRenderer or DiagnosticRenderer
- expected output:

```text
v0.44는 Controlled Workspace Read Design & Scope Contract부터 시작할 수 있습니다.
단, v0.43.7 UX repair가 통과해야 합니다.
v0.43.7에서는 workspace read, repo search, shell, edit/apply, subagent, production certification이 열리지 않습니다.
```

- forbidden output strings: claim that workspace read is already opened, claim that edit/shell/test may start immediately.

## 12. Tests Needed for v0.43.7

Required tests:

- intent classification:
  - `넌 누구야` -> `identity_question`
  - `무엇을 할 수 있어?` -> `capability_question`
  - `지금 너의 상태를 체크해봐` -> `runtime_status_question`
  - `저장소 상태 점검해줘`, `git 상태 봐줘` -> `repository_status_request`
  - `/summary ...` -> `explicit_artifact_command`
- identity question minimal answer:
  - no `업무 요약`
  - no `type: summary`
  - no `grounding:`, `source:`, `safety:`
  - max 5 lines
- repository status minimal boundary answer:
  - says repo inspection is not available in v0.43
  - mentions v0.44 Controlled Workspace Read
  - does not claim inspection
  - does not suggest shell/git execution by default
- plain text does not route to summary artifact:
  - `execute_work_session_input("넌 누구야")` does not call summary flow
  - `provider_invoked=False` if deterministic identity answer is intended
- explicit `/summary` still routes to artifact:
  - artifact structure allowed
  - raw metadata hidden by default
- duplicate heading suppression:
  - `## 핵심 요약\n## 핵심 요약` becomes one heading
- unknown section suppression:
  - `## 배경 / 맥락\n알 수 없음` is removed in default rendering
- safety footer hidden by default:
  - default artifact and default conversation contain no raw `safety: shell=false`
- debug metadata available only in debug/report:
  - `/artifact last --debug` or DebugRenderer includes structured metadata
  - default renderer does not
- v0.44 gate blocked until UX repair passes:
  - if identity output or repository output is dirty, `ready_for_v044_design=False`
- high-risk capabilities remain closed:
  - workspace read, repo search, shell, edit/apply, provider tool/function calling, subagent, memory mutation, CORE_MEMORY write all false

## 13. Implementation Hints for Codex

Do not implement in this analysis document. Suggested future implementation strategy:

Likely modules:

- `src/chanta_core/personal_runtime/default_personal_conversation_router.py`
- `src/chanta_core/personal_runtime/default_personal_business_ux.py`
- `src/chanta_core/personal_runtime/default_personal_work_session.py`
- `src/chanta_core/personal_runtime/default_personal_work_artifacts.py`
- `src/chanta_core/personal_runtime/default_personal_chat_shell.py`
- `src/chanta_core/cli/main.py`

Minimal change strategy:

1. Add router before artifact dispatch.
   - Run slash command parser first.
   - If unknown plain text, classify intent.
   - Only explicit artifact command or explicit summary phrase goes to artifact flow.

2. Split renderers.
   - Do not use `_render_artifact` raw output directly as default display.
   - Keep internal envelope and PI records unchanged.
   - Add projection renderer that hides raw metadata.

3. Add minimal rendering policy.
   - identity/capability/status/repository-boundary answers should be deterministic and concise.

4. Filter metadata in default output.
   - remove `type:`
   - remove `grounding:`
   - remove `confidence:`
   - remove `verification_required:`
   - remove `source:`
   - remove raw `safety:`

5. Keep debug/report paths intact.
   - `/what-happened`, `/report`, `/trace`, `/artifact last --debug`, `/grounding-check`, `/evidence used` may show metadata.

6. Add golden transcript tests.
   - Tests should assert route, renderer, forbidden strings, and high-risk capability flags.

7. Preserve closed capabilities.
   - Do not add file read, repo search, git status, shell, edit/apply, provider tool/function calling, subagent, memory mutation.

## 14. Non-Goals

v0.43.7 must not implement:

- workspace read
- repository search
- arbitrary file read
- shell
- git status execution
- file edit/apply
- provider tool calling
- function calling
- subagent
- memory mutation
- CORE_MEMORY write
- production certification

Also not a goal:

- copying OpenCode's tool system
- adding OpenCode-like TUI/server architecture
- opening permission prompts for shell/edit/read
- implementing autonomous coding loop
- adding broad directory scan or hidden indexing

## 15. v0.44 Gate Recommendation

Recommendation: do not proceed to v0.44 before this UX repair passes.

Confirmed basis:

- v0.43.1 artifact renderer can expose raw `type`, `grounding`, `source`, and `safety` lines.
- v0.42.9 already required clean default output and debug-only metadata, so the observed v0.43 behavior violates an existing UX principle.
- OpenCode reference structure supports the separation of stored runtime state from user-facing rendering.

Interpretation:

- v0.44 Controlled Workspace Read will introduce more evidence, paths, read disclosures, denials, and trace events.
- If ChantaCore cannot already keep artifact/debug metadata out of normal answers, adding workspace read will likely make normal chat more confusing and higher-risk.

Withdrawal condition:

- If golden transcript tests prove identity/status/repository outputs are clean, artifact commands remain useful, debug metadata is available only through explicit surfaces, and high-risk capabilities remain closed, then this block can be lifted.

Validity:

- This recommendation applies to the v0.43.7 pre-v0.44 gate state represented by the current repository and user-observed bad outputs.

## 16. Copy-Paste Prompt Seed for GPT Mode Vera

Use this seed to generate a stronger v0.43.7 implementation prompt:

```text
Implement ChantaCore v0.43.7 as a UX repair patch before v0.44.

OpenCode reference lesson:
Do not copy OpenCode's coding-agent capabilities. Copy the interaction contract: runtime state, message parts, events, tool/permission/status/debug details are stored internally and rendered through separate surfaces. Normal chat shows assistant text, not internal objects.

ChantaCore problem:
Plain conversation is currently leaking into business artifact rendering. Identity questions such as "넌 누구야" are wrapped as "업무 요약 / type: summary". Grounding/source/safety metadata leaks into default output. Duplicate headings and empty "알 수 없음" sections appear. Repository status requests are not answered as capability-boundary responses.

Required router:
identity_question, capability_question, runtime_status_question, repository_status_request, general_chat, explicit_artifact_command, evidence_command, grounded_command, pilot_command, debug_or_report_command, unknown.

Required renderer separation:
MinimalConversationRenderer for plain chat and identity/capability/status answers.
ArtifactRenderer only for explicit /summary, /todo, /memo, /decision, /handoff, /artifact last.
GroundedArtifactRenderer only for explicit grounded commands.
DiagnosticRenderer for /what-happened, /pilot report, /grounding-check, /v044 readiness.
DebugRenderer only for --debug or explicit debug/report/trace surfaces.
ErrorRenderer for unavailable capabilities such as repo status in v0.43.

Golden transcript acceptance:
1. "넌 누구야" -> concise ChantaCore default-personal identity. No 업무 요약, type: summary, grounding/source/safety metadata, duplicate headings, empty sections.
2. "무엇을 할 수 있어?" -> concise capability answer with closed capabilities briefly listed.
3. "지금 너의 상태를 체크해봐. 저장소 기준." -> status/repository boundary answer, no repo inspection claim.
4. "지금 ChantaCore 저장소 상태도 점검해줘" -> says v0.43 cannot inspect repo/git; v0.44 Controlled Workspace Read will design read-only scope; lists current status surfaces.
5. "/summary ..." -> explicit artifact renderer allowed, but raw metadata hidden by default.
6. "/artifact last" -> clean artifact projection.
7. "/what-happened" -> diagnostic metadata allowed because explicit.
8. "/v044 readiness" -> says v0.44 is blocked until UX repair passes; workspace read remains closed in v0.43.7.

Closed capabilities:
No workspace read, arbitrary file read, repo search, shell, git status execution, file edit/apply, provider tool calling, function calling, subagent, memory mutation, CORE_MEMORY write, or production certification.

v0.44 gate:
Do not proceed to v0.44 until the golden transcripts pass and default conversation output is clean.
```


# ChantaCore Default Agent REPL Findings for external planning assistant

Date: 2026-05-08

Audience: external planning assistant / ChantaCore architecture planning

Status: Design handoff note. This document is not canonical runtime state. It is a human-readable design memo derived from local code inspection and live CLI checks. Canonical runtime state remains OCEL.

## Purpose

This note records what was observed while testing the current ChantaCore Default Agent through `chanta-cli repl`, why the interaction looked silent or under-capable, and what should be reflected in later design.

The central issue is that the current Default Agent can start an interactive session and record process/session events, but it is not yet an active workspace agent. It is currently closer to a trace-aware local LLM chat path than to a tool-using Soul/agent capable of reading files, invoking runtime skills, or inspecting repository state on demand.

## Confirmed Facts

### CLI entrypoint

The command below starts the interactive loop:

```powershell
.\.venv\Scripts\chanta-cli.exe repl
```

The command below sends a single prompt:

```powershell
.\.venv\Scripts\chanta-cli.exe ask "??萸??????덉뼱?"
```

The CLI has three commands:

- `ask`
- `repl`
- `show-config`

### Previous configuration issue

`ask` and `repl` initially failed with:

```text
ValueError: Model is not configured for provider: lm_studio
```

The cause was that `show-config` loaded app settings, but `run_ask()` and `run_repl()` did not explicitly call `load_app_settings()` before constructing `AgentRuntime()` / `ChatService()`.

This was fixed in:

- `src/chanta_core/cli/main.py`

Current behavior:

- `run_ask()` calls `load_app_settings()`.
- `run_repl()` calls `load_app_settings()`.

### Default Agent execution path

The current REPL path is:

```text
chanta-cli repl
  -> ChatService.chat()
  -> AgentRuntime.run()
  -> ProcessRunLoop.run()
  -> skill:llm_chat
  -> execute_llm_chat_skill()
  -> LLMClient.chat_messages()
```

The default selected skill is `skill:llm_chat` unless an explicit skill is provided or a future decision service path selects another skill.

Confirmed in:

- `src/chanta_core/runtime/chat_service.py`
- `src/chanta_core/runtime/agent_runtime.py`
- `src/chanta_core/runtime/loop/process_run_loop.py`
- `src/chanta_core/skills/builtin/llm_chat.py`
- `src/chanta_core/skills/executor.py`

### Current Default Agent does not have direct workspace tools

In the current default chat path, the agent does not have direct access to:

- filesystem reads
- shell execution
- network calls
- MCP connections
- plugin loading
- runtime tool dispatch
- direct AgentRuntime capability mutation

Therefore, a prompt such as:

```text
<PERSONAL_DIRECTORY>/source/sample_profile.md 諛묒뿉 ?덈뒗 markdown ?뚯씪???쎌뼱遊먮킄
```

cannot be performed by the Default Agent through the current REPL path. The correct behavior is not to claim that it read the files. It should state the limitation plainly.

This limitation does not mean ChantaCore cannot support bounded workspace reads. Later versions add explicit, root-constrained read-only workspace skills; the default natural-language chat path still must not imply ambient filesystem access.

### REPL is not yet full conversational memory injection

The runtime records sessions, turns, user messages, assistant messages, and process events into OCEL/session structures.

However, the current LLM prompt assembly path does not automatically inject previous conversation turns into the next LLM prompt in ordinary REPL use.

Operationally, this means the REPL is currently closer to:

```text
same session id + repeated single-turn LLM calls + OCEL recording
```

than to:

```text
full multi-turn conversational agent with automatically assembled dialogue history
```

This should be treated as a design gap, not as a user mistake.

### Empty responses were caused by model output shape and token budget

During live testing, LM Studio returned empty assistant `content` for some prompts.

Observed raw response shape:

```text
finish_reason = length
content = ''
reasoning_tokens ~= 377
max_tokens = 384
```

Interpretation:

The configured reasoning model used nearly all completion budget on reasoning tokens and reached the length limit before emitting final assistant content.

This is a stronger explanation than ?쐔he agent chose not to answer,??because the OpenAI-compatible response showed an empty `message.content` with `finish_reason=length`.

The immediate mitigation was to increase the Default Agent `max_tokens` from `384` to `1024`.

Updated in:

- `src/chanta_core/agents/default_agent.py`

### Empty model output is now surfaced

The CLI now formats empty assistant output as:

```text
[empty model response: the configured LLM returned no assistant content]
```

This avoids the misleading experience of:

```text
assistant>
```

with no explanation.

Updated in:

- `src/chanta_core/cli/main.py`

Covered by:

- `tests/test_cli_default_agent_chat_boundaries.py`

## Current Practical Capability Level

The current Default Agent can:

- call the configured local LLM provider;
- answer based on the immediate prompt and assembled OCEL/PIG context;
- record user and assistant messages;
- record process run loop events;
- record skill selection/execution events;
- record LLM call/response events;
- inspect recent OCEL only if routed through the appropriate builtin skill path;
- provide a trace-aware local chat surface.

The current Default Agent cannot yet:

- read arbitrary repository files on request;
- inspect Personal Directory roots through ambient filesystem access;
- call shell commands;
- execute tools;
- load plugins;
- connect to MCP;
- perform active runtime registry updates;
- carry full conversational history into every turn by default;
- behave like Codex-like assistant with workspace tool access.

## Design Implications

### 1. Separate identity from capability

The Default Agent should not claim to be a fully active ChantaCore Soul unless its capability path actually supports active work.

Recommended wording principle:

```text
I am the ChantaCore Default Agent in the current local runtime path.
I can answer through the configured LLM and recorded context.
I cannot directly read files or run tools unless an explicit ChantaCore skill provides that operation.
```

This avoids false capability claims and keeps the architecture aligned with the anti-Chanta principle: do not affirm capability without evidence.

### 2. Add explicit capability introspection

The runtime needs a first-class way for the agent to answer:

```text
What can I currently do?
```

This should not be guessed by the LLM. It should be derived from registered runtime capabilities, active skills, permission gates, and execution policies.

Possible future object/view:

- `runtime_capability_snapshot`
- `agent_capability_profile`
- `active_skill_inventory`
- `permission_gated_capability_view`

The answer should distinguish:

- available now;
- available only as metadata/imported descriptor;
- disabled candidate;
- requires review;
- requires permission;
- not implemented.

### 3. Add session history assembly for REPL

The REPL should eventually include recent conversation turns in prompt assembly through a bounded context policy.

Suggested design:

- Use OCEL/session message records as source of truth.
- Build a bounded `SessionContextPolicy`.
- Include recent user/assistant turns as context blocks.
- Keep canonical persistence in OCEL/session objects.
- Do not make terminal scrollback canonical.

This would make follow-up prompts such as ?쒕갑湲?留먰븳 寃??ㅼ떆 ?ㅻ챸?대킄??behave more naturally.

### 4. Add workspace read as an explicit reviewed skill, not ambient power

If Default Agent is expected to read project files, that should be introduced as an explicit skill with boundaries.

Possible skill family:

- `skill:list_workspace_files`
- `skill:read_workspace_text_file`
- `skill:summarize_workspace_markdown`

Required boundaries:

- workspace-root constrained paths;
- path traversal defense;
- file size limits;
- binary file rejection;
- OCEL event recording;
- permission/sandbox relation if needed;
- no hidden shell fallback;
- no network fallback.

The Default Agent should not gain ambient filesystem access simply because it is conversational.

### 5. Add clear refusal/limitation behavior

When a requested operation is unavailable, the agent should say:

- what it cannot do;
- why, in runtime terms;
- what input would allow it to proceed safely;
- which future capability would be needed.

Example:

```text
I cannot read that directory through the current Default Agent chat path.
If you paste the file contents, I can analyze them.
If a future workspace-read skill is enabled, I should use that skill and record the read as an OCEL event.
```

### 6. Avoid using reasoning content as user-visible fallback

Some local reasoning models expose `reasoning_content` in the OpenAI-compatible response.

The runtime should not blindly show that field as assistant output. It may contain internal reasoning traces. A safer behavior is:

- increase output budget;
- detect empty final content;
- surface an operational diagnostic;
- optionally retry with a stronger ?쐄inal answer only??prompt or lower reasoning settings if the provider supports it;
- never expose hidden reasoning as a substitute for final answer.

### 7. Provider/model profile should be explicit

The current issue was partly caused by a reasoning-heavy local model with a low completion budget.

Future settings should distinguish:

- chat model profile;
- reasoning model profile;
- max completion tokens;
- whether provider returns reasoning tokens;
- whether the runtime should retry empty content;
- whether a model is suitable for terse REPL interaction.

Possible setting names:

- `CHANTA_LLM_MAX_TOKENS`
- `CHANTA_LLM_CHAT_MAX_TOKENS`
- `CHANTA_LLM_EMPTY_RESPONSE_RETRY`
- `CHANTA_LLM_REASONING_MODE`

### 8. OCEL trace inspection should be explicit about scope

The response:

```text
OCEL recent inspection: 2385 events, 1045 objects, ...
```

is useful, but the agent should clarify whether it inspected:

- recent global store;
- current session;
- current process instance;
- last N events;
- persisted OCEL store on disk.

Without that, users may infer that the agent has fully reconstructed ?쐔he conversation,??when it may only have run a coarse recent inspection.

### 9. Default Agent should be honest about relation to Personal Directories

At this stage, the Default Agent is not yet equivalent to a ChantaCore Soul with active agency.

It is better described as:

```text
a trace-aware local LLM runtime endpoint with OCEL persistence
```

than:

```text
an autonomous Soul capable of active workspace operation
```

To become Soul-like, it needs at least:

- stable identity/persona loading;
- bounded memory/session history;
- explicit capability inventory;
- permission-gated tool use;
- workspace read/write skills;
- review/sandbox integration;
- self-reporting of capability limits;
- OCEL-native action provenance.

## Changes Already Made After This Finding

### `src/chanta_core/cli/main.py`

Added:

- settings loading in `run_ask()`;
- settings loading in `run_repl()`;
- empty response diagnostic formatting.

### `src/chanta_core/agents/default_agent.py`

Updated:

- Default Agent system prompt now states current chat-path limitations.
- Default Agent is instructed to provide non-empty responses.
- Default `max_tokens` increased from `384` to `1024`.

### `tests/test_cli_default_agent_chat_boundaries.py`

Added tests for:

- Default Agent prompt boundary statements;
- CLI empty response formatting.

## Verification Performed

Targeted tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_cli_default_agent_chat_boundaries.py tests\test_process_run_loop_skill_dispatch.py tests\test_skill_executor.py
```

Observed result:

```text
5 passed
```

Live CLI check:

```powershell
.\.venv\Scripts\chanta-cli.exe ask "??萸??????덉뼱?"
```

Observed behavior after fix:

- The agent gives a non-empty answer.
- The agent describes itself as ChantaCore.
- The agent states that direct filesystem, shell, network, MCP, and plugin access are not available unless explicit ChantaCore skills provide them.

Live CLI check:

```powershell
.\.venv\Scripts\chanta-cli.exe ask "<PERSONAL_DIRECTORY>/source/sample_profile.md 諛묒뿉 ?덈뒗 markdown ?뚯씪???쎌뼱遊먮킄"
```

Observed behavior after fix:

- The agent does not claim to read files.
- The agent states it cannot directly access the filesystem through the current path.
- The agent asks for pasted content or an explicit capability path.

## Evidence Strength

Evidence strength is high for the current local repository state because it is based on:

- direct code inspection;
- direct CLI execution;
- direct LM Studio response inspection;
- targeted tests passing.

Evidence strength is limited for other machines, providers, or future versions because:

- local model behavior can vary;
- LM Studio model settings can change;
- future ChantaCore skills may add tool access;
- future context assembly may include session history.

## Withdrawal Conditions

The claims in this document should be revised or withdrawn if any of the following becomes true:

- `chanta-cli repl` starts routing file-read requests through an explicit workspace skill.
- `ProcessContextAssembler` begins injecting bounded session history by default.
- `SkillRegistry` gains active workspace read/tool dispatch skills and the decision service routes to them.
- Default Agent gains permission-gated filesystem or shell access.
- The configured LLM provider no longer emits empty final content under the tested prompts and token settings.
- A future Soul runtime layer supersedes the current Default Agent chat path.

## Validity Window

This note is valid for the observed local state on 2026-05-08 after the v0.14.3 implementation work and the small REPL behavior patch described above.

It should be rechecked before using it as a basis for v0.15+ design decisions.

## Final Conclusion

The current ChantaCore Default Agent REPL is functional as an OCEL-recorded local LLM chat surface, but it is not yet a capable active agent or Soul. Future design should add explicit capability introspection, bounded session history, and permission-gated workspace skills rather than letting the Default Agent imply unavailable powers.


# ChantaCore v0.14.3a - Default Agent Capability Contract

Date: 2026-05-08

Status: Boundary and UX hardening patch between v0.14.3 and v0.14.4.

This document is a human-readable restore/design note. It is not canonical runtime state. ChantaCore canonical runtime/process state remains OCEL-based.

## Purpose

v0.14.3a adds an explicit capability contract for the ChantaCore Default Agent.

The Default Agent REPL is currently an OCEL-recorded local LLM chat endpoint. It is not yet an active Soul, not yet a workspace agent, and not yet a tool-using autonomous runtime actor.

The patch prevents the Default Agent from implying unavailable powers when the user asks questions such as:

```text
What can you do?
```

or:

```text
/Souls/sample_personal_directory 諛묒뿉 ?덈뒗 markdown ?뚯씪???쎌뼱遊먮킄
```

## Confirmed Current Runtime Path

The current default interactive path is:

```text
chanta-cli repl
  -> ChatService
  -> AgentRuntime
  -> ProcessRunLoop
  -> skill:llm_chat
  -> LLMClient
```

The default path can record OCEL/session/process events and call the configured local LLM provider.

It does not directly:

- read arbitrary repository files;
- inspect `/Souls` directories;
- execute shell commands;
- call network resources;
- connect MCP;
- dynamically load plugins;
- mutate `ToolDispatcher`;
- mutate `SkillExecutor`;
- register active runtime tools;
- auto-grant permissions;
- inject full bounded REPL session history into every turn.

## Added Runtime Capability Read Model

Added:

- `RuntimeCapabilitySnapshot`
- `AgentCapabilityProfile`
- `RuntimeCapabilityIntrospectionService`

Location:

- `src/chanta_core/runtime/capability_contract.py`

These are generated runtime read-models for capability self-reporting. They do not add execution powers and do not create a canonical JSONL capability store.

## Capability Categories

The service generates the following categories.

### available_now

Current Default Agent chat-path capabilities:

- configured local LLM chat;
- immediate-prompt response;
- OCEL/session/process event recording;
- `skill:llm_chat`;
- trace-aware local chat surface;
- explicit limitation/refusal behavior.

### metadata_only

Current metadata/read-model surfaces:

- tool registry views;
- tool policy views;
- external capability descriptors;
- external assimilation candidates;
- PIG/OCPX reports when present as read-models.

### disabled_candidates

External capabilities remain disabled:

- external assimilation candidates with `execution_enabled=False`.

### requires_review

These require later explicit review workflows:

- imported external capabilities;
- MCP/plugin descriptors;
- future workspace read skills.

### requires_permission

These require explicit permission/safety layers before use:

- workspace file read;
- workspace file write;
- shell execution;
- network access;
- tool dispatch.

### not_implemented

These are not implemented in the Default Agent chat path:

- arbitrary repository file read;
- `/Souls` directory inspection;
- shell execution;
- network calls;
- MCP connection;
- plugin loading;
- active runtime registry updates;
- full bounded REPL session history injection;
- autonomous Soul behavior.

## Default Agent Prompt Contract

`load_default_agent_profile()` now includes a generated capability profile block in the system prompt.

The prompt tells the model:

- what the Default Agent currently is;
- what it can do now;
- what is metadata-only;
- what is disabled;
- what requires review;
- what requires permission;
- what is not implemented;
- that "what can you do?" must be answered from the capability contract.

This reduces unsupported claims and gives the LLM a concrete runtime-derived basis for self-reporting.

## Soul Boundary

The Default Agent is not yet an active Soul.

The correct current description is:

```text
trace-aware local LLM chat endpoint with OCEL persistence
```

not:

```text
active workspace Soul with autonomous tool use
```

To become Soul-like, later versions need explicit reviewed capabilities such as:

- bounded session history assembly;
- workspace read skills;
- workspace write skills;
- permission gates;
- sandbox/conformance integration;
- runtime capability inventory;
- tool dispatch policies;
- OCEL-native action provenance.

## OCEL/PIG Inspection Scope Labeling

The builtin `inspect_ocel_recent` skill now labels its output scope.

Output text includes:

```text
inspection_scope=recent_global
persistence_scope=persisted_store
```

Output attrs include:

- `inspection_scope`
- `persistence_scope`
- `current_session_scope_enabled`
- `current_process_instance_scope_enabled`

This avoids implying that a recent inspection is necessarily scoped to the current conversation or current process instance.

## Deliberately Not Implemented

v0.14.3a does not add:

- filesystem read skill;
- shell execution;
- network calls;
- MCP connection;
- plugin loading;
- ToolDispatcher mutation;
- SkillExecutor mutation;
- AgentRuntime active gate;
- permission grants;
- external candidate activation;
- full session history injection;
- reasoning-content exposure as assistant output;
- terminal scrollback canonicalization;
- canonical JSONL capability store.

## Tests

Added or extended:

- `tests/test_runtime_capability_introspection.py`
- `tests/test_default_agent_capability_profile.py`
- `tests/test_default_agent_capability_boundaries.py`
- `tests/test_cli_default_agent_chat_boundaries.py`
- `tests/test_process_intelligence_skills.py`
- `tests/test_skill_tool_integration.py`

Key assertions:

- required capability categories are generated;
- unsafe/unimplemented capabilities are not in `available_now`;
- Default Agent prompt includes the generated capability contract;
- Default Agent prompt states it is not yet an active Soul;
- empty model response diagnostic remains intact;
- OCEL recent inspection labels scope;
- no workspace read/shell/network/MCP/plugin execution path was added.

## Future Work

Future versions should add capabilities only as explicit, reviewed, OCEL-recorded runtime features.

Likely next design steps:

- session history assembly through a bounded `SessionContextPolicy`;
- workspace file read as an explicit reviewed skill;
- capability inventory derived from active `SkillRegistry` and permission policy;
- OCEL object/event support for capability snapshots if the read-model becomes persistent;
- later Soul activation only after safety/conformance layers exist.

## Restore Summary

v0.14.3a hardens the Default Agent's self-description.

It makes capability self-reporting runtime-derived, explicit, and bounded. It does not add new active powers.


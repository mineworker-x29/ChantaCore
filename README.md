# ChantaCore

`src/chanta_core/` includes a minimal CLI for OpenAI-compatible model endpoints such as LM Studio.

## Setup

1. Create `.env` from `.env.example`.
2. In LM Studio, start the local server and load `qwen3.6-35b-a3b:2`.
3. Install the package:

```bash
pip install -e .
```

## Usage

One-shot prompt:

```bash
chanta-cli ask "한국어로 자기소개를 해줘."
```

Pipe stdin:

```bash
echo "현재 설정을 요약해줘." | chanta-cli ask
```

Interactive session:

```bash
chanta-cli repl --system "답변은 간결하게 해."
```

Inspect resolved config:

```bash
chanta-cli show-config
```

`python -m chanta_core ...` also works.

## OCEL / OCPX / PIG Foundation

ChantaCore v0.3 adds an OCEL-oriented canonical trace layer for process
intelligence. Runtime events are persisted as object-centric event, object, and
relation records in a SQLite store at `data/ocel/chanta_core_ocel.sqlite`.

The existing JSONL event log remains only as an optional raw/debug mirror.
Canonical persistence for runtime traces is now the SQLite OCEL store.

User requests are first-class OCEL objects. The runtime trace path records
sessions, agents, user requests, prompts, LLM calls, providers, models, LLM
responses, outcomes, and errors as separate objects where applicable.

`chanta_core.ocpx` is the foundation for a future object-centric process
computation engine. It is inspired by OCPA-style analysis but is intended to
evolve into a local ChantaCore computation layer that reads OCEL records and
builds process views without requiring heavy runtime dependencies.

`chanta_core.pig` is the foundation for the Process Intelligence Graph / Guide
layer. It consumes OCPX views and currently provides simple graph, guide,
diagnostic, and recommendation outputs.

pm4py and ocpa compatibility is future-facing. Compatibility should be achieved
through standards-oriented OCEL export/import boundaries, not mandatory runtime
dependencies.

### v0.3.1 OCEL relation hygiene

Event-object and object-object relations now use logical uniqueness:
`event_id + object_id + qualifier` for event-object relations, and
`source_object_id + target_object_id + qualifier` for object-object relations.
Duplicate logical relations are ignored on insert.

`OCELValidator.validate_duplicate_relations()` reports duplicate relation groups
across both standard-oriented OCEL tables and Chanta operational extension
tables. The raw mirror may still append repeated raw events because it is
debug/audit-oriented, not canonical persistence.

Worker OCEL emission is still future work.

### v0.3.2 OCEL canonical model alignment

ChantaCore v0.3.2 aligns the internal OCEL-oriented model with a smaller
canonical event/object shape. Canonical events now use `event_activity`,
`event_timestamp`, and `event_attrs`; runtime taxonomy such as
`runtime_event_type`, lifecycle, source runtime, session id, and actor id lives
inside `event_attrs`.

Canonical objects now use `object_id`, `object_type`, and `object_attrs`.
Object-specific values such as `object_key`, `display_name`, `created_at`, and
runtime state are stored in `object_attrs`.

Python relation modeling uses a unified `OCELRelation` with `relation_kind`,
`source_id`, `target_id`, `qualifier`, and `relation_attrs`. SQLite persistence
still keeps event-object and object-object relation tables separate.

Runtime activities use stable reusable labels such as `receive_user_request`,
`start_goal`, `assemble_prompt`, `call_llm`, `receive_llm_response`, and
`complete_goal`. The basic AgentRuntime path now records a lightweight `goal`
object related to the user request, session, and agent.

Timestamp creation is centralized in `chanta_core.utility.time.utc_now_iso()`
and returns timezone-aware UTC strings with a trailing `Z`.

This remains an object-centric runtime trace foundation. Full worker events,
skill runtime, process mining algorithms, and complete pm4py/ocpa compatibility
are still future work.

### v0.4 ProcessInstance & Skill Trace Ontology

ChantaCore v0.4 uses `process_instance` as the executable process/case anchor
for the basic AgentRuntime path. Mission, goal, and objective information is
stored in `process_instance.object_attrs` instead of creating separate mission
or goal objects.

The canonical runtime activity sequence is:

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

The current LLM response path is traced as selection and execution of the
built-in `skill:llm_chat` object. This is trace ontology only; a full skill
execution framework, worker runtime, task queue, and process mining algorithms
remain future work.

### v0.5 ProcessRunLoop Runtime

ChantaCore v0.5 introduces `ProcessRunLoop` as the canonical bounded runtime
loop for advancing one `process_instance`. `AgentRuntime` still receives the
user request and starts the process instance, then delegates execution to the
loop.

The v0.5 loop is synchronous and bounded to one iteration by default. It keeps
mutable `ProcessRunState`, assembles model context, invokes the configured LLM
through the runtime harness, records an observation, applies a stop policy, and
persists each major transition through the OCEL-backed trace service.

Additional loop activities include:

```text
start_process_run_loop
decide_next_activity
assemble_context
observe_result
```

`ProcessTrace`-style views are read models produced through OCPX, not the
runtime loop itself. Process variants, permission gates, tool dispatch, context
compaction, subagent delegation, and worker queues remain future work.

Claude Code's shared-loop pattern is used only as architectural inspiration for
loop state, context assembly, harness execution, observation collection, stop
conditions, and persistence. ChantaCore v0.5 does not copy or implement Claude
Code features such as streaming, shell sandboxing, MCP/plugin execution, or
subagents.

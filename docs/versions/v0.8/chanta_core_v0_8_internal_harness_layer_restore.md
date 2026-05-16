# ChantaCore v0.8.x — Internal Harness Layer Plan

## 1. Purpose

v0.8.x is the Internal Harness Layer phase of ChantaCore. It is not one feature.

v0.3.x through v0.7.x established the Core Layer:

- OCEL canonical event/object/relation persistence
- OCPX object-centric process computation/read model
- PIG process intelligence graph/context/guidance/conformance/reporting
- ProcessRunLoop
- SkillRegistry / SkillExecutor
- Internal process intelligence tool gateway
- DecisionService
- Runtime self-conformance
- PI substrate operational reports and inspector

v0.8.x adds internal agent-harness capabilities on top of that spine. The phase
now extends through v0.8.9 and includes read-only inspection, repo search,
permissions, edit proposal, approved patch application, worker queue, scheduler,
ProcessJob FSM hardening, queue conformance, and OCEL/report quality hardening.

No internal harness feature may bypass the ChantaCore spine:

```text
ProcessRunLoop
-> DecisionService
-> SkillExecutor
-> ToolDispatcher
-> OCEL
-> OCPX
-> PIG
```

Lower-level infrastructure must still emit OCEL trace records when invoked
through runtime.

## 2. Layer Distinction

| Layer | Role | Examples | Status |
| --- | --- | --- | --- |
| Core Layer | ChantaCore-specific built-in process intelligence substrate. | OCEL, OCPX, PIG, ProcessRunLoop, Skill/Tool Gateway, DecisionService, PI Reports/Inspector | Established by v0.7.x |
| Internal Harness Layer | Basic agent harness capabilities implemented inside ChantaCore and traced through the Core Layer. | Workspace/file read, repo search, permissions, edit proposal, approved patching, worker queue, scheduler, queue FSM/conformance, compatibility/report hardening | v0.8.x |
| External Layer | Demand-driven integration with outside systems. | MCP, plugin system, external connectors, external skill ingestion, external web/API integration, third-party harness adapters | Future work |

Core Layer features are not optional plugins. Internal Harness Layer features
must use them instead of bypassing them.

## 3. v0.8.x Roadmap and Status

| Version | Name | Scope | Status |
| --- | --- | --- | --- |
| v0.8.0 | Internal Harness Layer Baseline | Scope declaration, architectural guardrails, no major runtime feature. | Roadmap baseline |
| v0.8.1 | Workspace/File Read-Only Inspection | Workspace root handling, path guard, `path_exists`, `list_files`, `read_text_file`, `summarize_tree`, read-only OCEL trace. | Implemented |
| v0.8.2 | Repo Search / Symbol Scan | Text search, file finding, lightweight symbol scan, definition candidate scan, stdlib/regex first, no heavy parser dependency. | Implemented |
| v0.8.3 | Safe Tool Permission Skeleton | Deny-first tool policy, risk classes, `approval_required` state, no interactive UI, no dangerous execution. | Implemented |
| v0.8.4 | Edit Proposal, Not Direct Edit | `EditProposal`, proposed diff, rationale, risk level, evidence refs, JSONL proposal store, no workspace mutation. | Implemented |
| v0.8.5 | Patch Application with Approval | Explicit approval phrase, backup/rollback metadata, approved patch application, OCEL trace, no silent write. | Implemented |
| v0.8.6 | Worker Queue / Background Process | Process jobs, local queue, worker runner, claim/running/completed/failed lifecycle, retry count, heartbeat. | Implemented |
| v0.8.7 | Scheduler / Mission-like Recurring Process Runs | One-time and interval process schedules that enqueue `ProcessJob`; no daemon, no cron, no MissionLoop/GoalLoop. | Implemented |
| v0.8.8 | Process Job FSM & Queue Conformance | ProcessJob-specific FSM, explicit transition table, invalid transition rejection, FSM OCEL trace, advisory PIG queue conformance. | Implemented |
| v0.8.9 | OCEL Compatibility & Report Quality Hardening | ChantaCore canonical JSON export/import, SQLite export, validator readiness, PIG report/inspector quality, hygiene tests. | Implemented |

## 4. Implemented Internal Harness Tools

v0.8.x uses gateway-level tools with operation-based dispatch:

- `tool:workspace`
- `tool:repo`
- `tool:edit`
- `tool:worker`
- `tool:scheduler`

These sit alongside the Core Layer process intelligence tools:

- `tool:ocel`
- `tool:ocpx`
- `tool:pig`
- `tool:echo`

Do not replace these with many tiny duplicated tools. Operations belong inside
the gateway tool when the tool boundary is clear.

Good:

```text
tool:workspace(operation="read_text_file")
tool:repo(operation="search_text")
tool:edit(operation="apply_approved_proposal")
tool:worker(operation="check_queue_conformance")
tool:scheduler(operation="run_once")
```

Bad:

```text
tool:read_text_file
tool:search_workspace_text
tool:apply_patch_directly
tool:check_queue_conformance
```

## 5. Guardrails

- No shell execution in v0.8.x.
- No network/web fetch in v0.8.x.
- No MCP/plugin system in v0.8.x.
- No external connector layer in v0.8.x.
- No self-modification.
- No automatic policy promotion.
- No direct runtime bypass of OCEL/OCPX/PIG.
- No async daemon.
- No full production sandbox.
- No generic FSM framework.
- No formal Petri-net conformance.
- No mandatory pm4py/ocpa integration.
- No pandas, numpy, or networkx dependency.

These guardrails are part of the v0.8.x restore contract. A later version may
revise them only through an explicit roadmap update.

## 6. Tool Naming Principles

Definitions:

- Skill = semantic capability.
- Tool = internal or external execution gateway.
- Operation = concrete function inside a tool.

For internal process intelligence:

- `tool:ocel`
- `tool:ocpx`
- `tool:pig`

For internal harness:

- `tool:workspace`
- `tool:repo`
- `tool:edit`
- `tool:worker`
- `tool:scheduler`

The expected shape is:

```text
tool:<domain>(operation="<specific_function>")
```

## 7. OCEL/OCPX/PIG Trace Requirement

All internal harness operations must eventually be visible through:

- `event_activity`
- object records
- event-object relations
- object-object relations
- OCPX read models
- PIG reports / inspector output

The trace requirement applies even when an operation is read-only. Read-only
status limits mutation; it does not exempt the runtime from observability.

## 8. Read-Only and Mutation Progression

v0.8.x intentionally staged mutation:

1. v0.8.1 and v0.8.2 are strictly read-only.
2. v0.8.3 adds permission skeleton before mutation.
3. v0.8.4 creates edit proposals only.
4. v0.8.5 applies patches only after explicit approval.

Patch application is not silent automation. It requires:

- existing `EditProposal`
- valid `PatchApproval`
- explicit phrase: `I APPROVE PATCH APPLICATION`
- policy configuration that allows approved writes
- backup metadata before target mutation

## 9. Worker and Scheduler Semantics

v0.8.6 and v0.8.7 add local, synchronous harness infrastructure:

- Worker queue enqueues and runs `ProcessJob`.
- Scheduler creates schedules and enqueues due jobs.
- Scheduler does not execute `ProcessRunLoop` directly.
- WorkerRunner executes jobs later.
- No daemon, no async runtime, no cron dependency, no distributed lock.

v0.8.8 hardens `ProcessJob` lifecycle as a ProcessJob-specific FSM:

- `None -> queued`
- `queued -> claimed`
- `claimed -> running`
- `running -> completed`
- `running -> failed`
- `failed -> queued` via retry
- `queued -> cancelled`

Illegal transitions are rejected, and queue conformance is advisory under PIG.

## 10. Naming Warning

Do not introduce `MissionLoop` or `GoalLoop`.

Do not introduce a `mission` object type prematurely.

Scheduled or recurring process runs can use:

- `process_schedule`
- `scheduled_process`
- `recurring_process`

If needed, `mission_text` and `objective_text` may live in `object_attrs`.

## 11. Compatibility and Report Hardening

v0.8.9 adds hardening rather than new runtime behavior:

- ChantaCore canonical JSON export/import
- SQLite copy export
- canonical/export readiness validation
- clearer distinction between internal canonical OCEL and future full OCEL 2.0
- operator-readable PIG reports
- operator-readable PI substrate inspector
- static hygiene checks

v0.8.9 does not claim full OCEL 2.0 conformance. pm4py/ocpa compatibility remains
future-facing and optional.

## 12. Validation Strategy

Each v0.8.x sub-version should include:

- unit tests without LM Studio
- script smoke tests without LM Studio unless explicitly LLM-related
- OCEL trace checks
- PIG report/inspector visibility
- generated file hygiene checks
- guardrail tests for forbidden directories/dependencies where relevant

Validation should prove that the feature works through the ChantaCore spine, not
only as an isolated helper.

## 13. Exit Criteria for v0.8.x

By the end of v0.8.x, ChantaCore should have:

- read-only workspace/repo inspection
- safe permission skeleton
- edit proposal and approved patch application
- background worker process foundation
- scheduler/recurring process run support
- ProcessJob FSM and queue conformance
- OCEL canonical JSON export/import
- OCEL validator readiness checks
- operator-readable PIG reports and inspector
- generated artifact hygiene
- all internal harness actions traceable through OCEL/OCPX/PIG

These are exit criteria for the Internal Harness Layer phase. They do not imply
external connector support.

## 14. Remaining Limitations After v0.8.x

- external connectors still future work
- MCP/plugin system still future work
- web/network tools still future work unless separately approved
- shell execution still future work unless separately approved
- full production sandbox still future work
- full UI dashboard still future work
- full OCEL 2.0 JSON/XML conformance still future work
- pm4py/ocpa integration still future-facing and optional
- formal process discovery/conformance/performance metrics still future work

v0.8.x makes ChantaCore more operationally capable without changing its identity:
ChantaCore remains a process-intelligence-native agent runtime, not a generic
harness with process intelligence bolted on afterward.

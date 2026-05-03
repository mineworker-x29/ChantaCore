# ChantaCore v0.8.x — Internal Harness Layer Plan

## 1. Purpose

v0.8.x is not a single feature release. It defines the Internal Harness Layer phase of ChantaCore.

v0.3.x through v0.7.x established the ChantaCore Core Layer:

- OCEL canonical event/object/relation persistence
- OCPX object-centric process computation/read model
- PIG process intelligence graph/guide/context/guidance/conformance/reporting
- ProcessRunLoop
- SkillRegistry / SkillExecutor
- Internal process intelligence tool gateway
- DecisionService
- PI substrate operational reports and inspector

v0.8.x should add basic internal agent harness capabilities only on top of this spine. These capabilities must be implemented as ChantaCore-native runtime features and traced through OCEL/OCPX/PIG.

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

If a feature is lower-level infrastructure, it must still emit OCEL trace records when invoked through runtime.

## 2. Layer Distinction

| Layer | Role | Examples |
| --- | --- | --- |
| Core Layer | ChantaCore-specific built-in process intelligence substrate. This is implemented by v0.7.x. | OCEL, OCPX, PIG, ProcessRunLoop, Skill/Tool Gateway, DecisionService, PI Reports/Inspector |
| Internal Harness Layer | Basic agent harness capabilities implemented inside ChantaCore and traced through the Core Layer. This is planned for v0.8.x. | Workspace/file read, repo search, symbol scan, permission skeleton, edit proposals, patch application with approval, worker queue, scheduler / recurring process runs |
| External Layer | Demand-driven integration with outside systems. This remains future work after v0.8.x unless separately approved. | MCP, plugin system, external connectors, external skill ingestion, external web/API integration, third-party harness adapters |

Core Layer features are not optional plugins. Internal Harness Layer features must use them instead of bypassing them.

## 3. v0.8.x Roadmap

### v0.8.0 — Internal Harness Layer Baseline

- scope declaration
- architectural guardrails
- no major runtime feature

### v0.8.1 — Workspace/File Read-Only Inspection

- workspace root handling
- path_exists
- list_files
- read_text_file
- summarize_tree
- path guard
- forbidden paths guard
- read-only OCEL trace

### v0.8.2 — Repo Search / Symbol Scan

- text search
- file finding
- simple symbol scan
- definition candidate scan
- stdlib/regex first
- no heavy parser dependency yet

### v0.8.3 — Safe Tool Permission Skeleton

- deny-first tool policy
- risk classes
- approval_required state
- no interactive UI yet
- no dangerous tool execution yet

### v0.8.4 — Edit Proposal, Not Direct Edit

- edit proposal object
- proposed diff
- rationale
- risk level
- evidence refs
- no file mutation

### v0.8.5 — Patch Application with Approval

- explicit approval requirement
- backup/rollback info
- patch application
- OCEL trace
- no silent write

### v0.8.6 — Worker Queue / Background Process

- queue
- process job
- worker loop
- claim/done/failed
- retry count
- heartbeat

### v0.8.7 — Scheduler / Mission-like Recurring Process Runs

- scheduled process runs
- recurring processes
- scheduler definitions
- no premature mission object type
- mission_text/objective in attrs if needed

## 4. Guardrails

- No shell execution before permission skeleton.
- No file write before edit proposal and approval model.
- No network/web fetch in v0.8.x unless explicitly approved later.
- No MCP/plugin system in v0.8.x.
- No external connector layer in v0.8.x.
- No self-modification.
- No automatic policy promotion.
- No direct runtime bypass of OCEL/OCPX/PIG.

These guardrails are part of the v0.8.x restore contract. A later version may revise them only with an explicit roadmap update.

## 5. Tool Naming Principles

Definitions:

- Skill = semantic capability.
- Tool = internal or external execution gateway.
- Operation = concrete function inside a tool.

Current internal process intelligence tools:

- `tool:ocel`
- `tool:ocpx`
- `tool:pig`

Future internal harness tools:

- `tool:workspace`
- `tool:repo`
- `tool:edit`
- `tool:worker`
- `tool:scheduler`

Do not create many tiny tools when one tool with operations is clearer.

Good:

```text
tool:workspace(operation="read_text_file")
```

Bad:

```text
tool:read_text_file
```

Good:

```text
tool:repo(operation="search_text")
```

Bad:

```text
tool:search_workspace_text
```

## 6. OCEL/PIG Trace Requirement

All internal harness operations must eventually be traceable as:

- event_activity
- object
- event-object relation
- object-object relation
- ProcessRunReport / PIGReport visibility

The trace requirement applies even when the operation is read-only. Read-only status limits mutation; it does not exempt the runtime from observability.

## 7. Read-Only First Principle

v0.8.1 and v0.8.2 are strictly read-only.

Mutation begins only at v0.8.4 as an edit proposal. Actual mutation begins only at v0.8.5, and only with approval.

This sequence is intentional:

1. Observe workspace and repository state.
2. Propose a bounded change.
3. Require approval before applying a patch.
4. Trace the action through OCEL/OCPX/PIG.

## 8. Naming Warning

Do not introduce `MissionLoop` or `GoalLoop`.

Do not introduce a `mission` object type prematurely.

Scheduled or recurring process runs can use:

- `process_schedule`
- `scheduled_process`
- `recurring_process`

If needed, `mission_text` and `objective_text` may live in `object_attrs`.

## 9. Validation Strategy

Each v0.8.x sub-version should include:

- fake/unit tests without LM Studio
- script smoke tests
- OCEL trace checks
- PIG report/inspector visibility
- generated file hygiene checks

Validation should prove that the feature works through the ChantaCore spine, not only as an isolated helper.

## 10. Exit Criteria for v0.8.x

By the end of v0.8.x, ChantaCore should have:

- read-only workspace/repo inspection
- safe permission skeleton
- edit proposal and approved patch application
- background worker process
- scheduler/recurring process run support
- all internal harness actions traceable through OCEL/OCPX/PIG

These are exit criteria for the Internal Harness Layer phase. They do not imply external connector support.

## 11. Remaining Limitations After v0.8.x

- external connectors still future work
- MCP/plugin system still future work
- web/network tools still future work unless separately approved
- full production sandbox still future work
- full UI dashboard still future work

v0.8.x should make ChantaCore more operationally capable without changing its identity: ChantaCore remains a process-intelligence-native agent runtime, not a generic harness with process intelligence bolted on afterward.

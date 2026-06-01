# ChantaCore Version Documents

Version documents are stored by minor-version folder:

```text
docs/versions/vMAJOR.MINOR/
  vMAJOR.MINOR.PATCH_slug.md
  chanta_core_vMAJOR_MINOR_PATCH_restore.md
```

Examples:

```text
docs/versions/v0.19/chanta_core_v0_19_9_restore.md
docs/versions/v0.20/v0.20.1_self_workspace_awareness.md
docs/versions/v0.23/chanta_core_v0_23_foundation_restore.md
docs/versions/v0.24/chanta_core_v0_24_0_restore.md
```

Use this folder for restore-grade version records, version contracts, version audits, and migration notes that belong to a specific release line. General documentation that is not tied to one version should remain directly under `docs/` or another topic-specific documentation folder.

## Release-Line Orientation

Current restore records should use this release-line orientation when explaining
version intent:

- `v0.10.x` through `v0.18.x`: Core / Process Intelligence. These releases
  build the organ of observation and the OCEL-native event/object/relation
  substrate.
- `v0.19.x`: Internal Observation + Digestion. These releases observe and
  digest external traces, skills, and behavior into OCEL-observable state and
  candidates.
- `v0.20.x`: OCEL-native Self-Awareness. These releases let ChantaCore observe
  its own workspace, code, project surfaces, candidates, verification reports,
  and intentions as OCEL object-centric processes.
- `v0.21.x`: Deep Self-Introspection. This line is reserved for deeper
  OCEL-oriented inspection of runtime, capability, policy, context, and trace
  consistency.
- `v0.22.x`: Self-Modification Safety. This line defines safety contracts,
  gates, lifecycle policy, patch policy, and observability before any
  self-modification capability is enabled.
- `v0.23.x`: Internal Dominion Foundation. This line defines a vendor-neutral
  internal control grammar for external runtimes under OCEL-visible gates and
  authorizations. `v0.23.1` adds declared runtime/agent/system inventory,
  `v0.23.2` adds capability observation/digestion, `v0.23.3` adds candidate-only
  control requests/action candidates, `v0.23.4` adds control plan and target
  binding, `v0.23.5` adds static safety checks, `v0.23.6` adds foundation-level
  declared runtime preflight/reachability checks, `v0.23.7` adds human review
  plus Dominion Gate state and unconsumed single-use authorization artifacts,
  `v0.23.8` adds authorization / bounded dispatch / status / output /
  outcome boundary artifacts without consuming authorization or dispatching,
  and `v0.23.9` consolidates Internal Dominion Foundation v1 for release readiness.
  It is not Self-Execution Safety and does not dispatch.
  Restore-grade v0.23 records live under `docs/versions/v0.23/`; direct
  `docs/versions/v0.23.*.md` compatibility files were folded into that folder.
- `v0.24.x`: Internal Provider / Local Runtime Provider. Self-execution and
  bounded local runtime/provider work belongs to this later provider track, not
  to v0.23.x. `v0.24.0` introduces the contract-only Internal Provider
  foundation, `v0.24.1` declares the provider registry and capability surface,
  `v0.24.2` activates only read-only workspace tree/metadata observation,
  `v0.24.3` activates bounded repository search and bounded sanitized file
  read/excerpt providers, `v0.24.4` activates bounded read-only OCEL/PIG/OCPX
  process-intelligence inspection providers, `v0.24.5` activates inert local
  runtime command candidate creation, `v0.24.6` activates deterministic static
  safety and declared preflight without execution, `v0.24.7` activates a gated
  bounded local runtime execution boundary, `v0.24.8` interprets bounded output
  without rerun or repair, and `v0.24.9` consolidates the provider foundation
  for v0.25 readiness.
  This track does not permit unrestricted shell, provider adapters, or local
  runtime execution before their scoped release units.
- `v0.25.x`: Bounded General Agent Surface & Internal Tool Routing. `v0.25.0`
  introduces the contract-only Agent Surface Contract and does not execute
  ask/REPL, tool routing, provider invocation, local commands, memory
  continuity, workspace workbench, or external adapters. `v0.25.1` introduces
  turn envelope and conversation-local interaction context records without
  intent classification, safety gate, routing, provider invocation, command
  execution, memory promotion, persistent memory write, or persona mutation.
  `v0.25.2` introduces deterministic intent classification and task framing
  without safety gate, final no-action/blocked/clarification decisions, tool
  routing, provider invocation, command execution, memory mutation, external
  adapters, or LLM judge. `v0.25.3` introduces deterministic safety/no-action/
  clarification gate decisions without creating route plans, selecting or
  invoking providers, executing local commands, executing ask/REPL, promoting
  memory, mutating persona, implementing external adapters, or using an LLM
  judge. `v0.25.4` introduces deterministic tool route planning and provider
  selection without route execution, provider invocation, local command
  execution, response assembly, memory mutation, external adapters, or LLM
  judge. `v0.25.5` introduces internal provider invocation orchestration through
  provider-owned boundaries, result references, traces, result bundles, and
  evidence seeds without direct file/search/process/command access, final
  response assembly, ask/REPL, memory mutation, external adapters, raw provider
  output inlining, or LLM judge. `v0.25.6` introduces response assembly and
  evidence binding from provider result refs or gate outcomes without final
  response emission, ask/REPL execution, provider invocation, direct
  file/search/process/command access, memory mutation, external adapters, raw
  provider output inlining, raw secret output, or LLM judge. `v0.25.7`
  introduces a synchronous Ask / REPL Surface that emits only v0.25.6 assembled
  responses, one explicit user turn at a time, without autonomous loops,
  background execution, self-prompting, direct provider/file/process/command
  bypasses, command rerun, automatic repair, memory mutation, external
  adapters, raw provider output emission, raw secret output, or LLM judge.
  `v0.25.8` introduces report-derived Agent Trace / Usability Telemetry that
  creates source bundles, surface traces, OCEL projections, metric sets, and
  descriptive telemetry reports from existing v0.25.7 artifacts without
  executing ask/REPL, emitting final responses, invoking providers, executing
  commands, starting background collection, running continuous watchers,
  performing autonomous optimization, implementing workspace workbench UI,
  promoting memory, mutating persona, persisting raw transcripts, exposing raw
  secrets, inlining raw provider output, implementing external adapters, or
  using an LLM judge. `v0.25.9` consolidates v0.25.0 through v0.25.8 into
  Bounded General Agent Surface Foundation v1, creates release manifest,
  coverage, safety, pipeline, trace/telemetry, gap, v0.26 readiness, handoff,
  and consolidation artifacts, and may mark `ready_for_v0_26` when criteria
  pass. It does not execute ask/REPL, emit final responses, invoke providers,
  execute local commands, run background collection or autonomous optimization,
  implement workspace workbench UI, mutate memory/persona, implement external
  adapters, introduce Schumpeter split, add GrowthKernel runtime dependency,
  persist raw transcripts, expose secrets, inline raw provider output, or use
  an LLM judge.
- `v0.26.x`: Workspace Agent Workbench. `v0.26.0` declares the contract-only
  Workspace Agent Workbench layer: surface modes, panel contracts, view
  permissions, action boundaries, read-only inspection, approval, command,
  snapshot, trace privacy, OCEL visibility, and roadmap boundaries. It does not
  implement actual UI or panels, trace explorer, provider browser, evidence
  inspector, approval console, run dashboard, command surface, snapshot/export,
  ask/REPL execution, final response emission, provider invocation, local
  command execution, memory continuity, external adapters, Schumpeter split, raw
  transcript/provider/secret persistence, or LLM judge. The next step is
  `v0.26.1` Workbench View State & Panel Model. `v0.26.1` creates view-state,
  panel model, layout, selection, filter, focus, navigation, and session-view
  records without UI rendering, panel behavior, trace/provider/evidence/
  approval/dashboard/command/snapshot behavior, ask/REPL execution, provider
  invocation, command execution, memory continuity, external adapters, raw data
  persistence, or LLM judge. The next step is `v0.26.2` Trace Explorer &
  Pipeline Timeline. `v0.26.2` creates Trace Explorer and Pipeline Timeline
  view artifacts from existing v0.26.1 view state and v0.25.8 trace telemetry
  refs. It does not render UI or panels, rerun stages/routes, invoke providers,
  execute ask/REPL, emit final responses, execute local commands, mutate
  traces, promote memory, add external adapters, persist raw transcript/
  provider/secret material, or use an LLM judge. The next step is `v0.26.3`
  Provider / Capability Browser. `v0.26.3` creates Provider / Capability
  Browser view artifacts from v0.24 provider registry/capability surfaces,
  v0.25 route/provider-selection refs, and v0.26 workbench state. It does not
  invoke or test-run providers, bypass provider boundaries, add external or
  vendor adapters, add process-mining runtime dependencies, treat PIG as memory,
  policy mutation, or execution, render UI, execute ask/REPL, emit final
  responses, execute local commands, mutate memory/persona, persist raw data, or
  use an LLM judge. The next step is `v0.26.4` Evidence / Report Inspector.
  `v0.26.4` creates Evidence / Report Inspector view artifacts from response
  assembly, evidence bundle, claim/support, safety, routing, provider browser,
  trace, PIG guidance, and failure refs. It does not rewrite responses, use
  factuality or safety LLM judges, invoke providers, rerun routes/stages,
  execute approvals, execute ask/REPL, emit final responses, execute local
  commands, mutate memory/persona/PIG/policy, add external or vendor adapters,
  persist raw transcript/provider/secret material, or use an LLM judge. The
  next step is `v0.26.5` Safety Gate / Approval Console. `v0.26.5` creates
  Safety Gate / Approval Console view and decision-record artifacts from safety,
  evidence, provider, route, trace, PIG guidance, risk, action-candidate, and
  human-intervention refs. It may record approval, rejection, deferral, manual
  review, scope, expiry, and non-executable approval token refs, but it does not
  execute approvals, execute approval tokens, auto-approve, execute commands,
  invoke providers, rerun routes/stages, execute ask/REPL, emit final responses,
  execute local commands, mutate memory/persona/PIG/policy, add external or
  vendor adapters, persist raw transcript/provider/secret material, or use an
  LLM judge. The next step is `v0.26.6` Run Dashboard / Session Monitor.
  `v0.26.6` creates Run Dashboard / Session Monitor view artifacts from
  ask/REPL, trace telemetry, approval, evidence, provider, PIG guidance, failure,
  and session refs. It may create run cards, pipeline status, descriptive status
  summaries, refs-only session summaries, repeated pattern views, context refs,
  metrics, and dashboard reports, but it does not start background monitors,
  continuous watchers, auto-refresh execution, rerun/retry/repair, autonomous
  optimization, command execution, approval execution, provider invocation,
  ask/REPL execution, final response emission, local command execution, memory
  continuity/promotion, persona mutation, external adapters, raw material
  persistence, or LLM judge. The next step is `v0.26.7` Workbench Command
  Surface. `v0.26.7` creates Workbench Command Surface command candidates,
  do-nothing candidates, skill/action/route/provider/file-edit/ask/snapshot
  request candidates, rationale, evidence, risk, PIG guidance, safety finding,
  approval requirement, boundary trace, decision record, non-executing envelope,
  result, history, audit, and report artifacts. It does not execute or dispatch
  commands, invoke providers, execute local runtime, mutate files, apply
  patches, execute ask/REPL, emit final responses, rerun routes/stages,
  auto-retry, auto-repair, start autonomous loops, execute approvals or approval
  tokens, promote memory, mutate persona, implement external/vendor adapters,
  treat PIG as memory/policy/execution, persist raw material, or use an LLM
  judge. The next step is `v0.26.8` Workbench Snapshot / OCEL Export.
  `v0.26.8` creates refs-only snapshot, manifest, ref bundle, OCEL export
  package, event-quality, trace-coverage, redaction, reproducibility, export
  boundary, and report artifacts from v0.26 workbench refs. It does not promote
  memory, write persistent memory, extract memory candidates, mutate persona,
  export raw transcript/provider/secret/credential/private path material, sync
  externally, add external/vendor adapters, add pm4py/ocpa runtime dependencies,
  execute commands/providers/local runtime/ask, emit final responses, mutate
  files, rerun routes/stages, retry, repair, start autonomous loops, treat PIG
  as memory/policy/execution, introduce Schumpeter split, or use an LLM judge.
  The next step is `v0.26.9` Workspace Agent Workbench Consolidation.
  `v0.26.9` consolidates `v0.26.0` through `v0.26.8` into Workspace Agent
  Workbench Foundation v1. It creates release manifest, capability map,
  coverage matrix, safety and interaction boundary reports, event and trace
  consolidation, usability readiness, feedback-loop readiness, future gap
  register, `v0.27` readiness, refs-only handoff packet, and consolidation
  report artifacts. It does not implement new Workbench panels, memory
  candidate extraction, memory promotion, persistent memory writes, persona
  mutation, command/provider/local/file/ask execution, final response emission,
  rerun/retry/repair, autonomous loops, external/vendor adapters, pm4py/ocpa
  runtime dependencies, raw transcript/provider/secret persistence, Schumpeter
  split, or LLM judging. The next step is `v0.27.0` Memory Candidate &
  Continuity Contract.
- `v0.27.x`: Memory Candidate & Continuity.
  `v0.27.0` introduces the contract-only Memory Candidate & Continuity layer
  after the Workspace Agent Workbench Foundation v1 handoff. It declares the
  full `v0.27.x` roadmap and source, candidate, evidence, scoring, promotion,
  durable memory, continuity, injection, audit, privacy, governance, PIG, and
  safety policies. It does not extract or score memory candidates, promote
  memory, write persistent memory, create durable memory records, create session
  continuity contexts, inject continuity, mutate persona or behavior policy,
  persist raw transcript/provider output as memory, treat PIG as memory,
  invoke providers, execute commands, bypass safety gates, implement external
  adapters, introduce Schumpeter split, expose secrets or credentials, or use an
  LLM judge. `v0.26.10` Release Hygiene / Governance Hardening is recommended
  before implementation-heavy memory work and required before `v0.27.5`
  persistent write or durable registry work. The next step is `v0.27.1` Memory
  Source / Ref Boundary.
  `v0.27.1` creates the Memory Source / Ref Boundary. It builds source category
  catalogs, refs, bundles, registry views, eligibility rules/evaluations/
  decisions, redaction views/reports, quality signals/reports, forbidden-source
  reports, and candidate-readiness boundaries. It remains non-mutating: source
  eligibility is not candidate extraction, source quality is not memory scoring,
  source bundles are not memory registries, and no memory candidates, durable
  memory records, continuity injection, provider/command execution, external
  adapters, Schumpeter split, raw memory, or LLM judge are introduced. The next
  step is `v0.27.2` Memory Candidate Extraction.
- `v0.28.x`: Public Alpha / Schumpeter Split Preparation.
- `v0.29.x+`: External Skill / External Provider Adapter Development.
- `v0.30.x+`: External Agent Dominion Bridge.

Do not describe `v0.20.x` as a write/shell/network/MCP/plugin safety track.
Those capabilities remain excluded from the self-awareness foundation unless a
later release line explicitly introduces and verifies a dedicated safety layer.

# v0.25 Bounded General Agent Surface & Internal Tool Routing

This folder stores v0.25.x records under the version-minor layout required by
the restore document policy.

Canonical v0.25 records:

- `v0.25.0_agent_surface_contract.md`
- `v0.25.1_turn_envelope_interaction_context.md`
- `v0.25.2_intent_classification_task_framing.md`
- `v0.25.3_safety_no_action_clarification_gate.md`
- `v0.25.4_tool_routing_plan_provider_selection.md`
- `v0.25.5_internal_provider_invocation_orchestrator.md`
- `v0.25.6_response_assembly_evidence_binder.md`
- `v0.25.7_ask_repl_surface.md`
- `v0.25.8_agent_trace_usability_telemetry.md`
- `v0.25.9_general_agent_usability_consolidation.md`

Restore interpretation:

- v0.25.0 defines the Agent Surface Contract.
- v0.25.0 is contract-only.
- v0.25.0 does not execute ask/REPL, route tools, invoke providers, execute
  local commands, promote memory, implement workspace workbench, implement
  external provider or external agent adapters, introduce Schumpeter split
  logic, expose credentials, or use an LLM judge.
- v0.25.1 implements Turn Envelope & Interaction Context.
- v0.25.1 creates envelope/context/trace records only. It does not execute
  ask/REPL, classify intent, route tools, invoke providers, execute local
  commands, promote memory, write persistent memory, mutate persona, implement
  external adapters, or use an LLM judge.
- v0.25.2 is reserved for Intent Classification & Task Framing.
- v0.25.2 implements deterministic intent classification and task framing.
- v0.25.2 does not execute ask/REPL, run a safety/no-action/clarification
  gate, finalize no-action/blocked/clarification decisions, route tools, invoke
  providers, execute local commands, promote memory, write persistent memory,
  mutate persona, implement external adapters, or use an LLM judge.
- v0.25.3 implements Safety / No-Action / Clarification Gate.
- v0.25.3 finalizes allow-route, no-action, clarification, needs-more-input,
  blocked, deferred, or failed outcomes only. It does not create tool routing
  plans, select or invoke providers, execute local commands, execute ask/REPL,
  promote memory, write persistent memory, mutate persona, implement external
  adapters, or use an LLM judge.
- v0.25.4 implements Tool Routing Plan & Provider Selection.
- v0.25.4 creates route plans, provider capability catalog views, provider
  selections, route steps, dependencies, and risk reviews only. It does not
  invoke providers, execute route steps, execute local commands, execute
  ask/REPL, assemble responses, promote memory, write persistent memory, mutate
  persona, implement external adapters, or use an LLM judge.
- v0.25.5 implements Internal Provider Invocation Orchestrator.
- v0.25.5 orchestrates registered internal provider invocations through
  provider-owned boundaries, creates result refs, invocation traces, result
  bundles, and evidence seeds for v0.25.6. It does not directly read files,
  search repositories, inspect processes, execute local commands, bypass
  provider boundaries, assemble final responses, execute ask/REPL, promote
  memory, write persistent memory, mutate persona, implement external adapters,
  inline raw provider output, or use an LLM judge.
- v0.25.6 implements Response Assembly & Evidence Binder.
- v0.25.6 binds provider result refs or gate outcomes into evidence bundles,
  claims, supports, response sections, answer drafts, and assembled response
  artifacts. It does not emit final responses through ask/REPL, invoke
  providers, execute commands, read files directly, promote memory, mutate
  persona, implement external adapters, inline raw provider output, expose raw
  secrets, or use an LLM judge.
- v0.25.7 implements Ask / REPL Surface.
- v0.25.7 runs one explicit user turn through the bounded v0.25 pipeline and
  emits only v0.25.6 assembled responses. It does not implement autonomous
  loops, background execution, self-prompting, direct provider invocation,
  direct file/search/process/local command bypasses, command rerun, automatic
  repair, memory promotion, persistent memory write, persona mutation, external
  adapters, raw provider output emission, raw secret output, or an LLM judge.
- v0.25.8 implements Agent Trace / Usability Telemetry.
- v0.25.8 creates report-derived trace, OCEL projection, metric, and telemetry
  artifacts from existing v0.25.7 ask/repl reports. It does not execute
  ask/REPL, emit final responses, invoke providers, execute local commands,
  start background collection, run continuous watchers, perform autonomous
  optimization, implement workspace workbench UI, promote memory, write
  persistent memory, mutate persona, implement external adapters, persist raw
  transcripts, inline raw provider output, expose raw secrets, or use an LLM
  judge.
- v0.25.9 implements General Agent Usability Consolidation.
- v0.25.9 consolidates v0.25.0 through v0.25.8 into Bounded General Agent
  Surface Foundation v1, creates release/readiness artifacts, and may mark
  ready_for_v0_26 when substrate criteria pass. It does not execute ask/REPL,
  emit final responses, invoke providers, execute local commands, start
  background daemons or continuous watchers, perform autonomous optimization,
  implement workspace workbench UI, promote memory, write persistent memory,
  mutate persona, implement external adapters, persist raw transcripts, inline
  raw provider output, expose raw secrets, introduce Schumpeter split, add
  GrowthKernel runtime dependency, or use an LLM judge.

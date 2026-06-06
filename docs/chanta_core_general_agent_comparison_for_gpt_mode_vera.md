# ChantaCore Progress And General Agent Comparison For GPT Mode Vera

Date: 2026-06-03

Audience: GPT Mode Vera

Purpose: give GPT Mode Vera a balanced orientation about ChantaCore's current state, especially its recent General Agent direction, without turning readiness artifacts into unsupported runtime claims.

## Reading Rule

This document separates confirmed local evidence from interpretation.

Confirmed means the statement is grounded in ChantaCore repository files or public product documentation inspected on 2026-06-03. Interpretation means a conservative judgment built from those facts. Unknown means the available evidence is not enough to claim the point.

The default action posture remains no action. The do-nothing alternative is valid when evidence is missing, scope is unclear, or a requested action would cross an execution, network, credential, provider, private-data, or external-side-effect boundary.

## Local Evidence Used

- `pyproject.toml`: package version is `0.29.9`.
- `src/chanta_core/__init__.py`: `__version__ = "0.29.9"`.
- `docs/versions/README.md`: release-line orientation from v0.10.x through v0.30.x.
- `docs/WORKBENCH_FOUNDATION.md`: v0.26 workbench surfaces are report/preview surfaces, not provider invocation or command execution.
- `docs/MEMORY_FOUNDATION.md`: v0.27 memory continuity remains bounded and is not autonomous memory-driven execution.
- `docs/PUBLIC_ALPHA_RUNTIME_PROFILE.md`: v0.28 public alpha profile keeps provider invocation, command expansion, external adapters, RPA, and Schumpeter company runtime disabled or future-track.
- `docs/versions/v0.29/v0.29.8_limited_provider_invocation_preview_gate.md`: limited preview gate is not provider invocation and does not execute preview invocation.
- `docs/versions/v0.29/v0.29.9_external_provider_adapter_foundation_consolidation.md`: External Provider Adapter Foundation v1 is consolidation-only and not provider runtime.

Known verification caveat: previous implementation notes recorded passing focused v0.29.9 tests, v0.29 track tests, representative v0.26.9/v0.27.9/v0.28.9 foundation regressions, and v0.29.9 CLI checks. A full `py -m pytest` run timed out at about 303 seconds, so complete full-suite status is unknown.

## External Evidence Used

- Hermes Agent official documentation: https://hermes-agent.nousresearch.com/docs/
- Hermes Agent features overview: https://hermes-agent.nousresearch.com/docs/user-guide/features/overview/
- OpenCode official site: https://opencode.ai/
- OpenClaw official site: https://openclaw.ai/
- OpenClaw docs entry point found through search: https://docs.openclaw.ai/getting-started

External-product numbers such as stars, users, contributors, and adoption scale are not independently verified here. If a public page states a number, this document treats it as a product claim, not as an audited fact.

## ChantaCore Progress Summary

ChantaCore has developed as an OCEL-native process-intelligence and agent-foundation system. The repository orientation describes these release lines:

| Release line | Local meaning | Confirmed boundary |
| --- | --- | --- |
| v0.10.x-v0.18.x | Core / Process Intelligence | Builds observation and OCEL-native event/object/relation substrate. |
| v0.19.x | Internal Observation + Digestion | Observes and digests traces, skills, and behavior into observable candidates. |
| v0.20.x | OCEL-native Self-Awareness | Observes its own workspace, code, candidates, verification reports, and intentions. Not a write/shell/network safety track. |
| v0.21.x | Deep Self-Introspection | Reserved for deeper runtime, capability, policy, context, and trace consistency inspection. |
| v0.22.x | Self-Modification Safety | Defines safety contracts, gates, lifecycle, patch policy, and observability before self-modification. |
| v0.23.x | Internal Dominion Foundation | Defines vendor-neutral internal control grammar, authorization artifacts, and gates. It does not dispatch. |
| v0.24.x | Internal Provider / Local Runtime Provider | Adds bounded internal provider concepts and local-runtime boundaries. It is not unrestricted shell or external adapter runtime. |
| v0.25.x | Bounded General Agent Surface & Internal Tool Routing | Creates the first bounded general-agent surface: turn envelope, intent/task framing, safety/no-action/clarification gates, route planning, provider orchestration, response assembly, Ask/REPL surface, trace/usability telemetry, and v1 consolidation. |
| v0.26.x | Workspace Agent Workbench Foundation v1 | Creates workbench view/report surfaces, approval console previews, dashboard/snapshot concepts, and consolidation. It is not actual autonomous UI execution. |
| v0.27.x | Memory Candidate & Continuity Foundation v1 | Creates memory source boundaries, candidate/continuity concepts, promotion gates, durable registry concepts, and injection boundaries. It is not autonomous memory mutation by default. |
| v0.28.x | Public Alpha / Schumpeter Split Preparation Foundation v1 | Documents public/private split, Schumpeter future boundary, public alpha runtime profile, and safety surfaces. Provider invocation and external adapters remain disabled/future-track. |
| v0.29.x | External Skill / External Provider Adapter Development | Builds external provider adapter foundation without unrestricted invocation. v0.29.9 consolidates it as External Provider Adapter Foundation v1. |
| v0.30.x+ | External Agent Dominion Bridge | Future track. v0.30.0 should begin with a contract, not execution. |

## Recent v0.29 Track Summary

v0.29.x is important because it defines the outer edge of what people may be tempted to call "External Skill" or "external provider" capability.

| Version | What it created | What it did not create |
| --- | --- | --- |
| v0.29.0 | External Provider Adapter Contract | Provider invocation, provider registration, SDK invocation, network, credential access. |
| v0.29.1 | Provider Capability Inventory / Adapter Registry | Live provider registration or provider execution. |
| v0.29.2 | Mock Adapter Harness / No-Network Default | Live adapter use or network calls. |
| v0.29.3 | Permission / Safety / Scope Gate | Permission grant or provider invocation. |
| v0.29.4 | Credential / Secret / Network Boundary | Credential value access, secret retrieval, or network access. |
| v0.29.5 | Adapter Invocation Candidate / Dry-Run Plan | Provider call, payload send, SDK invocation, network call. |
| v0.29.6 | Provider Invocation Approval / Audit / Rollback Boundary | Approval grant, rollback execution, retry, live invocation. |
| v0.29.7 | External Skill Packaging / Certification Matrix | Package publish, release tag, production certification, certified live adapter. |
| v0.29.8 | Limited Provider Invocation Preview Gate | Preview execution, provider invocation, network/credential access. |
| v0.29.9 | External Provider Adapter Foundation Consolidation / External Provider Adapter Foundation v1 | Provider runtime, live adapter runtime, external agent dominion runtime. |

The most important local fact is that v0.29.9 may declare foundation readiness, but the documented runtime readiness flags remain false:

- `provider_invocation_runtime_ready = False`
- `limited_preview_execution_ready_now = False`
- `live_adapter_runtime_ready = False`
- `external_agent_dominion_runtime_ready = False`

## Current General Agent Capability

Confirmed local capability:

ChantaCore has a bounded General Agent foundation. It can represent user turns, classify intent, frame tasks, choose no-action/clarification/safety outcomes, plan routes, bind evidence, assemble responses, inspect process traces, represent workbench and memory surfaces, and consolidate readiness reports. It has a strong native vocabulary for OCEL, PIG, OCPX, evidence refs, safety gates, audit trails, no-op outcomes, and withdrawal conditions.

Conservative interpretation:

ChantaCore is closer to a governance-first agent operating system kernel than to a high-agency desktop assistant. Its strength is not "doing everything now"; its strength is making it hard to confuse a candidate, preview, certification, or readiness report with actual execution permission.

Not supported by current evidence:

- It should not be described as an unrestricted independent agent system.
- It should not be described as a live external provider runtime.
- It should not be described as a provider SDK runtime.
- It should not be described as a network-capable external skill runner.
- It should not be described as a credential-accessing assistant.
- It should not be described as an RPA/A360/Brity/UiPath adapter runtime.
- It should not be described as an External Agent Dominion implementation.

## External Skill Readiness

It is reasonable to say that ChantaCore is structurally ready to define External Skill manifests, certification matrices, preview gates, and consolidation artifacts.

It is not yet reasonable to say that ChantaCore can freely run External Skills against live providers. The current local evidence supports "external skill packaging/certification/readiness foundation", not "live external skill execution."

GPT Mode Vera should preserve this difference:

- External skill manifest is not runtime enablement.
- Adapter package manifest is not package publish.
- Certification matrix is not production certification.
- Certified mock is not certified live adapter.
- Preview gate readiness is not preview execution.
- Foundation consolidation is not provider runtime.

## General Agent Comparison

This table compares product orientation, not absolute quality. A direct benchmark was not run.

| System | Confirmed orientation | Strongest apparent area | Safety/authority posture | Main uncertainty |
| --- | --- | --- | --- | --- |
| ChantaCore v0.29.9 | OCEL-native bounded agent foundation and external provider adapter foundation consolidation. | Evidence, safety boundaries, auditability, readiness separation, refs-only handoff, no-op validity. | Strongly deny-first. Provider/network/credential/command/runtime flags remain false unless later gates explicitly change them. | Full-suite test status is unknown due timeout; practical runtime UX and autonomous task throughput are not proven by v0.29.9 alone. |
| Hermes Agent | Official docs describe an autonomous agent by Nous Research with memory, skills, messaging platforms, tools, code execution, browser automation, voice, MCP, provider routing, and plugins. | Persistent assistant behavior, cross-session memory, tools, automation, messaging integrations, skills. | Official docs mention command approval, authorization, and container isolation, but this document did not audit implementation. It is more execution-oriented than ChantaCore. | Actual safety in a specific deployment, isolation correctness, and operational reliability are unknown without local audit. |
| OpenCode | Official site describes an open-source coding agent for terminal, IDE, and desktop that helps write code and supports LSP, multi-session, many models, and editor surfaces. | Codebase editing, developer workflow integration, coding-agent ergonomics. | More code-execution/editing oriented. It may be appropriate for programming workflows but is not shown here as a general governance foundation. | External performance/adoption claims are not independently verified; exact safety model depends on configuration and model/tool permissions. |
| OpenClaw | Official site presents it as a personal assistant that "actually does things", with chat-app control, local install, source checkout, and examples involving email/calendar/actions. | Broad personal-agent automation and tool orchestration. | High-agency execution posture. This may be powerful but creates larger safety, credential, private-data, and side-effect exposure than ChantaCore's current default. | Official docs page was partially inaccessible in this session; public claims are highly promotional; security and reliability require independent audit. |

## Balanced Interpretation For GPT Mode Vera

ChantaCore should not try to compete with Hermes Agent, OpenCode, or OpenClaw on raw action-taking yet. Those systems are more outwardly execution-oriented. Hermes Agent appears closer to a persistent autonomous assistant; OpenCode appears closer to a practical coding agent; OpenClaw appears closer to a broad personal automation agent.

ChantaCore's current advantage is different: it preserves distinctions that execution-heavy systems often blur. It asks whether a thing is a candidate, a plan, an approval requirement, a preview gate, a certification, a handoff packet, or an actual executable permission. That distinction matters when the agent might touch providers, credentials, network, private data, local files, commands, RPA, or other agents.

So the balanced view is:

ChantaCore is not yet the most capable "do everything" agent. It is a strong foundation for making agent capability legible, auditable, revocable, and safe before execution is allowed.

## Suggested Operating Posture For GPT Mode Vera

Use ChantaCore as a thinking and governance substrate, not as proof that live execution is safe.

When asked whether ChantaCore can do something:

1. Identify the artifact level: contract, candidate, plan, certification, gate, readiness report, or execution.
2. Prefer no-action, defer, or clarification if evidence is incomplete.
3. Do not treat readiness as permission.
4. Do not treat certification as live certification.
5. Do not treat preview eligibility as execution authorization.
6. Do not treat a manifest as runtime enablement.
7. Require explicit future gates before provider/network/credential/command/external-agent execution.
8. Mark unknown external comparisons as unknown instead of filling gaps with confidence.

## Practical Answer To "Can ChantaCore Operate As An Independent Agent System?"

Evidence-supported answer:

ChantaCore can be treated as an independent bounded agent-foundation system for structured reasoning, process intelligence, internal tool-routing concepts, evidence-based response assembly, workbench/report surfaces, memory candidate governance, and external provider adapter readiness consolidation.

Evidence-not-supported answer:

ChantaCore should not yet be treated as an independent high-agency runtime that freely executes external skills, invokes providers, browses the network, uses credentials, controls a workstation, performs RPA, or delegates to external agents.

The right phrase is "bounded independent agent foundation", not "unrestricted autonomous agent runtime."

## What GPT Mode Vera Should Avoid Saying

- "ChantaCore is already equivalent to Hermes Agent/OpenClaw as a live general assistant."
- "ChantaCore can now invoke external providers."
- "External Skill readiness means external skill execution."
- "ready_for_v030_contract means external agent dominion runtime."
- "Certification means production certification."
- "No-network certification means network access is safe."
- "Approval boundary means approval was granted."
- "Rollback plan means rollback can be executed."
- "A PIG report can authorize execution."
- "An LLM judge can be the sole authority."

## What GPT Mode Vera Can Safely Say

- ChantaCore v0.29.9 is at External Provider Adapter Foundation v1.
- The foundation is consolidation-only and explicitly not provider runtime.
- v0.29.x built the conceptual, policy, certification, preview, and consolidation layers for future External Skill work.
- ChantaCore's General Agent direction is strongest in process visibility, safety boundaries, evidence, audit, and readiness separation.
- Compared with Hermes Agent, OpenCode, and OpenClaw, ChantaCore is currently less execution-oriented and more boundary-oriented.
- Future versions may expand capability, but current claims must stay within the documented gates.

## Recommended Comparison Narrative

If GPT Mode Vera needs one paragraph:

ChantaCore is best understood as a safety-first, OCEL-native agent foundation that has reached a structured readiness point for External Skill work, but not a live provider or broad personal automation runtime. Hermes Agent and OpenClaw appear more directly autonomous and tool-executing, while OpenCode is more specialized for code editing and developer workflows. ChantaCore's comparative strength is not raw action breadth; it is the discipline of separating observation, candidate, plan, certification, preview, approval, handoff, and execution so that future agent abilities do not silently cross safety boundaries.

## Evidence Strength

High confidence:

- Local version is v0.29.9.
- v0.29.9 docs declare External Provider Adapter Foundation v1.
- v0.29.9 docs explicitly keep provider invocation runtime, limited preview execution, live adapter runtime, and external agent dominion runtime false.
- Local docs consistently preserve no-provider/no-network/no-credential/no-command boundaries across v0.26-v0.29.

Medium confidence:

- ChantaCore is structurally ready for External Skill manifest/certification/preview-gate design.
- ChantaCore is a bounded independent agent foundation rather than an unrestricted runtime.

Low confidence / unknown:

- Full regression status for every historical test line is unknown because the full test suite timed out in prior verification.
- External adoption/performance numbers for Hermes Agent, OpenCode, and OpenClaw are not audited here.
- Whether any of the external systems would outperform ChantaCore on a specific workload is unknown without a benchmark.

## Withdrawal Conditions

Withdraw or revise this document if any of the following become true:

- ChantaCore introduces provider invocation, provider SDK invocation, provider registration, network calls, credential access, command execution, rollback execution, automatic retry, package publishing, live adapter implementation, RPA/A360/Brity/UiPath runtime, external agent dominion runtime, private-data use, raw provider output persistence, or LLM judge sole authority without a later explicit reviewed gate.
- A full regression run reveals failures that invalidate v0.29.9 readiness.
- v0.30.0 changes the boundary from contract-first to execution-first.
- Official external documentation for Hermes Agent, OpenCode, or OpenClaw materially changes.
- A direct benchmark is run and shows different practical capability boundaries.

## Validity Horizon

Valid until v0.30.0 External Agent Dominion Bridge Contract begins, until ChantaCore's external execution policy changes, or until the external comparison targets materially change.

## Final Position For GPT Mode Vera

ChantaCore is ready to discuss and design External Skill work as a bounded, auditable foundation, but it should not be presented as ready for unrestricted live External Skill execution or as a full high-agency personal automation agent. Its current value is disciplined readiness, not unconstrained action.

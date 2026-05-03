# ChantaCore v0.7.1 Restore Notes

ChantaCore v0.7.1 operationalizes the process intelligence substrate with
read-only reports and inspection.

This version adds:

- `src/chanta_core/pig/reports.py`
- `ProcessRunReport`
- `PIGReportService`
- `src/chanta_core/pig/inspector.py`
- `PISubstrateInspection`
- `PISubstrateInspector`

The goal is to make the existing OCEL / OCPX / PIG substrate readable,
inspectable, and reportable by a human operator. It does not add major new
runtime capability.

Reports can summarize:

- recent PI substrate state
- process-instance traces
- session traces
- activity sequence
- relation coverage
- variant and performance summaries
- conformance status
- guidance and decision summaries where available
- skill and tool usage

The substrate inspector summarizes:

- OCEL health
- OCPX recent view state
- PIG report status
- conformance status
- built-in skills
- built-in tools
- warnings

This version is read-only at the reporting layer. It does not mutate OCELStore,
PIArtifactStore, DecisionService, runtime policy, tool policy, or skill/tool
registries.

Guardrails:

- no file write/edit tools
- no shell execution
- no network/web fetch
- no MCP/plugin system
- no worker queue
- no UI dashboard
- no async runtime
- no sandbox
- no source-code self-modification
- no automatic policy promotion
- no learned ranking model
- no full process mining dashboard

PIG remains the process intelligence and reporting layer.

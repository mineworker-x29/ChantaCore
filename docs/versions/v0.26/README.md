# v0.26.x Workspace Agent Workbench

`v0.26.x` is the Workspace Agent Workbench track.

This release line makes agent turns, decisions, routes, provider invocation
references, evidence, assembled responses, and telemetry inspectable through
OCEL-visible workbench contracts. It must increase human control without
creating bypass paths.

## Releases

- `v0.26.0` - Workspace Agent Workbench Contract.
- `v0.26.1` - Workbench View State & Panel Model.
- `v0.26.2` - Trace Explorer & Pipeline Timeline.

## Boundary

`v0.26.0` is contract-only. Actual view state, panel models, trace explorer,
provider browser, evidence inspector, approval console, run dashboard, command
surface, and snapshot/export work remain deferred to later `v0.26.x` releases.
`v0.26.1` creates view-state and panel-model records only; it still does not
render UI or implement panel-specific behavior.
`v0.26.2` creates trace explorer and pipeline timeline view artifacts only; it
does not render UI, rerun stages/routes, invoke providers, execute ask/REPL,
emit final responses, execute commands, mutate traces, promote memory, add
external adapters, persist raw transcript/provider/secret material, or use an
LLM judge.

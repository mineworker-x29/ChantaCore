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
- `v0.26.3` - Provider / Capability Browser.
- `v0.26.4` - Evidence / Report Inspector.
- `v0.26.5` - Safety Gate / Approval Console.
- `v0.26.6` - Run Dashboard / Session Monitor.
- `v0.26.7` - Workbench Command Surface.
- `v0.26.8` - Workbench Snapshot / OCEL Export.
- `v0.26.9` - Workspace Agent Workbench Consolidation.

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
`v0.26.3` creates provider and capability browser view artifacts only; it does
not invoke or test-run providers, bypass provider boundaries, add external or
vendor adapters, add process-mining runtime dependencies, treat PIG as memory,
policy mutation, or execution, render UI, execute ask/REPL, emit final
responses, execute commands, mutate memory/persona, persist raw material, or use
an LLM judge.
`v0.26.4` creates evidence and report inspector view artifacts only; it does not
rewrite or regenerate responses, use factuality/safety LLM judges, invoke or
test-run providers, rerun routes/stages, execute approvals, execute ask/REPL,
emit final responses, execute commands, mutate memory/persona/PIG/policy, add
external or vendor adapters, persist raw transcript/provider/secret material, or
use an LLM judge.
`v0.26.5` creates safety gate and approval console view plus decision-record
artifacts only; it does not execute approvals or approval tokens, auto-approve,
execute commands, invoke providers, rerun routes/stages, execute ask/REPL, emit
final responses, execute local commands, mutate memory/persona/PIG/policy, add
external or vendor adapters, persist raw transcript/provider/secret material, or
use an LLM judge.
`v0.26.6` creates run dashboard and session monitor view artifacts only; it does
not start background monitors, continuous watchers, auto-refresh execution,
rerun or retry runs, repair failures, execute commands or approvals, invoke
providers, execute ask/REPL, emit final responses, enable memory continuity,
mutate memory/persona/PIG/policy, add external or vendor adapters, persist raw
transcript/provider/secret material, or use an LLM judge.
`v0.26.7` creates Workbench Command Surface candidate, decision-record,
boundary-trace, non-executing envelope, result, history, and audit artifacts
only; it does not execute or dispatch commands, invoke providers, execute local
runtime, mutate files, apply patches, execute ask/REPL, emit final responses,
rerun routes/stages, retry or repair automatically, start autonomous loops,
execute approvals or approval tokens, mutate memory/persona/PIG/policy, add
external or vendor adapters, persist raw transcript/provider/secret material, or
use an LLM judge.
`v0.26.8` creates Workbench Snapshot / OCEL Export artifacts only; it does not
promote memory, write persistent memory, extract memory candidates, mutate
persona, export raw transcript/provider/secret/credential/private path material,
sync externally, add external/vendor adapters, add pm4py/ocpa runtime
dependencies, execute commands/providers/local runtime/ask, emit final
responses, mutate files, rerun routes/stages, retry, repair, start autonomous
loops, mutate PIG/policy, introduce Schumpeter split, or use an LLM judge.
`v0.26.9` consolidates `v0.26.0` through `v0.26.8` as Workspace Agent
Workbench Foundation v1 and prepares a refs-only `v0.27` handoff; it does not
implement memory candidate extraction, memory scoring, memory promotion,
persistent memory writes, persona mutation, command/provider/local/file/ask
execution, final response emission, rerun/retry/repair, autonomous loops,
external/vendor adapters, pm4py/ocpa runtime dependencies, raw transcript/
provider/secret persistence, Schumpeter split, or LLM judging.

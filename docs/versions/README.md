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
- `v0.25.x`: General Agent Usability & Tool Routing.
- `v0.26.x`: Workspace Agent Workbench.
- `v0.27.x`: Memory Candidate & Continuity.
- `v0.28.x`: Public Alpha / Schumpeter Split Preparation.
- `v0.29.x+`: External Skill / External Provider Adapter Development.

Do not describe `v0.20.x` as a write/shell/network/MCP/plugin safety track.
Those capabilities remain excluded from the self-awareness foundation unless a
later release line explicitly introduces and verifies a dedicated safety layer.

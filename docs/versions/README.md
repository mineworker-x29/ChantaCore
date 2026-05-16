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

Do not describe `v0.20.x` as a write/shell/network/MCP/plugin safety track.
Those capabilities remain excluded from the self-awareness foundation unless a
later release line explicitly introduces and verifies a dedicated safety layer.

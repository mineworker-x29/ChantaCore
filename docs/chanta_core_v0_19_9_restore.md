# ChantaCore v0.19.9 Restore

## Version

- Version: `0.19.9`
- Name: Observation/Digestion Ecosystem Consolidation
- Status: restore reference

## Purpose

v0.19.9 consolidates the Observation/Digestion ecosystem. It summarizes v0.19.0 through v0.19.8 and provides a read-only view of skill seeds, registry view, proposal surface, gated invocation surface, conformance and smoke checks, static digestion, observation spine, cross-harness adapter contracts, and adapter candidate building.

## Component Readiness

The consolidation service distinguishes component readiness levels:

- `ready`
- `partial`
- `contract_only`
- `stub_only`
- `blocked`
- `future_track`
- `unknown`

Unavailable components degrade to findings and partial readiness instead of crashing the consolidation report.

## Safety Boundary

External candidates remain non-executable. The safety boundary report confirms that external harness execution, external script execution, shell, network, workspace write, MCP, plugin, memory mutation, persona mutation, overlay mutation, raw transcript export, and full body export remain disabled by default.

v0.19.9 does not add execution capabilities.

## Release Coverage

The release manifest includes:

- `v0.19.0` internal Observation/Digestion skill seed pack
- `v0.19.1` skill registry view
- `v0.19.2` proposal integration
- `v0.19.3` gated invocation
- `v0.19.4` conformance and smoke checks
- `v0.19.5` expanded static digestion
- `v0.19.6` agent observation spine and movement ontology
- `v0.19.7` cross-harness trace adapter contracts
- `v0.19.8` observation-to-digestion adapter candidate builder
- `v0.19.9` ecosystem consolidation

## CLI

`chanta-cli observe-digest ecosystem` provides read-only diagnostics:

- `snapshot`
- `components`
- `capabilities`
- `safety`
- `gaps`
- `manifest`
- `report`

Outputs are redacted summaries and include skill counts, adapter counts, candidate counts, executable external candidate count, safety boundary booleans, and future gaps.

## Future Tracks

- Full external adapters
- Sidecar observer
- Event bus collector
- Enterprise collector
- Basic/foundation skill pack
- Write safety track
- Shell safety track
- Network safety track
- MCP safety track
- Plugin safety track

## Non-Goals

- No new executable skills.
- No external harness or script execution.
- No shell, network, workspace write, MCP, or plugin enablement.
- No canonical import of external candidates as executable skills.
- No memory, persona, or overlay mutation.
- No LLM calls.
- No JSONL canonical consolidation store.

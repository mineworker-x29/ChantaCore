# ChantaCore v0.19.7 Restore Notes

ChantaCore v0.19.7 defines Cross-Harness Trace Adapter Contracts.

This release maps supported external harness trace shapes into `AgentObservationNormalizedEventV2` records for the Agent Observation Spine. It registers adapter contracts and deterministic mapping rules for ChantaCore OCEL-like records, generic JSONL transcripts, and several explicit contract stubs.

Implemented read-only adapters:

- `GenericJSONLTranscriptAdapter`
- `ChantaCoreOCELAdapter`

Registered contract stubs:

- `SchumpeterAgentEventAdapter`
- `OpenCodeToolLifecycleAdapter`
- `ClaudeCodeTranscriptAdapter`
- `CodexTaskLogAdapter`
- `OpenClawGatewayLogAdapter`
- `HermesMissionLogAdapter`

The implemented paths only inspect provided files and normalize supported fixture records. Stub adapters return controlled findings when selected.

Boundary rules:

- No external harness execution.
- No live sidecar or event bus connection.
- No shell, network, write, MCP, or plugin capability is enabled.
- No raw private transcript export or full file body export is enabled.
- Observed relations do not make causal claims by default.

Future work:

- actual OpenCode, Claude Code, and Codex adapter implementations
- sidecar observer
- event bus collector
- Observation to Digestion adapter candidate builder

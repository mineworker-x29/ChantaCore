# ChantaCore v0.15.1 Restore Notes

Version name: ChantaCore v0.15.1 - Runtime Capability-aware Decision Surface

## Scope

v0.15.1 adds a runtime-derived capability decision surface for the Default Agent chat path.

The decision surface is a read-model and prompt guidance layer. It determines whether a user request maps to a capability that is available now, metadata-only, disabled, review-required, permission-required, not implemented, or unknown.

## Added Models

- `CapabilityRequestIntent`
- `CapabilityRequirement`
- `CapabilityDecision`
- `CapabilityDecisionSurface`
- `CapabilityDecisionEvidence`

These records are emitted to OCEL for observability.

## Deterministic Extraction

Requirement extraction is deterministic keyword/structure matching. It does not call an LLM classifier or reviewer.

Examples:

- ordinary chat and capability self-report -> `llm_chat`
- previous conversation references -> `session_context`
- Markdown, `<PERSONAL_DIRECTORY>/`, file read requests -> workspace/file read boundary
- PowerShell/bash/command execution -> shell boundary
- URL/API access -> network boundary
- MCP mentions -> MCP connection boundary
- plugin mentions -> plugin loading boundary
- external capability execution -> disabled/review-required external candidate boundary
- external OCEL import/merge -> metadata/review-required import candidate boundary

## Prompt Guidance

The Default Agent runtime now builds a capability decision surface for each user prompt and injects a concise guidance block into prompt context when bounded session context projection is active.

This guidance does not prevent the LLM call. It instructs the model to state limitations honestly instead of claiming unsupported capabilities.

## Boundaries

v0.15.1 does not add:

- ToolDispatcher active routing
- tool execution
- workspace file read
- shell execution
- network calls
- MCP connection
- plugin loading
- permission grant creation
- sandbox enforcement
- external candidate activation
- canonical JSONL capability decision store
- terminal scrollback source of truth

External capability candidates remain disabled or review-required. External OCEL import candidates remain metadata/review records only.

## OCEL Shape

Object types:

- `capability_request_intent`
- `capability_requirement`
- `capability_decision`
- `capability_decision_surface`
- `capability_decision_evidence`

Events:

- `capability_request_intent_created`
- `capability_requirement_recorded`
- `capability_decision_recorded`
- `capability_decision_surface_created`
- `capability_decision_evidence_recorded`
- `capability_limitation_detected`
- `capability_request_unfulfillable`

## PIG/OCPX

PIG reports include lightweight capability decision counts by availability category and unfulfillable/limitation event counts.

## Future Work

- explicit workspace read skills
- permission-aware capability routing
- reviewed capability activation
- capability-aware decision routing beyond prompt guidance

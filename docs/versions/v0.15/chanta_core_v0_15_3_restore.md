# ChantaCore v0.15.3 Restore Notes

## Target

ChantaCore v0.15.3 adds the Soul Identity / Persona Loading Foundation.

This version introduces persona identity records and bounded prompt projection for the Default Agent. It does not create an autonomous Soul runtime.

## Canonical Rule

Canonical persistence remains OCEL-based. Persona identity, profile, instruction artifact, binding, loadout, and projection records are represented as OCEL objects/events.

Markdown Personal Directory files are not canonical persona source in this version. No canonical JSONL persona store is introduced.

## Added Records

- `SoulIdentity`
- `PersonaProfile`
- `PersonaInstructionArtifact`
- `AgentRoleBinding`
- `PersonaLoadout`
- `PersonaProjection`

`PersonaLoadingService` can create the Default Agent persona profile and render a bounded persona projection block for prompt context.

## Default Agent Persona

The Default Agent persona states that it is a persona-loadable local LLM chat endpoint with OCEL provenance.

It also states:

- it is not an autonomous Soul runtime yet
- it has no ambient filesystem access
- workspace read exists only through explicit root-constrained read-only skills
- it has no shell, network, MCP, plugin, or runtime registry mutation capability in the default chat path
- capability boundaries override persona claims

## Prompt Projection

Persona projection is a bounded prompt read-model. It is attached before capability decision guidance when ChatService uses the default AgentRuntime prompt assembly path.

The intended prompt order is:

1. system prompt
2. persona projection
3. runtime capability / decision surface
4. bounded session context projection
5. current user message

Persona projection must not be treated as permission to execute tools or access unavailable capabilities.

## Explicit Non-goals

v0.15.3 does not add:

- autonomous Soul runtime lifecycle
- self-modifying persona
- hidden tool access
- shell execution
- network calls
- MCP connection
- plugin loading
- external capability activation
- permission auto-grants
- unbounded persona injection
- hidden reasoning output

## PIG/OCPX Reporting

PIG reports include lightweight persona counts:

- soul identity count
- persona profile count
- persona instruction artifact count
- agent role binding count
- persona loadout count
- persona projection count
- persona capability boundary count
- persona prompt attachment count

## Future Work

- Soul runtime lifecycle
- persona memory assimilation
- reviewed staged import for Soul/persona documents
- persona versioning and conformance checks

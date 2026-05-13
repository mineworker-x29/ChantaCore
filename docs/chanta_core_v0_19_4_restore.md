# ChantaCore v0.19.4 Restore Notes

ChantaCore v0.19.4 adds conformance and smoke validation for Observation/Digestion skills.

It validates the 10 seed skills across registry, onboarding, input and output contracts, risk profile, gate contract, envelope support, OCEL visibility, PIG/OCPX visibility, and audit/workbench visibility.

Smoke cases run only safe read-only Observation/Digestion paths through the existing gated invocation service. This release does not add new capabilities.

It does not execute external harnesses or external scripts. It does not enable write, shell, network, MCP, or plugin capabilities.

## Restore Checklist

- Verify package version `0.19.4`.
- Run Observation/Digestion conformance checks.
- Run safe read-only smoke cases with public fixtures.
- Confirm successful smoke invocations create execution envelopes.
- Confirm external candidates remain `pending_review`.
- Confirm `canonical_import_enabled=False` and `execution_enabled=False` remain external candidate defaults.
- Confirm no external harness, external script, write, shell, network, MCP, or plugin execution is enabled.

## Future Work

- v0.19.5 static digestion expansion.
- v0.19.6 full Agent Observation Spine & Movement Ontology.
- v0.19.7 cross-harness adapters.

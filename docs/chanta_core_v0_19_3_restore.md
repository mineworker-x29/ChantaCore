# ChantaCore v0.19.3 Restore Notes

ChantaCore v0.19.3 enables gated invocation for Observation/Digestion internal skills.

Observation converts agent or harness behavior into evidence-bearing OCEL-observable process state. Digestion converts observed behavior or external skill definitions into reviewable ChantaCore capability candidates.

This release executes only ChantaCore internal read-only observation and digestion service methods. It does not execute external harnesses or external scripts. It does not enable shell, network, write, MCP, or plugin capabilities.

All Observation/Digestion internal skill invocations must be explicit, pass the read-only gate, be wrapped in an execution envelope, and remain OCEL-observable.

External assimilation results remain candidates. `canonical_import_enabled=False` and `execution_enabled=False` remain the defaults for external candidates and adapter candidates.

## Restore Checklist

- Verify package version `0.19.3`.
- Confirm the 10 Observation/Digestion internal skill runtime bindings exist.
- Confirm default invocation policy allows only those 10 internal skill ids.
- Confirm successful invocations produce execution envelopes.
- Confirm blocked invocations record findings and do not execute.
- Confirm CLI output stays redacted and summary-oriented.
- Confirm no external harness, external script, shell, network, write, MCP, or plugin execution is enabled.

## Future Work

- v0.19.4 conformance/smoke.
- v0.19.6 full Agent Observation Spine & Movement Ontology.
- v0.19.7 cross-harness adapters.

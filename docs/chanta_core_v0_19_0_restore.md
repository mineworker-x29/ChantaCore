# ChantaCore v0.19.0 Restore Notes

ChantaCore v0.19.0 establishes the Observation and Digestion internal skill seed pack.

Observation converts agent or harness behavior into evidence-bearing OCEL-observable process state. The initial seed supports read-only source inspection, generic JSONL transcript observation, normalized observed events, deterministic behavior inference, and process narrative generation.

Digestion converts observed behavior or external skill definitions into reviewable ChantaCore capability candidates. The initial seed supports read-only external skill source inspection, static profile extraction, behavior fingerprinting, assimilation candidates, and adapter candidates.

External candidates are not executable by default. `canonical_import_enabled=False` by default. `execution_enabled=False` by default.

v0.19.0 does not execute external harnesses. It does not enable write, shell, network, MCP, or plugin execution. It does not promote external skills into executable canonical skills automatically.

The restore boundary for this version is review-first and read-only:

- Observation records OCEL-like objects, events, and best-effort relations.
- Digestion records reviewable candidates and adapters without granting permissions.
- Public summaries are redacted by default and do not store full raw source bodies.
- Generic JSONL input is an observation adapter, not a canonical observation store.

Future work:

- v0.19.1 registry view
- v0.19.2 proposal integration
- v0.19.6 full Agent Observation Spine & Movement Ontology
- v0.19.7 cross-harness adapters
- v0.19.8 observer hook/sidecar/event bus contracts

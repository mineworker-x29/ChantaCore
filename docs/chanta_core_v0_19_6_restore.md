# ChantaCore v0.19.6 Restore Notes

ChantaCore v0.19.6 establishes the Agent Observation Spine and Movement Ontology.

Observation is not just log summarization. This release defines generic identity, runtime context, movement ontology, object/effect/relation models, confidence/evidence/withdrawal conditions, review and correction models, redaction/export policies, and fleet snapshot aggregation.

Live sidecar and event bus collection are contract-only in this version and remain disabled by default.

No external harness execution is enabled. No write, shell, network, MCP, or plugin capability is enabled.

Future work:

- v0.19.7 cross-harness trace adapter contracts
- v0.19.8 Observation to Digestion adapter candidate builder
- v0.19.9 consolidation

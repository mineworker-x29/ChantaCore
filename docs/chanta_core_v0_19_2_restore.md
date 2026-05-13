# ChantaCore v0.19.2 Restore Notes

ChantaCore v0.19.2 adds Observation/Digestion Skill Proposal Integration.

Natural language can produce observation and digestion skill proposals. The proposal layer uses deterministic rule-based classification and maps matched intents to the read-only Observation/Digestion internal skill seed pack.

Proposal does not execute. It does not approve reviews, bridge proposals to execution, create permission grants, call an LLM, or activate shell, network, MCP, plugin, or write operations.

Missing inputs are shown in proposal bindings, proposal results, CLI summaries, and findings. Review is required for all generated proposals, and `execution_performed=false` remains part of the proposal set and result.

The proposal layer records OCEL-like objects, events, and best-effort relations for policies, intent candidates, bindings, proposal sets, findings, and results. It also contributes lightweight PIG/OCPX counts for observation/digestion proposal visibility.

Future work:

- v0.19.3 gated invocation integration
- v0.19.4 conformance/smoke
- v0.19.6 full Agent Observation Spine & Movement Ontology

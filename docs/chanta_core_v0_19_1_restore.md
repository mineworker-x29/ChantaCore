# ChantaCore v0.19.1 Restore Notes

ChantaCore v0.19.1 adds the Observation/Digestion Skill Registry View.

The registry view is read-only. It classifies skills by layer, origin, risk, and status, and renders reviewable metadata without running or enabling skills.

Observation and Digestion are the two ChantaCore-specific internal skill families. Observation converts agent or harness behavior into evidence-bearing OCEL-observable process state. Digestion converts observed behavior or external skill definitions into reviewable ChantaCore capability candidates.

External candidates remain `pending_review` and `execution_enabled=false`. The registry does not import external candidates as canonical executable skills.

The registry does not execute skills, enable skills, dynamically register tools, create permission grants, call an LLM, or enable shell, network, MCP, plugin, or write operations.

The registry records OCEL-like objects, events, and best-effort relations for views, entries, filters, findings, and results. It also contributes lightweight PIG/OCPX counts for registry visibility.

Future work:

- v0.19.2 observation-aware proposal integration
- v0.19.3 gated invocation integration
- v0.19.6 full Agent Observation Spine & Movement Ontology

# ChantaCore v0.19.5 Restore Notes

ChantaCore v0.19.5 expands static digestion for external skill sources.

The release inspects files and directories read-only, inventories scripts without executing them, parses manifests and bounded instruction previews, extracts declared capabilities, and infers static risks from generic public-safe source metadata.

Static digestion creates reviewable candidates only. `canonical_import_enabled=False` and `execution_enabled=False` remain the defaults for generated candidates and adapter hints.

No external harness, external script, shell, network, MCP, plugin, or write capability is enabled by this release.

Future work:

- v0.19.6 Agent Observation Spine & Movement Ontology
- v0.19.7 cross-harness trace adapter contracts
- v0.19.8 Observation to Digestion Adapter Candidate Builder

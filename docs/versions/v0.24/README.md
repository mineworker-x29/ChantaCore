# v0.24 Internal Provider / Local Runtime Provider

This folder stores v0.24.x records under the version-minor layout required by
the restore document policy.

Canonical v0.24.0 restore record:

- `chanta_core_v0_24_0_restore.md`
- `v0.24.1_provider_registry_capability_surface.md`
- `v0.24.2_read_only_workspace_provider.md`
- `v0.24.3_repository_search_file_read_provider.md`
- `v0.24.4_ocel_pig_ocpx_inspection_provider.md`
- `v0.24.5_local_runtime_command_candidate_provider.md`
- `v0.24.6_local_runtime_static_safety_preflight.md`
- `v0.24.7_gated_local_runtime_execution_boundary.md`
- `v0.24.8_local_runtime_output_failure_explanation.md`
- `v0.24.9_internal_provider_consolidation.md`

The former direct-path `docs/versions/v0.24.0_internal_provider_contract.md`
summary has been folded into the restore-grade record. Future v0.24.x version
documents should be added in this folder.

Restore interpretation:

- v0.24.0 is contract-only.
- v0.24.0 defines the Internal Provider Contract.
- v0.24.0 does not invoke providers, read workspace files as provider actions,
  search repositories as provider actions, execute local commands, implement
  external provider adapters, introduce Schumpeter split logic, expose
  credentials, or use an LLM judge.
- v0.24.1 declares the provider registry and capability surface.
- v0.24.2 activates the read-only workspace provider for tree and metadata observation only.
- v0.24.3 activates bounded repository search and bounded sanitized file read/excerpt providers.
- v0.24.4 activates bounded read-only OCEL/PIG/OCPX process-intelligence inspection providers.
- v0.24.5 activates inert local runtime command candidate creation only.
- v0.24.6 activates deterministic static safety and declared preflight without execution.
- v0.24.7 activates gated bounded local runtime execution through a single runner boundary.
- v0.24.8 interprets existing bounded/redacted local runtime output and explains failures without rerun or repair.
- v0.24.9 consolidates v0.24.0 through v0.24.8 as Internal Provider / Local Runtime Provider Foundation v1 and prepares v0.25 entry.

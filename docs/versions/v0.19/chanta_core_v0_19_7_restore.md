# ChantaCore v0.19.7 Restore Notes

ChantaCore v0.19.7 defines Cross-Harness Trace Adapter Contracts.

This release maps supported external harness trace shapes into `AgentObservationNormalizedEventV2` records for the Agent Observation Spine. It registers adapter contracts and deterministic mapping rules for ChantaCore OCEL-like records, generic JSONL transcripts, and several explicit contract stubs.

Implemented read-only adapters:

- `GenericJSONLTranscriptAdapter`
- `ChantaCoreOCELAdapter`

Registered contract stubs:

- `SchumpeterAgentEventAdapter`
- `OpenCodeToolLifecycleAdapter`
- `ClaudeCodeTranscriptAdapter`
- `CodexTaskLogAdapter`
- `OpenClawGatewayLogAdapter`
- `HermesMissionLogAdapter`

The implemented paths only inspect provided files and normalize supported fixture records. Stub adapters return controlled findings when selected.

Boundary rules:

- No external harness execution.
- No live sidecar or event bus connection.
- No shell, network, write, MCP, or plugin capability is enabled.
- No raw private transcript export or full file body export is enabled.
- Observed relations do not make causal claims by default.

Future work:

- actual OpenCode, Claude Code, and Codex adapter implementations
- sidecar observer
- event bus collector
- Observation to Digestion adapter candidate builder

## Restore-Grade Policy Addendum

### Restore Goal

Restore cross-harness trace adapter contracts that map supported trace shapes
into `AgentObservationNormalizedEventV2` records. Implemented adapters should
normalize public-safe fixture records only; unimplemented adapters should remain
contract stubs with controlled findings.

### Implemented Files

Primary implementation:

- `src/chanta_core/observation/adapter_contracts.py`
- `src/chanta_core/observation/adapters.py`
- `src/chanta_core/observation/spine.py`
- `src/chanta_core/observation/__init__.py`
- `src/chanta_core/cli/main.py`
- `src/chanta_core/pig/reports.py`

Tests:

- `tests/test_cross_harness_trace_adapter_models.py`
- `tests/test_cross_harness_trace_adapter_service.py`
- `tests/test_cross_harness_trace_adapter_cli.py`
- `tests/test_cross_harness_trace_adapter_history_adapter.py`
- `tests/test_cross_harness_trace_adapter_ocel_shape.py`
- `tests/test_cross_harness_trace_adapter_mapping.py`
- `tests/test_cross_harness_trace_adapter_coverage.py`
- `tests/test_cross_harness_trace_adapter_boundaries.py`

### Public API / Model Surface

Models:

- `CrossHarnessTraceAdapterPolicy`
- `HarnessTraceAdapterContract`
- `HarnessTraceSourceInspection`
- `HarnessTraceMappingRule`
- `HarnessTraceNormalizationPlan`
- `HarnessTraceNormalizationResult`
- `HarnessTraceAdapterCoverageReport`
- `HarnessTraceAdapterFinding`
- `HarnessTraceAdapterResult`

Service:

- `CrossHarnessTraceAdapterService`

Key service methods:

- `create_default_policy`
- `register_adapter_contracts`
- `register_default_mapping_rules`
- `inspect_trace_source`
- `select_adapter`
- `build_normalization_plan`
- `normalize_records`
- `normalize_generic_jsonl`
- `normalize_chantacore_ocel_like`
- `create_adapter_coverage_report`
- `normalize_file`
- `record_finding`
- `record_result`
- `render_adapter_cli`
- `render_mapping_rules_cli`
- `render_coverage_cli`

### Persistence and Canonical State

Adapter contracts and mapping rules are reviewable observation infrastructure.
They do not execute external harnesses, do not connect sidecars/event buses, and
do not create executable external adapters.

Stub adapters are registered to document expected future integrations. Selecting
a stub must return controlled findings rather than attempting execution.

### OCEL Shape

Object types:

- `cross_harness_trace_adapter_policy`
- `harness_trace_adapter_contract`
- `harness_trace_source_inspection`
- `harness_trace_mapping_rule`
- `harness_trace_normalization_plan`
- `harness_trace_normalization_result`
- `harness_trace_adapter_coverage_report`
- `harness_trace_adapter_finding`
- `harness_trace_adapter_result`

Events:

- `cross_harness_trace_adapter_policy_registered`
- `harness_trace_adapter_contract_registered`
- `harness_trace_source_inspected`
- `harness_trace_mapping_rule_registered`
- `harness_trace_normalization_plan_created`
- `harness_trace_normalization_result_recorded`
- `harness_trace_adapter_coverage_report_created`
- `harness_trace_adapter_finding_recorded`
- `harness_trace_adapter_result_recorded`

Expected relations:

- mapping rules belong to adapter contracts;
- inspection selects or references an adapter contract;
- normalization plan uses inspection and mapping rules;
- normalization result derives from plan and creates normalized event/object/relation refs;
- coverage report summarizes contract and mapping rules;
- findings belong to inspection, plan, or adapter result.

### CLI Surface

```powershell
chanta-cli observe adapters list
chanta-cli observe adapters show <adapter_name>
chanta-cli observe adapters inspect-source --root <root> --path <trace_file> --runtime <runtime_hint>
chanta-cli observe adapters plan --root <root> --path <trace_file> --runtime <runtime_hint>
chanta-cli observe adapters normalize --root <root> --path <trace_file> --runtime <runtime_hint>
chanta-cli observe adapters mapping-rules <adapter_name>
chanta-cli observe adapters coverage <adapter_name>
```

### Restore Procedure

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pytest tests\test_cross_harness_trace_adapter_models.py tests\test_cross_harness_trace_adapter_service.py tests\test_cross_harness_trace_adapter_cli.py tests\test_cross_harness_trace_adapter_history_adapter.py tests\test_cross_harness_trace_adapter_ocel_shape.py tests\test_cross_harness_trace_adapter_mapping.py tests\test_cross_harness_trace_adapter_coverage.py tests\test_cross_harness_trace_adapter_boundaries.py
.\.venv\Scripts\python.exe -m pytest
```

### Restore Checklist

- [ ] `GenericJSONLTranscriptAdapter` is implemented.
- [ ] `ChantaCoreOCELAdapter` is implemented.
- [ ] Schumpeter/OpenCode/Claude/Codex/OpenClaw/Hermes adapters remain stubs.
- [ ] Stub adapter selection returns controlled findings.
- [ ] Mapping rules are registered deterministically.
- [ ] Normalization creates `AgentObservationNormalizedEventV2` records for supported fixtures.
- [ ] Coverage reports distinguish implemented and stub adapters.
- [ ] Observed relations do not make causal claims by default.
- [ ] Boundary tests confirm no external harness execution, live sidecar/event bus connection, shell/network/write/MCP/plugin capability, raw private transcript export, or full file body export.

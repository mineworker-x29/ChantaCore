# ChantaCore v0.19.6 Restore Notes

ChantaCore v0.19.6 establishes the Agent Observation Spine and Movement Ontology.

Observation is not just log summarization. This release defines generic identity, runtime context, movement ontology, object/effect/relation models, confidence/evidence/withdrawal conditions, review and correction models, redaction/export policies, and fleet snapshot aggregation.

Live sidecar and event bus collection are contract-only in this version and remain disabled by default.

No external harness execution is enabled. No write, shell, network, MCP, or plugin capability is enabled.

Future work:

- v0.19.7 cross-harness trace adapter contracts
- v0.19.8 Observation to Digestion adapter candidate builder
- v0.19.9 consolidation

## Restore-Grade Policy Addendum

### Restore Goal

Restore the Agent Observation Spine and Movement Ontology. The spine should
provide generic, evidence-bearing models for agent identity, runtime context,
movement, objects, effects, relations, confidence, review, correction,
redaction, export, and fleet aggregation.

### Implemented Files

Primary implementation:

- `src/chanta_core/observation/ontology.py`
- `src/chanta_core/observation/policies.py`
- `src/chanta_core/observation/spine.py`
- `src/chanta_core/observation/__init__.py`
- `src/chanta_core/cli/main.py`
- `src/chanta_core/pig/reports.py`

Tests:

- `tests/test_agent_observation_spine_models.py`
- `tests/test_agent_observation_spine_service.py`
- `tests/test_agent_observation_spine_cli.py`
- `tests/test_agent_observation_spine_history_adapter.py`
- `tests/test_agent_observation_spine_ocel_shape.py`
- `tests/test_agent_observation_spine_ontology.py`
- `tests/test_agent_observation_spine_privacy_policy.py`
- `tests/test_agent_observation_spine_fleet.py`
- `tests/test_agent_observation_spine_boundaries.py`

### Public API / Model Surface

Models:

- `AgentInstance`
- `AgentRuntimeDescriptor`
- `RuntimeEnvironmentSnapshot`
- `AgentObservationSpinePolicy`
- `AgentObservationCollectorContract`
- `AgentObservationAdapterProfile`
- `AgentMovementOntologyTerm`
- `AgentObservationNormalizedEventV2`
- `ObservedAgentObject`
- `ObservedAgentRelation`
- `AgentBehaviorInferenceV2`
- `AgentObservationReview`
- `AgentObservationCorrection`
- `ObservationRedactionPolicy`
- `ObservationExportPolicy`
- `AgentFleetObservationSnapshot`
- `AgentObservationSpineFinding`
- `AgentObservationSpineResult`

Service:

- `AgentObservationSpineService`

### Persistence and Canonical State

The spine records observation models and contracts. It does not collect live
events by itself, does not connect to sidecars or event buses, and does not
execute external harnesses. Live collection surfaces are contract-only and
disabled by default.

Observation exports default to redacted summary-only mode. Full private
transcript export is not enabled by this release.

### OCEL Shape

Object types include:

- `agent_instance`
- `agent_runtime_descriptor`
- `runtime_environment_snapshot`
- `agent_observation_spine_policy`
- `agent_observation_collector_contract`
- `agent_observation_adapter_profile`
- `agent_movement_ontology_term`
- `agent_observation_normalized_event_v2`
- `observed_agent_object`
- `observed_agent_relation`
- `agent_behavior_inference_v2`
- `agent_observation_review`
- `agent_observation_correction`
- `observation_redaction_policy`
- `observation_export_policy`
- `agent_fleet_observation_snapshot`
- `agent_observation_spine_finding`
- `agent_observation_spine_result`

Events include registration, normalization, inference, review, correction,
policy creation, export policy creation, fleet snapshot creation, finding
recording, and result recording activities for those object families.

Expected relations connect runtime descriptors to agent instances, environment
snapshots to runtimes, normalized events to observed objects and relations,
inferences to event sets, corrections to reviews/events, and fleet snapshots to
aggregate observation sets.

### CLI Surface

```powershell
chanta-cli observe spine ontology
chanta-cli observe spine adapters
chanta-cli observe spine collectors
chanta-cli observe spine runtimes
chanta-cli observe spine redaction-policy
chanta-cli observe spine export-policy
chanta-cli observe spine fleet-snapshot
chanta-cli observe spine normalize --event-json-file event.json
chanta-cli observe spine infer --observed-run-json-file observed_run.json
```

### Restore Procedure

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pytest tests\test_agent_observation_spine_models.py tests\test_agent_observation_spine_service.py tests\test_agent_observation_spine_cli.py tests\test_agent_observation_spine_history_adapter.py tests\test_agent_observation_spine_ocel_shape.py tests\test_agent_observation_spine_ontology.py tests\test_agent_observation_spine_privacy_policy.py tests\test_agent_observation_spine_fleet.py tests\test_agent_observation_spine_boundaries.py
.\.venv\Scripts\python.exe -m pytest
```

### Restore Checklist

- [ ] Movement ontology terms register deterministically.
- [ ] Runtime descriptors and agent instances are generic and public-safe.
- [ ] Normalized V2 events include confidence/evidence/withdrawal metadata.
- [ ] Object/effect/relation models avoid default causal overclaims.
- [ ] Review and correction records are available.
- [ ] Redaction/export policies default to redacted summary-only output.
- [ ] Fleet snapshot aggregation records counts without private transcript export.
- [ ] Live sidecar/event bus collection remains disabled by default.
- [ ] Boundary tests confirm no external harness execution, shell/network/write/MCP/plugin capability, or raw private export.

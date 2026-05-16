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

## Restore-Grade Policy Addendum

### Restore Goal

Restore the first public, generic Observation/Digestion internal skill seed pack.
The restored system should be able to observe supplied traces and digest supplied
external skill definitions into reviewable OCEL-backed records without enabling
external execution.

### Implemented Files

Primary implementation:

- `src/chanta_core/observation_digest/models.py`
- `src/chanta_core/observation_digest/ids.py`
- `src/chanta_core/observation_digest/service.py`
- `src/chanta_core/observation_digest/history_adapter.py`
- `src/chanta_core/observation_digest/__init__.py`
- `src/chanta_core/skills/builtin/observation_digest.py`
- `src/chanta_core/skills/onboarding.py`
- `src/chanta_core/cli/main.py`
- `src/chanta_core/pig/reports.py`

Tests:

- `tests/test_observation_digest_models.py`
- `tests/test_observation_digest_service.py`
- `tests/test_observation_digest_cli.py`
- `tests/test_observation_digest_history_adapter.py`
- `tests/test_observation_digest_ocel_shape.py`
- `tests/test_observation_digest_boundaries.py`
- `tests/test_observation_digest_pig_report.py`
- `tests/test_external_skill_static_digest.py`

### Public API / Model Surface

Observation models:

- `AgentObservationSource`
- `AgentObservationBatch`
- `AgentObservationNormalizedEvent`
- `ObservedAgentRun`
- `AgentBehaviorInference`
- `AgentProcessNarrative`

Digestion models:

- `ExternalSkillSourceDescriptor`
- `ExternalSkillStaticProfile`
- `ExternalSkillBehaviorFingerprint`
- `ExternalSkillAssimilationCandidate`
- `ExternalSkillAdapterCandidate`
- `ObservationDigestionFinding`
- `ObservationDigestionResult`

Services:

- `ObservationService`
- `DigestionService`

Seed skill ids:

- `skill:agent_observation_source_inspect`
- `skill:agent_trace_observe`
- `skill:agent_observation_normalize`
- `skill:agent_behavior_infer`
- `skill:agent_process_narrative`
- `skill:external_skill_source_inspect`
- `skill:external_skill_static_digest`
- `skill:external_behavior_fingerprint`
- `skill:external_skill_assimilate`
- `skill:external_skill_adapter_candidate`

### Persistence and Canonical State

Observation/Digestion records are OCEL-observable review artifacts. Generic JSONL
input is an adapter input, not a canonical store. External skill profiles,
assimilation candidates, and adapter candidates remain review candidates.

Required invariants:

```text
canonical_import_enabled=False
execution_enabled=False
```

### OCEL Shape

Object types:

- `agent_observation_source`
- `agent_observation_batch`
- `agent_observation_normalized_event`
- `observed_agent_run`
- `agent_behavior_inference`
- `agent_process_narrative`
- `external_skill_source_descriptor`
- `external_skill_static_profile`
- `external_skill_behavior_fingerprint`
- `external_skill_assimilation_candidate`
- `external_skill_adapter_candidate`
- `observation_digestion_finding`
- `observation_digestion_result`

Events:

- `agent_observation_source_inspected`
- `agent_observation_batch_created`
- `agent_observation_event_normalized`
- `observed_agent_run_created`
- `agent_behavior_inference_created`
- `agent_process_narrative_created`
- `external_skill_source_inspected`
- `external_skill_static_profile_created`
- `external_skill_behavior_fingerprint_created`
- `external_skill_assimilation_candidate_created`
- `external_skill_adapter_candidate_created`
- `observation_digestion_finding_recorded`
- `observation_digestion_result_recorded`

Expected relations connect sources to batches, batches to normalized events,
events to observed runs, inferences and narratives to observed runs, static
profiles to source descriptors, fingerprints to observed runs, and candidates to
profiles/fingerprints.

### CLI Surface

Observation:

```powershell
chanta-cli observe source-inspect --root <root> --path <relative_path>
chanta-cli observe trace --root <root> --path <relative_path>
chanta-cli observe infer --observed-run-json-file observed_run.json
chanta-cli observe narrative --observed-run-json-file observed_run.json
```

Digestion:

```powershell
chanta-cli digest source-inspect --root <root> --path <relative_path>
chanta-cli digest static --root <root> --path <relative_path>
chanta-cli digest fingerprint --observed-run-json-file observed_run.json
chanta-cli digest assimilate --static-profile-json-file profile.json
chanta-cli digest adapter-candidate --candidate-json-file candidate.json
```

### Restore Procedure

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pytest tests\test_observation_digest_models.py tests\test_observation_digest_service.py tests\test_observation_digest_cli.py tests\test_observation_digest_history_adapter.py tests\test_observation_digest_ocel_shape.py tests\test_observation_digest_boundaries.py tests\test_observation_digest_pig_report.py tests\test_external_skill_static_digest.py
.\.venv\Scripts\python.exe -m pytest
```

### Restore Checklist

- [ ] The 10 seed skill ids are present as review-first internal skills.
- [ ] Observation source inspection is read-only and bounded.
- [ ] Generic JSONL traces normalize into observation records without becoming canonical state.
- [ ] Digestion produces static profiles, fingerprints, assimilation candidates, and adapter candidates only.
- [ ] External candidates keep `canonical_import_enabled=False`.
- [ ] External candidates keep `execution_enabled=False`.
- [ ] No external harness/script, write, shell, network, MCP, or plugin execution is enabled.
- [ ] OCEL objects/events/relations and ContextHistory adapters are present.
- [ ] PIG/OCPX report includes observation/digestion counts.

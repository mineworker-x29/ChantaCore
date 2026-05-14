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

## Restore-Grade Policy Addendum

### Restore Goal

Restore explicit, gated invocation for the 10 Observation/Digestion internal
read-only skills. Successful invocation must be wrapped in execution envelope
provenance and remain OCEL-observable.

### Implemented Files

Primary implementation:

- `src/chanta_core/skills/observation_digest_invocation.py`
- `src/chanta_core/observation_digest/service.py`
- `src/chanta_core/execution/envelope_service.py`
- `src/chanta_core/skills/onboarding.py`
- `src/chanta_core/cli/main.py`
- `src/chanta_core/pig/reports.py`

Tests:

- `tests/test_observation_digest_invocation_models.py`
- `tests/test_observation_digest_invocation_service.py`
- `tests/test_observation_digest_invocation_cli.py`
- `tests/test_observation_digest_invocation_history_adapter.py`
- `tests/test_observation_digest_invocation_ocel_shape.py`
- `tests/test_observation_digest_invocation_safe_paths.py`
- `tests/test_observation_digest_invocation_boundaries.py`

### Public API / Model Surface

Models:

- `ObservationDigestSkillRuntimeBinding`
- `ObservationDigestInvocationPolicy`
- `ObservationDigestInvocationFinding`
- `ObservationDigestInvocationResult`

Service:

- `ObservationDigestSkillInvocationService`

Key methods:

- `create_default_policy`
- `create_runtime_bindings`
- `resolve_binding`
- `validate_invocation_input`
- `gate_invocation`
- `invoke_observation_skill`
- `invoke_digestion_skill`
- `invoke_skill`
- `wrap_result_in_envelope`
- `render_invocation_cli`

### Persistence and Canonical State

Invocation results are OCEL-observable execution records. External digestion
outputs remain candidates unless later reviewed workflows explicitly handle
them. Candidate defaults remain:

```text
canonical_import_enabled=False
execution_enabled=False
```

### OCEL Shape

Object types:

- `observation_digest_skill_runtime_binding`
- `observation_digest_invocation_policy`
- `observation_digest_invocation_finding`
- `observation_digest_invocation_result`

Events:

- `observation_digest_skill_runtime_binding_registered`
- `observation_digest_invocation_policy_registered`
- `observation_digest_invocation_requested`
- `observation_digest_invocation_finding_recorded`
- `observation_digest_invocation_blocked`
- `observation_digest_invocation_completed`
- `observation_digest_invocation_failed`
- `observation_digest_invocation_result_recorded`

Expected relations:

- invocation result references runtime binding and skill id;
- findings belong to invocation result or requested skill;
- completed invocations reference output object ids from observation/digestion services;
- envelope records reference invocation result ids when wrapping is enabled.

### CLI Surface

```powershell
chanta-cli observe run source-inspect --root <root> --path trace.jsonl
chanta-cli observe run trace --root <root> --path trace.jsonl
chanta-cli observe run normalize --records-json-file records.json
chanta-cli observe run infer --observed-run-json-file observed_run.json
chanta-cli observe run narrative --observed-run-json-file observed_run.json
chanta-cli digest run source-inspect --root <root> --path SKILL.md
chanta-cli digest run static --root <root> --path SKILL.md
chanta-cli digest run fingerprint --observed-run-json-file observed_run.json
chanta-cli digest run assimilate --static-profile-json-file profile.json
chanta-cli digest run adapter-candidate --candidate-json-file candidate.json
```

### Restore Procedure

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pytest tests\test_observation_digest_invocation_models.py tests\test_observation_digest_invocation_service.py tests\test_observation_digest_invocation_cli.py tests\test_observation_digest_invocation_history_adapter.py tests\test_observation_digest_invocation_ocel_shape.py tests\test_observation_digest_invocation_safe_paths.py tests\test_observation_digest_invocation_boundaries.py
.\.venv\Scripts\python.exe -m pytest
```

### Restore Checklist

- [ ] All 10 runtime bindings exist.
- [ ] Default policy allows only the 10 Observation/Digestion internal skill ids.
- [ ] Missing required inputs block invocation.
- [ ] Workspace path traversal and outside-root reads are blocked.
- [ ] Successful invocations create execution envelopes when wrapping is enabled.
- [ ] Blocked invocations record findings and do not execute service methods.
- [ ] External candidates remain non-executable review candidates.
- [ ] Boundary tests confirm no external harness/script, shell, network, write, MCP, plugin, or permission grant.

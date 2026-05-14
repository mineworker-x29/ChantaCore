# ChantaCore v0.19.4 Restore Notes

ChantaCore v0.19.4 adds conformance and smoke validation for Observation/Digestion skills.

It validates the 10 seed skills across registry, onboarding, input and output contracts, risk profile, gate contract, envelope support, OCEL visibility, PIG/OCPX visibility, and audit/workbench visibility.

Smoke cases run only safe read-only Observation/Digestion paths through the existing gated invocation service. This release does not add new capabilities.

It does not execute external harnesses or external scripts. It does not enable write, shell, network, MCP, or plugin capabilities.

## Restore Checklist

- Verify package version `0.19.4`.
- Run Observation/Digestion conformance checks.
- Run safe read-only smoke cases with public fixtures.
- Confirm successful smoke invocations create execution envelopes.
- Confirm external candidates remain `pending_review`.
- Confirm `canonical_import_enabled=False` and `execution_enabled=False` remain external candidate defaults.
- Confirm no external harness, external script, write, shell, network, MCP, or plugin execution is enabled.

## Future Work

- v0.19.5 static digestion expansion.
- v0.19.6 full Agent Observation Spine & Movement Ontology.
- v0.19.7 cross-harness adapters.

## Restore-Grade Policy Addendum

### Restore Goal

Restore static conformance and safe smoke validation for the 10
Observation/Digestion seed skills. Conformance validates contracts and smoke
cases exercise only public-safe read-only paths.

### Implemented Files

Primary implementation:

- `src/chanta_core/skills/observation_digest_conformance.py`
- `src/chanta_core/skills/observation_digest_invocation.py`
- `src/chanta_core/skills/onboarding.py`
- `src/chanta_core/cli/main.py`
- `src/chanta_core/pig/reports.py`

Tests:

- `tests/test_observation_digest_conformance_models.py`
- `tests/test_observation_digest_conformance_service.py`
- `tests/test_observation_digest_conformance_cli.py`
- `tests/test_observation_digest_conformance_history_adapter.py`
- `tests/test_observation_digest_conformance_ocel_shape.py`
- `tests/test_observation_digest_conformance_smoke.py`
- `tests/test_observation_digest_conformance_boundaries.py`

### Public API / Model Surface

Models:

- `ObservationDigestConformancePolicy`
- `ObservationDigestConformanceCheck`
- `ObservationDigestSmokeCase`
- `ObservationDigestSmokeResult`
- `ObservationDigestConformanceFinding`
- `ObservationDigestConformanceResult`

Service:

- `ObservationDigestConformanceService`

The service checks registry, onboarding, input/output contracts, risk profile,
gate contract, envelope support, OCEL visibility, PIG/OCPX visibility, audit
visibility, and workbench visibility.

### Persistence and Canonical State

Conformance and smoke records are diagnostic. They do not enable skills, approve
reviews, create permission grants, or promote candidates. Smoke cases use public
fixtures and must remain read-only.

### OCEL Shape

Object types:

- `observation_digest_conformance_policy`
- `observation_digest_conformance_check`
- `observation_digest_smoke_case`
- `observation_digest_smoke_result`
- `observation_digest_conformance_finding`
- `observation_digest_conformance_result`

Events:

- `observation_digest_conformance_policy_registered`
- `observation_digest_conformance_check_recorded`
- `observation_digest_smoke_case_recorded`
- `observation_digest_smoke_result_recorded`
- `observation_digest_conformance_finding_recorded`
- `observation_digest_conformance_result_recorded`

Expected relations:

- checks belong to policy and target skill ids;
- smoke results belong to smoke cases;
- findings belong to checks, smoke cases, or target skill ids;
- conformance result summarizes checks, smoke results, and findings.

### CLI Surface

```powershell
chanta-cli observe-digest conformance run
chanta-cli observe-digest conformance smoke
chanta-cli observe-digest conformance report
chanta-cli observe-digest conformance check-skill --skill-id <skill_id>
chanta-cli observe-digest conformance findings
```

### Restore Procedure

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pytest tests\test_observation_digest_conformance_models.py tests\test_observation_digest_conformance_service.py tests\test_observation_digest_conformance_cli.py tests\test_observation_digest_conformance_history_adapter.py tests\test_observation_digest_conformance_ocel_shape.py tests\test_observation_digest_conformance_smoke.py tests\test_observation_digest_conformance_boundaries.py
.\.venv\Scripts\python.exe -m pytest
```

### Restore Checklist

- [ ] All 10 seed skills have conformance checks.
- [ ] Registry/onboarding/input/output/risk/gate/envelope/OCEL/PIG/audit/workbench visibility are checked.
- [ ] Safe smoke cases run through the gated invocation service.
- [ ] Smoke output creates execution envelopes for successful safe cases.
- [ ] External candidates remain `pending_review`.
- [ ] `canonical_import_enabled=False` and `execution_enabled=False` remain defaults for external candidates.
- [ ] Boundary tests confirm no external harness/script, write, shell, network, MCP, plugin, or permission grant.

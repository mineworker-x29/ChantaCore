# ChantaCore v0.18.6 Restore Notes

Version name: ChantaCore v0.18.6 - Internal Skill Onboarding Contract

## Scope

Internal Skill Onboarding defines the contract for future internal skills. It is a diagnostic and conformance layer for describing a capability before it can be treated as a proper internal skill.

A skill is not fully integrated unless it has all of these contracts:

- Skill Descriptor
- Skill Input Contract
- Skill Output Contract
- Skill Risk Profile
- Skill Gate Contract
- Skill Observability Contract

## Mandatory Contract Rules

- OCEL observability is mandatory.
- Execution envelope support is mandatory.
- PIG/OCPX visibility is mandatory.
- Audit visibility and workbench visibility must be declared.
- Accepted onboarding results remain disabled by default.

## Boundaries

- v0.18.6 does not execute skills during onboarding.
- v0.18.6 does not enable write, shell, network, MCP, or plugin skills.
- v0.18.6 does not dynamically register executable tools.
- v0.18.6 does not create permission grants.
- v0.18.6 does not mutate ToolDispatcher or SkillExecutor dynamically.

## CLI

The diagnostic CLI surface is:

- `chanta-cli skills onboarding list`
- `chanta-cli skills onboarding show <skill_id>`
- `chanta-cli skills onboarding check --skill-id <skill_id>`
- `chanta-cli skills onboarding validate --descriptor-json-file <path>`

These commands inspect descriptors and validate onboarding contracts. They do not execute skills, register runtime tools, or grant permissions.

## Future Work

- v0.19.0 read-only internal skill pack.
- Internal skill registry view.
- Skill conformance and smoke tests.

No private content is included in this public restore note.

## Restore-Grade Policy Addendum

### Implemented Files

Primary implementation:

- `src/chanta_core/skills/onboarding.py`
- `src/chanta_core/skills/ids.py`
- `src/chanta_core/skills/history_adapter.py`
- `src/chanta_core/skills/__init__.py`
- `src/chanta_core/cli/main.py`
- `src/chanta_core/pig/reports.py`

Tests:

- `tests/test_internal_skill_onboarding_models.py`
- `tests/test_internal_skill_onboarding_service.py`
- `tests/test_internal_skill_onboarding_cli.py`
- `tests/test_internal_skill_onboarding_history_adapter.py`
- `tests/test_internal_skill_onboarding_ocel_shape.py`
- `tests/test_internal_skill_onboarding_boundaries.py`

### Public API / Model Surface

Models:

- `InternalSkillDescriptor`
- `InternalSkillInputContract`
- `InternalSkillOutputContract`
- `InternalSkillRiskProfile`
- `InternalSkillGateContract`
- `InternalSkillObservabilityContract`
- `InternalSkillOnboardingReview`
- `InternalSkillOnboardingFinding`
- `InternalSkillOnboardingResult`

Service:

- `InternalSkillOnboardingService`

Key service methods:

- `create_descriptor`
- `create_input_contract`
- `create_output_contract`
- `create_risk_profile`
- `create_gate_contract`
- `create_observability_contract`
- `validate_onboarding`
- `record_review`
- `record_finding`
- `record_result`
- `create_read_only_skill_contract_bundle`
- `default_read_only_descriptor_candidates`
- `render_onboarding_summary`

### Persistence and Canonical State

Onboarding records are diagnostic and contractual. Accepted onboarding results
remain disabled by default and do not dynamically register executable tools.

Required invariant:

```text
enabled=false
```

Onboarding does not mutate `ToolDispatcher`, `SkillExecutor`, runtime
capabilities, permission grants, or plugin registries.

### OCEL Shape

Object types:

- `internal_skill_descriptor`
- `internal_skill_input_contract`
- `internal_skill_output_contract`
- `internal_skill_risk_profile`
- `internal_skill_gate_contract`
- `internal_skill_observability_contract`
- `internal_skill_onboarding_review`
- `internal_skill_onboarding_finding`
- `internal_skill_onboarding_result`

Events:

- `internal_skill_descriptor_registered`
- `internal_skill_input_contract_registered`
- `internal_skill_output_contract_registered`
- `internal_skill_risk_profile_registered`
- `internal_skill_gate_contract_registered`
- `internal_skill_observability_contract_registered`
- `internal_skill_onboarding_review_recorded`
- `internal_skill_onboarding_finding_recorded`
- `internal_skill_onboarding_result_recorded`

Expected relations:

- contracts belong to the descriptor;
- review targets descriptor;
- findings target descriptor or a missing contract;
- result summarizes descriptor, review, and findings.

### CLI Surface

```powershell
chanta-cli skills onboarding list
chanta-cli skills onboarding show <skill_id>
chanta-cli skills onboarding check --skill-id <skill_id>
chanta-cli skills onboarding validate --descriptor-json-file descriptor.json
```

These commands inspect descriptors and validate contracts. They do not execute
skills or register runtime tools.

### Restore Procedure

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pytest tests\test_internal_skill_onboarding_models.py tests\test_internal_skill_onboarding_service.py tests\test_internal_skill_onboarding_cli.py tests\test_internal_skill_onboarding_history_adapter.py tests\test_internal_skill_onboarding_ocel_shape.py tests\test_internal_skill_onboarding_boundaries.py
.\.venv\Scripts\python.exe -m pytest
```

### Restore Checklist

- [ ] Descriptor, input, output, risk, gate, and observability contracts exist.
- [ ] Missing OCEL, envelope, PIG/OCPX, audit, or workbench visibility creates findings.
- [ ] Accepted onboarding results still render `enabled=false`.
- [ ] CLI list/show/check/validate paths are read-only diagnostics.
- [ ] OCEL onboarding objects/events/relations are recorded.
- [ ] ContextHistory adapter entries are generated.
- [ ] Boundary tests confirm no dynamic tool registration, permission grants, or shell/network/write/MCP/plugin capability.

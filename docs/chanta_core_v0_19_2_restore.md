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

## Restore-Grade Policy Addendum

### Restore Goal

Restore deterministic proposal integration for Observation/Digestion internal
skills. User text may create reviewable proposals, but proposal creation must
not execute any skill.

### Implemented Files

Primary implementation:

- `src/chanta_core/skills/observation_digest_proposal.py`
- `src/chanta_core/skills/proposal.py`
- `src/chanta_core/skills/registry_view.py`
- `src/chanta_core/skills/history_adapter.py`
- `src/chanta_core/skills/__init__.py`
- `src/chanta_core/cli/main.py`
- `src/chanta_core/pig/reports.py`

Tests:

- `tests/test_observation_digest_proposal_models.py`
- `tests/test_observation_digest_proposal_service.py`
- `tests/test_observation_digest_proposal_cli.py`
- `tests/test_observation_digest_proposal_history_adapter.py`
- `tests/test_observation_digest_proposal_ocel_shape.py`
- `tests/test_observation_digest_proposal_boundaries.py`

### Public API / Model Surface

Models:

- `ObservationDigestProposalPolicy`
- `ObservationDigestIntentCandidate`
- `ObservationDigestProposalBinding`
- `ObservationDigestProposalSet`
- `ObservationDigestProposalFinding`
- `ObservationDigestProposalResult`

Service:

- `ObservationDigestProposalService`

The service deterministically maps prompt intent to the 10 Observation/Digestion
seed skill ids and records missing inputs.

### Persistence and Canonical State

Proposal records are review inputs only. They do not execute, approve, bridge,
grant permission, or create canonical observation/digestion state.

Required invariant:

```text
execution_performed=false
```

### OCEL Shape

Object types:

- `observation_digest_proposal_policy`
- `observation_digest_intent_candidate`
- `observation_digest_proposal_binding`
- `observation_digest_proposal_set`
- `observation_digest_proposal_finding`
- `observation_digest_proposal_result`

Events:

- `observation_digest_proposal_policy_registered`
- `observation_digest_intent_candidate_created`
- `observation_digest_proposal_binding_created`
- `observation_digest_proposal_set_created`
- `observation_digest_proposal_finding_recorded`
- `observation_digest_proposal_result_recorded`

Expected relations:

- binding belongs to intent;
- proposal set includes intent candidates and bindings;
- finding belongs to proposal set or binding;
- result summarizes proposal set.

### CLI Surface

```powershell
chanta-cli observe propose "observe this trace" --root <root> --path trace.jsonl
chanta-cli digest propose "digest this external skill" --root <root> --path SKILL.md
chanta-cli skills propose observation-digestion "infer agent behavior"
```

The CLI prints proposal summaries and missing input diagnostics. It must not run
the proposed skill.

### Restore Procedure

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pytest tests\test_observation_digest_proposal_models.py tests\test_observation_digest_proposal_service.py tests\test_observation_digest_proposal_cli.py tests\test_observation_digest_proposal_history_adapter.py tests\test_observation_digest_proposal_ocel_shape.py tests\test_observation_digest_proposal_boundaries.py
.\.venv\Scripts\python.exe -m pytest
```

### Restore Checklist

- [ ] Deterministic classifier maps observation prompts to observation skill ids.
- [ ] Deterministic classifier maps digestion prompts to digestion skill ids.
- [ ] Missing inputs are recorded in bindings, findings, and CLI output.
- [ ] All proposals require review.
- [ ] `execution_performed=false` is preserved.
- [ ] OCEL proposal objects/events/relations are recorded.
- [ ] ContextHistory adapter entries are generated.
- [ ] Boundary tests confirm no LLM classifier, execution, approval, bridge, permission grant, shell/network/write/MCP/plugin capability, or private content.

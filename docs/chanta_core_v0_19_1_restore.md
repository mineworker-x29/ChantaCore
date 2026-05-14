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

## Restore-Grade Policy Addendum

### Restore Goal

Restore the read-only registry view for Observation/Digestion internal skills and
external candidates. The registry should classify skill metadata without running
or enabling any skill.

### Implemented Files

Primary implementation:

- `src/chanta_core/skills/registry_view.py`
- `src/chanta_core/skills/registry.py`
- `src/chanta_core/skills/history_adapter.py`
- `src/chanta_core/skills/__init__.py`
- `src/chanta_core/cli/main.py`
- `src/chanta_core/pig/reports.py`

Tests:

- `tests/test_skill_registry_view_models.py`
- `tests/test_skill_registry_view_service.py`
- `tests/test_skill_registry_view_cli.py`
- `tests/test_skill_registry_view_history_adapter.py`
- `tests/test_skill_registry_view_ocel_shape.py`
- `tests/test_skill_registry_view_boundaries.py`
- `tests/test_skill_registry.py`

### Public API / Model Surface

Models:

- `SkillRegistryView`
- `SkillRegistryEntry`
- `SkillRegistryFilter`
- `SkillRegistryFinding`
- `SkillRegistryResult`

Service:

- `SkillRegistryViewService`

The view classifies entries by layer, origin, risk class, status, supported
execution state, and contract completeness.

### Persistence and Canonical State

The registry view is a read-only projection. It can record registry view,
entry, filter, finding, and result objects, but it must not enable skills,
import candidates, create permission grants, call LLMs, or dynamically register
tools.

External candidates remain review records with:

```text
execution_enabled=false
canonical_import_enabled=False
```

### OCEL Shape

Object types:

- `skill_registry_view`
- `skill_registry_entry`
- `skill_registry_filter`
- `skill_registry_finding`
- `skill_registry_result`

Events:

- `skill_registry_view_created`
- `skill_registry_entry_recorded`
- `skill_registry_filter_recorded`
- `skill_registry_finding_recorded`
- `skill_registry_result_recorded`
- `skill_registry_rendered`

Expected relations:

- entry belongs to registry view;
- filter applies to registry view;
- finding belongs to entry or registry view;
- result summarizes registry view and filter.

### CLI Surface

```powershell
chanta-cli skills registry list
chanta-cli skills registry show <skill_id>
chanta-cli skills registry observation
chanta-cli skills registry digestion
chanta-cli skills registry external-candidates
chanta-cli skills registry risk
chanta-cli skills registry observability
chanta-cli skills registry findings
```

Filters include layer/origin/risk/status/execution-enabled controls where
available. Output is summary-oriented and public-safe.

### Restore Procedure

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pytest tests\test_skill_registry_view_models.py tests\test_skill_registry_view_service.py tests\test_skill_registry_view_cli.py tests\test_skill_registry_view_history_adapter.py tests\test_skill_registry_view_ocel_shape.py tests\test_skill_registry_view_boundaries.py tests\test_skill_registry.py
.\.venv\Scripts\python.exe -m pytest
```

### Restore Checklist

- [ ] Observation and digestion seed skills appear in the registry.
- [ ] External candidates appear as candidates, not enabled executable skills.
- [ ] Missing contract findings are recorded.
- [ ] Registry filters do not execute or enable skills.
- [ ] OCEL registry view objects/events/relations are recorded.
- [ ] ContextHistory adapter entries are generated.
- [ ] PIG/OCPX registry counts are present.
- [ ] Boundary tests confirm no tool registration, permission grants, shell/network/write/MCP/plugin execution, or private content.

# ChantaCore v0.19.5 Restore Notes

ChantaCore v0.19.5 expands static digestion for external skill sources.

The release inspects files and directories read-only, inventories scripts without executing them, parses manifests and bounded instruction previews, extracts declared capabilities, and infers static risks from generic public-safe source metadata.

Static digestion creates reviewable candidates only. `canonical_import_enabled=False` and `execution_enabled=False` remain the defaults for generated candidates and adapter hints.

No external harness, external script, shell, network, MCP, plugin, or write capability is enabled by this release.

Future work:

- v0.19.6 Agent Observation Spine & Movement Ontology
- v0.19.7 cross-harness trace adapter contracts
- v0.19.8 Observation to Digestion Adapter Candidate Builder

## Restore-Grade Policy Addendum

### Restore Goal

Restore expanded static digestion for external skill sources. The restored
system should inspect external skill directories and files read-only, inventory
resources, parse manifests and bounded instructions, infer static risks, and
create reviewable profiles/candidates without executing external code.

### Implemented Files

Primary implementation:

- `src/chanta_core/digestion/static_expansion.py`
- `src/chanta_core/digestion/__init__.py`
- `src/chanta_core/observation_digest/service.py`
- `src/chanta_core/observation_digest/models.py`
- `src/chanta_core/cli/main.py`
- `src/chanta_core/pig/reports.py`

Tests:

- `tests/test_external_skill_static_digestion_models.py`
- `tests/test_external_skill_static_digestion_service.py`
- `tests/test_external_skill_static_digestion_cli.py`
- `tests/test_external_skill_static_digestion_history_adapter.py`
- `tests/test_external_skill_static_digestion_ocel_shape.py`
- `tests/test_external_skill_static_digestion_risk.py`
- `tests/test_external_skill_static_digestion_boundaries.py`
- `tests/test_external_skill_static_digest.py`

### Public API / Model Surface

Models:

- `ExternalSkillResourceInventory`
- `ExternalSkillManifestProfile`
- `ExternalSkillInstructionProfile`
- `ExternalSkillDeclaredCapability`
- `ExternalSkillStaticRiskProfile`
- `ExternalSkillStaticDigestionReport`
- `ExternalSkillStaticDigestionFinding`

Service:

- `ExternalSkillStaticDigestionService`

Key service methods:

- `inspect_resource_inventory`
- `parse_skill_md_frontmatter`
- `parse_generic_manifest`
- `parse_instruction_profile`
- `extract_declared_capabilities`
- `infer_static_risk_profile`
- `create_static_digestion_report`
- `create_static_profile_from_report`
- `create_assimilation_candidate_from_report`
- `create_adapter_hints_from_report`
- `render_static_digestion_cli`

### Persistence and Canonical State

Static digestion records source metadata, bounded previews, hashes, static risk
classifications, and reviewable candidates. It must not execute scripts, import
packages, install dependencies, call external services, or create executable
skills.

Required invariants:

```text
canonical_import_enabled=False
execution_enabled=False
```

### OCEL Shape

Object types:

- `external_skill_resource_inventory`
- `external_skill_manifest_profile`
- `external_skill_instruction_profile`
- `external_skill_declared_capability`
- `external_skill_static_risk_profile`
- `external_skill_static_digestion_report`
- `external_skill_static_digestion_finding`

Events:

- `external_skill_resource_inventory_created`
- `external_skill_manifest_profile_created`
- `external_skill_instruction_profile_created`
- `external_skill_declared_capability_recorded`
- `external_skill_static_risk_profile_created`
- `external_skill_static_digestion_report_created`
- `external_skill_static_digestion_finding_recorded`

Expected relations:

- manifest and instruction profiles belong to the resource inventory;
- declared capabilities and risk profiles derive from manifest/instruction
  profiles;
- static digestion report summarizes inventory, profiles, capabilities, risks,
  and findings;
- generated assimilation/adapter candidates remain review candidates.

### CLI Surface

```powershell
chanta-cli digest source-inspect --root <root> --path <relative_path>
chanta-cli digest inventory --root <root> --path <relative_path>
chanta-cli digest static --root <root> --path <relative_path>
chanta-cli digest risk --root <root> --path <relative_path>
chanta-cli digest report --root <root> --path <relative_path>
```

The CLI inspects files and directories read-only. It must reject traversal and
outside-root paths through the existing safe path handling.

### Restore Procedure

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pytest tests\test_external_skill_static_digestion_models.py tests\test_external_skill_static_digestion_service.py tests\test_external_skill_static_digestion_cli.py tests\test_external_skill_static_digestion_history_adapter.py tests\test_external_skill_static_digestion_ocel_shape.py tests\test_external_skill_static_digestion_risk.py tests\test_external_skill_static_digestion_boundaries.py tests\test_external_skill_static_digest.py
.\.venv\Scripts\python.exe -m pytest
```

### Restore Checklist

- [ ] Resource inventory classifies markdown, manifest, script, reference, and asset files.
- [ ] Scripts are inventoried but not executed.
- [ ] Manifest and instruction previews are bounded.
- [ ] Static risk detects shell/network/write/MCP/plugin-like capability declarations.
- [ ] Static profiles, assimilation candidates, and adapter hints remain review-only.
- [ ] `canonical_import_enabled=False` and `execution_enabled=False` are preserved.
- [ ] OCEL static digestion objects/events/relations are recorded.
- [ ] Boundary tests confirm no external execution, write, shell, network, MCP, plugin, dependency install, or private content export.

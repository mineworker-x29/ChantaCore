# ChantaCore v0.16.2 Restore Notes

Version name: ChantaCore v0.16.2 - Personal Core Profile & Mode Loadouts

This document is a restore-grade record of the v0.16.2 implementation. It is not canonical runtime state. Personal mode loadouts are design-time, OCEL-traceable artifacts and do not activate runtime modes by themselves.

## Restore Goal

v0.16.2 adds a generic Personal Core Profile and Personal Mode Loadout framework.

The restoration target is a public, generic framework where a user can represent:

- one Personal Core Profile;
- multiple Personal Mode Profiles;
- mode-specific boundaries;
- mode-specific capability binding metadata;
- bounded Personal Mode Loadouts;
- draft loadouts that remain pending review.

This version does not implement runtime mode selection. Runtime binding and selector policy are future work.

## Implemented Files

Core implementation:

- `src/chanta_core/persona/personal_mode_loadout.py`
- `src/chanta_core/persona/ids.py`
- `src/chanta_core/persona/errors.py`
- `src/chanta_core/persona/history_adapter.py`
- `src/chanta_core/persona/__init__.py`
- `src/chanta_core/pig/reports.py`

Version marker:

- `pyproject.toml`
- `src/chanta_core/__init__.py`

Restore document:

- `docs/versions/v0.16/chanta_core_v0_16_2_restore.md`

Tests:

- `tests/test_personal_mode_loadout_models.py`
- `tests/test_personal_mode_loadout_service.py`
- `tests/test_personal_mode_loadout_history_adapter.py`
- `tests/test_personal_mode_loadout_ocel_shape.py`
- `tests/test_personal_mode_loadout_boundaries.py`
- `tests/test_imports.py`
- `tests/test_pig_reports.py`

## Public Concepts

`PersonalCoreProfile`

- Represents the generic core identity/profile record for a personal assistant or workflow profile.
- It stores profile name, type, identity statement, optional continuity statement, status, privacy flag, timestamps, and attrs.
- It does not grant capabilities.

`PersonalModeProfile`

- Represents a mode-specific role and operating context.
- It stores mode name, mode type, role statement, operating context, capability summary, limitation summary, status, privacy flag, timestamps, and attrs.
- It belongs to a Personal Core Profile.

`PersonalModeBoundary`

- Represents a mode-specific boundary.
- Supported boundary categories include capability, runtime, privacy, source, tool, memory, safety, mode separation, manual, and other.
- Boundaries are prompt/design metadata, not permission grants.

`PersonalModeCapabilityBinding`

- Represents capability truth metadata for a mode.
- It records capability name, category, availability, execution status, permission requirement, review requirement, and optional source reference.
- It does not create a permission grant.

`PersonalModeLoadout`

- Represents a bounded prompt-ready loadout built from core profile, mode profile, boundaries, capability bindings, projection refs, and source candidate refs.
- It contains identity, role, capability boundary, safety boundary, and optional privacy boundary blocks.
- It includes the statement:

```text
Runtime capability profile overrides personal/persona claims.
```

`PersonalModeLoadoutDraft`

- Represents a review draft.
- It records projected blocks, source refs, unresolved questions, review status, privacy flag, and attrs.
- It always sets:

```text
canonical_activation_enabled=False
```

## Service Surface

`PersonalModeLoadoutService` supports:

- `register_core_profile`
- `register_mode_profile`
- `register_mode_boundary`
- `register_capability_binding`
- `create_mode_loadout`
- `create_mode_loadout_draft`
- `create_multi_mode_loadout_set`
- `render_mode_loadout_block`

Expected restoration behavior:

- core profile registration records an OCEL object/event;
- mode profile registration links the mode to the core profile;
- boundaries link to mode profiles;
- capability bindings link to mode profiles;
- loadouts link to core profile, mode profile, and capability bindings;
- drafts are created as pending review;
- `create_multi_mode_loadout_set` uses caller-supplied generic specs only;
- rendering is bounded and includes capability truth language.

## Model Field Summary

Core profile fields:

- `core_profile_id`
- `profile_name`
- `profile_type`
- `description`
- `identity_statement`
- `continuity_statement`
- `status`
- `private`
- `created_at`
- `updated_at`
- `profile_attrs`

Mode profile fields:

- `mode_profile_id`
- `core_profile_id`
- `mode_name`
- `mode_type`
- `role_statement`
- `operating_context`
- `capability_summary`
- `limitation_summary`
- `status`
- `private`
- `created_at`
- `updated_at`
- `mode_attrs`

Boundary fields:

- `boundary_id`
- `mode_profile_id`
- `boundary_type`
- `boundary_text`
- `severity`
- `required`
- `status`
- `created_at`
- `boundary_attrs`

Capability binding fields:

- `binding_id`
- `mode_profile_id`
- `capability_name`
- `capability_category`
- `availability`
- `can_execute_now`
- `requires_permission`
- `requires_review`
- `source_kind`
- `source_ref`
- `created_at`
- `binding_attrs`

Loadout fields:

- `loadout_id`
- `core_profile_id`
- `mode_profile_id`
- `loadout_name`
- `identity_block`
- `role_block`
- `capability_boundary_block`
- `safety_boundary_block`
- `privacy_boundary_block`
- `projection_ref_ids`
- `source_candidate_ids`
- `capability_binding_ids`
- `total_chars`
- `truncated`
- `private`
- `created_at`
- `loadout_attrs`

Draft fields:

- `draft_id`
- `core_profile_id`
- `mode_profile_id`
- `draft_name`
- `projected_blocks`
- `source_refs`
- `unresolved_questions`
- `review_status`
- `private`
- `canonical_activation_enabled`
- `created_at`
- `draft_attrs`

## Boundary Rules

v0.16.2 does not add:

- runtime mode selection;
- CLI mode switching;
- ChatService mode mutation;
- AgentRuntime mode mutation;
- automatic Personal Overlay loading;
- permission grants;
- tool execution;
- shell execution;
- network execution;
- MCP connection;
- plugin loading;
- LLM summarization;
- JSONL personal/persona store;
- canonical activation of a draft.

Capability truth remains authoritative. Personal profile text and loadout text are not capability grants.

## Generic Mode Examples

The tests use only generic public-safe examples:

`research_mode`

- can analyze provided documents;
- cannot claim filesystem access unless explicit capability exists.

`coding_mode`

- may reason about code provided in prompt;
- runtime execution depends on actual capability binding.

`local_runtime_mode`

- may use local runtime capabilities only if explicitly bound;
- has no ambient shell, network, plugin, or MCP access.

`review_mode`

- reviews supplied text or artifacts;
- follows capability and privacy boundaries.

## OCEL Object Types

The service records:

- `personal_core_profile`
- `personal_mode_profile`
- `personal_mode_boundary`
- `personal_mode_capability_binding`
- `personal_mode_loadout`
- `personal_mode_loadout_draft`

## OCEL Events

The service records:

- `personal_core_profile_registered`
- `personal_mode_profile_registered`
- `personal_mode_boundary_registered`
- `personal_mode_capability_binding_registered`
- `personal_mode_loadout_created`
- `personal_mode_loadout_draft_created`
- `personal_mode_boundary_attached`
- `personal_mode_capability_boundary_attached`

## OCEL Relations

Best-effort relations link:

- mode profile belongs to core profile;
- boundary belongs to mode profile;
- capability binding belongs to mode profile;
- loadout uses core profile;
- loadout uses mode profile;
- loadout includes capability bindings;
- draft belongs to core profile;
- draft belongs to mode profile.

Projection ref ids and source candidate ids remain references. They do not imply automatic activation.

## Context History Adapter

The history adapter exports:

- `personal_core_profiles_to_history_entries`
- `personal_mode_profiles_to_history_entries`
- `personal_mode_loadouts_to_history_entries`
- `personal_mode_boundaries_to_history_entries`

The adapter source is:

```text
personal_mode_loadout
```

Priority policy:

- capability boundary: high;
- privacy boundary: high;
- mode separation: high;
- runtime/safety boundary: high;
- role/identity profile content: medium;
- other style/context content: lower priority.

## PIG/OCPX Reporting

`PIGReportService` includes:

- `personal_core_profile_count`
- `personal_mode_profile_count`
- `personal_mode_boundary_count`
- `personal_mode_capability_binding_count`
- `personal_mode_loadout_count`
- `personal_mode_loadout_draft_count`
- `personal_mode_private_count`
- `personal_mode_boundary_by_type`
- `personal_mode_by_type`
- `personal_mode_capability_available_now_count`
- `personal_mode_capability_requires_permission_count`
- `personal_mode_capability_not_implemented_count`

The report text includes Personal Core / Mode object counts and capability binding availability summaries.

## Test Coverage

The v0.16.2 tests cover:

- model `to_dict` shape;
- core profile registration;
- multiple dummy mode profile registration;
- distinct mode boundaries;
- capability bindings differing by mode;
- loadout block creation;
- runtime capability override statement;
- draft creation with `canonical_activation_enabled=False`;
- multi-mode loadout set creation from generic specs;
- history adapter entries and priorities;
- OCEL object/event shape;
- PIG/OCPX report counts;
- no runtime mode selection;
- no ChatService mode mutation;
- no LLM/tool/shell/network execution;
- no JSONL personal/persona store.

All tests use dummy public-safe content only.

## Restore Procedure

1. Confirm public version markers:

```powershell
.\.venv\Scripts\python.exe -c "import chanta_core; print(chanta_core.__version__)"
```

Expected:

```text
0.16.2
```

2. Run the v0.16.2 targeted test set:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_personal_mode_loadout_models.py tests\test_personal_mode_loadout_service.py tests\test_personal_mode_loadout_history_adapter.py tests\test_personal_mode_loadout_ocel_shape.py tests\test_personal_mode_loadout_boundaries.py
```

3. Run the full suite:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

4. Confirm no runtime mode switch feature was introduced:

```powershell
rg -n "AgentRuntime mode switch|chanta-cli --mode|canonical_activation_enabled=True" src tests docs
```

Expected:

```text
no matches
```

## Restore Checklist

- [ ] `personal_mode_loadout.py` exists.
- [ ] `PersonalCoreProfile` exists.
- [ ] `PersonalModeProfile` exists.
- [ ] `PersonalModeBoundary` exists.
- [ ] `PersonalModeCapabilityBinding` exists.
- [ ] `PersonalModeLoadout` exists.
- [ ] `PersonalModeLoadoutDraft` exists.
- [ ] `PersonalModeLoadoutService` exists.
- [ ] Core profile registration works.
- [ ] Mode profile registration works.
- [ ] Mode boundary registration works.
- [ ] Capability binding registration works.
- [ ] Mode loadout creation works.
- [ ] Mode loadout draft creation works.
- [ ] Multi-mode loadout set creation works from supplied generic specs.
- [ ] Capability boundary block includes runtime capability override statement.
- [ ] Drafts set `canonical_activation_enabled=False`.
- [ ] OCEL objects/events are recorded.
- [ ] ContextHistory adapter entries exist.
- [ ] PIG/OCPX report counts exist.
- [ ] No runtime mode selection exists.
- [ ] No CLI mode switching exists.
- [ ] No ChatService mode mutation exists.
- [ ] No LLM/tool/shell/network execution is introduced.

## Known Limitations

- No runtime mode binding yet.
- No CLI mode selection yet.
- No persona/personal conformance policy yet.
- No automatic mode selector yet.
- No canonical activation path for drafts.

## Future Work

- Personal Mode selection and runtime binding.
- CLI mode selection after conformance work.
- Persona/personal conformance checks.
- Runtime capability binding verification.
- Mode loadout review workflow.

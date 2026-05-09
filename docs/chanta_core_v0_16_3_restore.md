# ChantaCore v0.16.3 Restore Notes

Version name: ChantaCore v0.16.3 - Personal Mode Selection / Runtime Binding

This document is a restore-grade record of the v0.16.3 implementation. It is not canonical runtime activation state. Personal Mode Binding records describe selected mode context and runtime binding metadata; they do not grant capabilities or switch active runtime behavior.

## Restore Goal

v0.16.3 adds a generic Personal Mode Selection / Runtime Binding framework.

The restoration target is a public framework that can record:

- a selected Personal Mode;
- a descriptive runtime binding for the selected mode;
- runtime capability binding metadata;
- a request to activate a Personal Mode for prompt context;
- a result showing whether the binding was attached as prompt context or denied.

The feature is intentionally non-executing. It does not execute tools, create permissions, alter runtime routing, or infer modes from natural language.

## Implemented Files

Core implementation:

- `src/chanta_core/persona/personal_mode_binding.py`
- `src/chanta_core/persona/ids.py`
- `src/chanta_core/persona/errors.py`
- `src/chanta_core/persona/history_adapter.py`
- `src/chanta_core/persona/__init__.py`
- `src/chanta_core/pig/reports.py`

Version marker:

- `pyproject.toml`
- `src/chanta_core/__init__.py`

Restore document:

- `docs/chanta_core_v0_16_3_restore.md`

Tests:

- `tests/test_personal_mode_binding_models.py`
- `tests/test_personal_mode_binding_service.py`
- `tests/test_personal_mode_binding_history_adapter.py`
- `tests/test_personal_mode_binding_ocel_shape.py`
- `tests/test_personal_mode_binding_boundaries.py`
- `tests/test_imports.py`
- `tests/test_pig_reports.py`

## Public Models

`PersonalModeSelection`

- Records one selected Personal Mode.
- Tracks core profile id, mode profile id, optional loadout id, selected mode name/type, selection source, session id, turn id, status, privacy flag, timestamp, and attrs.
- Selection is metadata. It does not imply capability availability.

`PersonalRuntimeBinding`

- Records how a selected mode maps to a runtime kind.
- Tracks runtime kind, optional runtime path, context ingress policy, optional capability profile reference, status, privacy flag, timestamp, and attrs.
- Binding is descriptive. It does not execute a runtime.

`PersonalRuntimeCapabilityBinding`

- Records runtime capability metadata for a binding.
- Tracks capability name/category, availability, execution status, permission/review requirement, source kind/ref, timestamp, and attrs.
- It must not create a permission grant.

`PersonalModeActivationRequest`

- Records a request to attach or record a Personal Mode binding.
- Tracks mode profile id, optional loadout id, runtime kind, requester, session id, turn id, reason, timestamp, and attrs.

`PersonalModeActivationResult`

- Records the result of an activation request.
- Tracks request id, optional selection id, optional runtime binding id, status, activation flag, activation scope, capability boundary summary, denied reason, finding ids, timestamp, and attrs.
- In v0.16.3 the normal activation scopes are:
  - `prompt_context_only`
  - `runtime_binding_only`
  - `none` for denied attempts.

## Service Surface

`PersonalModeBindingService` supports:

- `select_mode`
- `bind_runtime`
- `register_runtime_capability_binding`
- `create_activation_request`
- `activate_mode_for_prompt_context`
- `render_runtime_binding_block`

Expected restoration behavior:

- selection records the chosen mode and optional loadout;
- runtime binding infers a default context ingress from runtime kind;
- runtime capability binding records metadata only;
- activation records prompt-context or runtime-binding scope only;
- active runtime switching attempts are denied;
- rendered blocks explicitly say that the binding does not grant new runtime capabilities.

## Runtime Kind Semantics

`external_chat`

- Default context ingress: `manual_handoff`.
- No local repository access is implied.
- No file or test execution is implied.

`local_chat_runtime`

- Default context ingress: `session_context_projection`.
- No shell, network, or plugin access is implied.
- Workspace access remains dependent on explicit runtime capability metadata.

`codex_like_local_repo`

- Default context ingress: `manual_handoff`.
- Represents a code-review or patch-capable external environment as metadata.
- ChantaCore does not execute anything through this binding.

`local_runtime`

- Default context ingress: `local_runtime_context`.
- Represents ChantaCore local runtime context.
- Explicit skill access remains the capability boundary.

`review_runtime`

- Default context ingress: `session_context_projection`.
- Represents review over supplied context or artifacts.

`manual_handoff`

- Default context ingress: `manual_handoff`.
- User-provided context only.

`test_runtime`

- Default context ingress: `none`.
- Used for tests and metadata-only binding behavior.

## Boundary Rules

v0.16.3 does not add:

- automatic mode switching from user prompt;
- CLI mode switching;
- active runtime behavior mutation;
- active tool routing;
- permission grant creation;
- shell execution;
- network execution;
- MCP connection;
- plugin loading;
- LLM classification;
- JSONL personal mode store;
- automatic Personal Directory loading;
- private content import.

Capability truth remains authoritative. Personal Mode claims and binding metadata cannot override the runtime capability profile.

The rendered runtime binding block includes:

```text
This binding does not grant new runtime capabilities.
```

It also includes:

```text
Runtime capability profile overrides personal/persona claims.
```

## OCEL Object Types

The service records:

- `personal_mode_selection`
- `personal_runtime_binding`
- `personal_runtime_capability_binding`
- `personal_mode_activation_request`
- `personal_mode_activation_result`

## OCEL Events

The service records:

- `personal_mode_selected`
- `personal_runtime_binding_created`
- `personal_runtime_capability_binding_registered`
- `personal_mode_activation_requested`
- `personal_mode_activation_recorded`
- `personal_mode_activation_denied`
- `personal_mode_binding_attached_to_prompt`

## OCEL Relations

Best-effort relations link:

- mode selection references mode profile;
- mode selection references loadout;
- runtime binding belongs to selection;
- runtime capability binding belongs to runtime binding;
- activation result belongs to activation request;
- activation result references selection;
- activation result references runtime binding.

## Context History Adapter

The history adapter exports:

- `personal_mode_selections_to_history_entries`
- `personal_runtime_bindings_to_history_entries`
- `personal_mode_activation_results_to_history_entries`
- `personal_runtime_capability_bindings_to_history_entries`

The adapter source is:

```text
personal_mode_binding
```

Priority policy:

- denied activation: high;
- capability boundary: high;
- runtime binding: medium;
- selection: low to medium.

## PIG/OCPX Reporting

`PIGReportService` includes:

- `personal_mode_selection_count`
- `personal_runtime_binding_count`
- `personal_runtime_capability_binding_count`
- `personal_mode_activation_request_count`
- `personal_mode_activation_result_count`
- `personal_mode_activation_denied_count`
- `personal_mode_prompt_context_activation_count`
- `personal_runtime_binding_by_kind`
- `personal_context_ingress_by_type`
- `personal_runtime_capability_available_now_count`
- `personal_runtime_capability_requires_permission_count`
- `personal_runtime_capability_not_implemented_count`

## Test Coverage

The v0.16.3 tests cover:

- model `to_dict` shape;
- mode selection;
- `external_chat` defaulting to `manual_handoff`;
- `local_runtime` defaulting to `local_runtime_context`;
- runtime capability binding metadata;
- rendered capability boundary text;
- prompt-context activation scope;
- denial of active runtime attempts;
- history adapter entries;
- OCEL object/event shape;
- PIG/OCPX report counts;
- no runtime mutation;
- no capability grant creation;
- no LLM/tool/shell/network execution;
- no JSONL personal mode store.

All tests use dummy public-safe Personal Mode data only.

## Restore Procedure

1. Confirm public version markers:

```powershell
.\.venv\Scripts\python.exe -c "import chanta_core; print(chanta_core.__version__)"
```

Expected:

```text
0.16.3
```

2. Run the v0.16.3 targeted test set:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_personal_mode_binding_models.py tests\test_personal_mode_binding_service.py tests\test_personal_mode_binding_history_adapter.py tests\test_personal_mode_binding_ocel_shape.py tests\test_personal_mode_binding_boundaries.py
```

3. Run the full suite:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

4. Confirm no active runtime switching is introduced in the new layer:

```powershell
rg -n "active_runtime_requested.*False|This binding does not grant new runtime capabilities" src/chanta_core/persona/personal_mode_binding.py tests/test_personal_mode_binding_*.py docs/chanta_core_v0_16_3_restore.md
```

## Restore Checklist

- [ ] `personal_mode_binding.py` exists.
- [ ] `PersonalModeSelection` exists.
- [ ] `PersonalRuntimeBinding` exists.
- [ ] `PersonalRuntimeCapabilityBinding` exists.
- [ ] `PersonalModeActivationRequest` exists.
- [ ] `PersonalModeActivationResult` exists.
- [ ] `PersonalModeBindingService` exists.
- [ ] `select_mode` works.
- [ ] `bind_runtime` works.
- [ ] `register_runtime_capability_binding` works.
- [ ] `create_activation_request` works.
- [ ] `activate_mode_for_prompt_context` works.
- [ ] `render_runtime_binding_block` works.
- [ ] `external_chat` defaults to `manual_handoff`.
- [ ] `local_runtime` defaults to `local_runtime_context`.
- [ ] Binding does not grant capabilities.
- [ ] Activation scope is prompt-context or runtime-binding only.
- [ ] No active runtime switching exists.
- [ ] No runtime behavior mutation exists.
- [ ] No active tool routing exists.
- [ ] OCEL objects/events are recorded.
- [ ] ContextHistory adapter entries exist.
- [ ] PIG/OCPX report counts exist.
- [ ] No private content is included.
- [ ] No hardcoded private root exists.
- [ ] No LLM/tool/shell/network execution is introduced.

## Known Limitations

- No full CLI mode selector yet.
- No Personal Mode conformance validator yet.
- No active runtime mode switching.
- No automatic mode classifier.
- No runtime capability profile merge.

## Future Work

- CLI mode selection.
- Conformance validation.
- Controlled runtime mode activation only if a later design explicitly adds it.
- Runtime capability binding verification.
- Personal Mode Binding review workflows.

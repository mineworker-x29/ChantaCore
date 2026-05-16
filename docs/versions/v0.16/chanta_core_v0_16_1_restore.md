# ChantaCore v0.16.1 Restore Notes

Version name: ChantaCore v0.16.1 - Personal Directory / Personal Overlay Loader Boundary

This document is a restore-grade record of the v0.16.1 implementation. It is not canonical runtime state. ChantaCore canonical process state remains OCEL-based, and local Personal Directory content remains outside public ChantaCore state.

## Restore Goal

v0.16.1 adds a generic Personal Directory / Personal Overlay loader boundary.

The goal is not to import personal content. The goal is to define a safe boundary for optional local Personal Directory projections:

- the Personal Directory root comes from explicit local configuration;
- the root is optional;
- excluded areas are not treated as persona source;
- source bodies are not prompt blocks;
- reviewed projection files can be attached only through bounded projection references;
- unsafe boundary findings deny prompt attachment.

## Implemented Files

Core implementation:

- `src/chanta_core/persona/personal_overlay.py`
- `src/chanta_core/persona/ids.py`
- `src/chanta_core/persona/errors.py`
- `src/chanta_core/persona/history_adapter.py`
- `src/chanta_core/persona/__init__.py`
- `src/chanta_core/runtime/agent_runtime.py`
- `src/chanta_core/pig/reports.py`

Version marker:

- `pyproject.toml`
- `src/chanta_core/__init__.py`

Restore document:

- `docs/versions/v0.16/chanta_core_v0_16_1_restore.md`

Tests:

- `tests/test_personal_overlay_loader_models.py`
- `tests/test_personal_overlay_loader_service.py`
- `tests/test_personal_overlay_loader_boundaries.py`
- `tests/test_personal_overlay_loader_history_adapter.py`
- `tests/test_personal_overlay_loader_ocel_shape.py`
- `tests/test_chat_service_personal_overlay_integration.py`
- `tests/test_imports.py`
- `tests/test_pig_reports.py`

## Public Terminology

The public layer uses generic names:

- Personal Directory
- Personal Source
- Personal Profile
- Personal Overlay
- Personal Projection
- Personal Mode
- Personal Runtime Binding

The implementation must not hardcode any user-specific local directory or assistant name. A user can configure any local path as their Personal Directory outside the ChantaCore repository.

## Public Models

`PersonalDirectoryConfig`

- Records local Personal Directory configuration.
- Fields include config id, directory name, directory root, config source, private flag, status, created timestamp, and attrs.
- The directory root is supplied by environment, explicit input, or later local config. There is no hardcoded default root.

`PersonalDirectoryManifest`

- Records derived Personal Directory paths.
- Tracks `source`, `overlay`, `profiles`, `mode_loadouts`, `validation`, and excluded roots.
- `letters`, `messages`, and `archive` are excluded roots by default when present.

`PersonalOverlayLoadRequest`

- Records a request to load prompt-safe projection refs.
- Supports requested projection, requested profile, requested mode, session id, and turn id.

`PersonalProjectionRef`

- Represents a prompt-safe candidate projection reference.
- Stores projection name, path, kind, hash, preview, total chars, private flag, and safe-for-prompt flag.
- It is a projection reference, not raw source import.

`PersonalOverlayLoadResult`

- Records loaded projection ref ids, rendered blocks, total chars, truncation, denied state, and boundary finding ids.
- A denied result must not attach prompt content.

`PersonalOverlayBoundaryFinding`

- Records boundary failures or warnings.
- Finding types include root-inside-public-repo, excluded source import attempts, unsafe projection refs, large projections, and unknown issues.

## Service Surface

`PersonalOverlayLoaderService` supports:

- `load_config_from_env`
- `register_config`
- `load_manifest`
- `check_overlay_boundaries`
- `register_projection_refs`
- `load_projection_for_prompt`
- `render_personal_overlay_block`

Expected restoration behavior:

- absent environment config returns `None` and runtime remains unchanged;
- `CHANTA_PERSONAL_DIRECTORY_ROOT` is the public environment key;
- a registered config is private by default;
- manifest loading derives expected directories under the configured root;
- boundary checks reject unsafe configurations;
- projection refs come only from allowed projection directories;
- prompt rendering uses bounded loaded projection blocks;
- source bodies, letters, messages, and archives are not prompt blocks.

## Generic Personal Directory Shape

A local Personal Directory may use this shape:

```text
<PERSONAL_DIRECTORY_ROOT>/
  source/
    identity/
    preferences/
    operating_rules/
    style/
  letters/
    to_future_persona/
    to_user/
  overlay/
  profiles/
  mode_loadouts/
  validation/
  archive/
```

Only projection refs from these directories are prompt candidates by default:

- `overlay`
- `profiles`
- `mode_loadouts`

The following are excluded from prompt projection:

- `source`
- `letters`
- `messages`
- `archive`

Validation reports are not prompt projection refs in v0.16.1.

## Boundary Rules

v0.16.1 does not add:

- required Personal Directory usage;
- hardcoded local root;
- raw source body prompt injection;
- excluded letter/message/archive source import;
- JSONL private overlay store;
- canonical Markdown persona storage;
- permission grant creation;
- external capability activation;
- network fetch;
- shell execution;
- MCP connection;
- plugin loading;
- LLM summarization.

Capability truth remains authoritative. A Personal Overlay can provide prompt context only; it cannot grant runtime capabilities.

## Runtime Integration

`AgentRuntime` has optional Personal Overlay integration:

- if `CHANTA_PERSONAL_DIRECTORY_ROOT` is absent, the integration is a no-op;
- if configured, it loads config, manifest, boundary findings, projection refs, and a bounded load result;
- if boundary findings fail, prompt attachment is denied;
- if safe projection refs exist, the rendered Personal Overlay block is inserted after generic persona projection and before capability/session context.

Runtime metadata records:

- `personal_directory_manifest_id`
- `personal_overlay_load_result_id`
- `personal_overlay_denied`
- `personal_overlay_warning`

This integration does not mutate runtime mode and does not grant tools.

## OCEL Object Types

The loader records:

- `personal_directory_config`
- `personal_directory_manifest`
- `personal_overlay_load_request`
- `personal_projection_ref`
- `personal_overlay_load_result`
- `personal_overlay_boundary_finding`

## OCEL Events

The loader records:

- `personal_directory_config_registered`
- `personal_directory_manifest_loaded`
- `personal_overlay_boundary_checked`
- `personal_overlay_boundary_finding_recorded`
- `personal_projection_ref_registered`
- `personal_overlay_load_requested`
- `personal_overlay_load_completed`
- `personal_overlay_load_denied`
- `personal_projection_attached_to_prompt`

## OCEL Relations

Best-effort relations link:

- manifest uses config;
- projection ref belongs to manifest;
- request uses manifest;
- result belongs to request;
- result includes projection refs;
- finding checks manifest or request.

## Context History Adapter

The history adapter exports:

- `personal_directory_manifests_to_history_entries`
- `personal_projection_refs_to_history_entries`
- `personal_overlay_load_results_to_history_entries`
- `personal_overlay_boundary_findings_to_history_entries`

The adapter source is:

```text
personal_overlay
```

History entries should use basename, hash, or redacted path references rather than full local private paths.

## PIG/OCPX Reporting

`PIGReportService` includes:

- `personal_directory_config_count`
- `personal_directory_manifest_count`
- `personal_projection_ref_count`
- `personal_overlay_load_request_count`
- `personal_overlay_load_result_count`
- `personal_overlay_boundary_finding_count`
- `personal_overlay_load_denied_count`
- `personal_overlay_boundary_failed_count`
- `personal_projection_attached_to_prompt_count`
- `personal_overlay_safe_projection_count`

Reports expose counts and safety status. They should not expose private local paths.

## Test Coverage

The v0.16.1 tests cover:

- model `to_dict` shape;
- env absent no-op behavior;
- config from `CHANTA_PERSONAL_DIRECTORY_ROOT`;
- manifest directory detection;
- letters/messages/archive exclusion;
- projection refs only from `overlay`, `profiles`, and `mode_loadouts`;
- source bodies not loaded as prompt blocks;
- root-inside-public-repo boundary finding;
- denied load on boundary failure;
- bounded prompt block loading;
- history adapter redaction behavior;
- OCEL object/event shape;
- optional chat/runtime integration;
- no JSONL store;
- no network/shell/MCP/plugin/LLM behavior.

All tests use temporary dummy Personal Directories and public-safe content only.

## Restore Procedure

1. Confirm public version markers:

```powershell
.\.venv\Scripts\python.exe -c "import chanta_core; print(chanta_core.__version__)"
```

Expected:

```text
0.16.1
```

2. Run the v0.16.1 targeted test set:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_personal_overlay_loader_models.py tests\test_personal_overlay_loader_service.py tests\test_personal_overlay_loader_boundaries.py tests\test_personal_overlay_loader_history_adapter.py tests\test_personal_overlay_loader_ocel_shape.py tests\test_chat_service_personal_overlay_integration.py
```

3. Run the full suite:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

4. Confirm public code does not hardcode a private local root or legacy overlay vocabulary:

```powershell
rg -n "legacy_overlay_env_key|legacy_overlay_module|legacy overlay vocabulary" src tests docs
```

Expected:

```text
no matches
```

## Restore Checklist

- [ ] `personal_overlay.py` exists.
- [ ] All six Personal Overlay models exist.
- [ ] `PersonalOverlayLoaderService` exists.
- [ ] Personal Directory root is env/local/explicit only.
- [ ] No hardcoded private root exists.
- [ ] Env absent behavior is no-op.
- [ ] Letters/messages/archive are excluded.
- [ ] Source bodies are not prompt blocks.
- [ ] Projection refs come only from overlay/profiles/mode_loadouts.
- [ ] Boundary failure prevents prompt attachment.
- [ ] Optional runtime integration is gated.
- [ ] OCEL objects/events are recorded.
- [ ] ContextHistory adapter entries exist.
- [ ] PIG/OCPX report counts exist.
- [ ] No permission grant or runtime capability activation is created.

## Known Limitations

- No Personal Mode runtime binding.
- No CLI mode selection.
- No explicit local config file parser beyond env/explicit input.
- No conformance policy for Personal Directory content yet.
- No validation report prompt projection.

## Future Work

- Personal Core Profile and Personal Mode Loadouts.
- Personal Mode runtime binding.
- Personal Overlay conformance checks.
- More explicit local configuration files.
- Runtime selector policies for optional overlays.

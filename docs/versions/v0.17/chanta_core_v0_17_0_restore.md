# ChantaCore v0.17.0 Restore Document

Version name: ChantaCore v0.17.0 - Personal Runtime CLI / Local Config Surface

## Purpose

v0.17.0 adds a generic, diagnostic-only Personal Runtime CLI surface. A user may configure a local Personal Directory outside the ChantaCore repository through local environment/configuration. ChantaCore only exposes public framework concepts: Personal Directory, Personal Source, Personal Profile, Personal Overlay, Personal Projection, Personal Mode, Personal Runtime Binding, Personal Conformance, Personal Runtime Smoke Test, and Personal Runtime CLI.

The CLI is read-only in this version. It does not activate modes, grant capabilities, execute tools, call an LLM, open network connections, connect MCP, load plugins, or create a line-delimited personal runtime store.

## Implemented Files

- `src/chanta_core/persona/personal_runtime_surface.py`
- `src/chanta_core/persona/ids.py`
- `src/chanta_core/persona/errors.py`
- `src/chanta_core/persona/history_adapter.py`
- `src/chanta_core/persona/__init__.py`
- `src/chanta_core/cli/main.py`
- `src/chanta_core/pig/reports.py`
- `tests/test_personal_runtime_surface_models.py`
- `tests/test_personal_runtime_surface_service.py`
- `tests/test_personal_runtime_surface_cli.py`
- `tests/test_personal_runtime_surface_history_adapter.py`
- `tests/test_personal_runtime_surface_ocel_shape.py`
- `tests/test_personal_runtime_surface_boundaries.py`
- `tests/test_imports.py`
- `pyproject.toml`
- `src/chanta_core/__init__.py`

## Public API / Model Surface

New models:

- `PersonalRuntimeConfigView`
- `PersonalRuntimeStatusSnapshot`
- `PersonalRuntimeHealthCheck`
- `PersonalRuntimeDiagnostic`
- `PersonalCLICommandResult`

New service:

- `PersonalRuntimeSurfaceService`

New ID helpers:

- `new_personal_runtime_config_view_id`
- `new_personal_runtime_status_snapshot_id`
- `new_personal_runtime_health_check_id`
- `new_personal_runtime_diagnostic_id`
- `new_personal_cli_command_result_id`

## CLI Surface

Command group:

```powershell
chanta-cli personal
```

Subcommands:

```powershell
chanta-cli personal status
chanta-cli personal config
chanta-cli personal sources
chanta-cli personal overlays
chanta-cli personal modes
chanta-cli personal validate
chanta-cli personal smoke
```

Each subcommand accepts:

```powershell
--show-paths
```

Paths are redacted by default. `--show-paths` is an explicit local diagnostic override.

## Service Behavior

`load_config_view` discovers the Personal Directory from:

```text
CHANTA_PERSONAL_DIRECTORY_ROOT
```

If the environment variable is absent, `personal status` returns a controlled no-op result. `personal validate` and `personal smoke` return controlled diagnostics and non-zero exit codes. Expected missing configuration does not produce a traceback.

The CLI summarizes directory presence, overlay/profile/loadout counts, conformance status, smoke status, diagnostics, and health checks. It does not print Personal Source file bodies. It does not read `letters`, `messages`, or `archive` as source.

## OCEL Shape

Object types:

- `personal_runtime_config_view`
- `personal_runtime_status_snapshot`
- `personal_runtime_health_check`
- `personal_runtime_diagnostic`
- `personal_cli_command_result`

Events:

- `personal_runtime_config_view_created`
- `personal_runtime_status_snapshot_created`
- `personal_runtime_health_check_recorded`
- `personal_runtime_diagnostic_recorded`
- `personal_cli_command_started`
- `personal_cli_command_completed`
- `personal_cli_command_failed`
- `personal_cli_command_noop`

Relations:

- command result references diagnostics
- command result references status snapshot
- status snapshot references config view
- health check references status snapshot

## Context History

New adapters use `source="personal_runtime_surface"`:

- `personal_runtime_status_snapshots_to_history_entries`
- `personal_runtime_diagnostics_to_history_entries`
- `personal_cli_command_results_to_history_entries`

Failed commands receive high priority. Missing configuration diagnostics receive medium priority. Status snapshots are low to medium priority.

## PIG / OCPX Report Support

The PIG persona summary includes:

- `personal_runtime_config_view_count`
- `personal_runtime_status_snapshot_count`
- `personal_runtime_health_check_count`
- `personal_runtime_diagnostic_count`
- `personal_cli_command_result_count`
- `personal_directory_configured_count`
- `personal_directory_missing_count`
- `personal_cli_validate_run_count`
- `personal_cli_smoke_run_count`
- `personal_runtime_health_failed_count`
- `personal_runtime_health_warning_count`

## Restore Procedure

1. Install the package in editable mode:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

2. Run targeted tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_personal_runtime_surface_models.py tests\test_personal_runtime_surface_service.py tests\test_personal_runtime_surface_cli.py tests\test_personal_runtime_surface_history_adapter.py tests\test_personal_runtime_surface_ocel_shape.py tests\test_personal_runtime_surface_boundaries.py
```

3. Run the full suite:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

4. Check public hygiene:

```powershell
rg -n "private_persona_name|private_user_name|<LOCAL_PRIVATE_ROOT>" src tests docs README.md pyproject.toml
```

Expected result: no public private-content matches.

## Test Coverage

Covered behavior:

- env absent -> `personal status` controlled no-op
- env absent -> `personal validate` / `personal smoke` controlled diagnostics
- env present with public-safe dummy Personal Directory
- default path redaction
- optional `--show-paths`
- sources/overlays/modes summarize without printing file bodies
- conformance summary
- deterministic smoke summary
- OCEL objects/events/relations
- ContextHistory adapters
- PIG/OCPX summary counts
- boundary flags for no source body printing, no mode activation, no capability grants, no LLM/tool/shell/network/MCP/plugin execution, and no line-delimited runtime store

## Known Limitations

- No prompt-context mode activation yet.
- No explicit skill invocation surface yet.
- No natural-language skill proposal router yet.
- No read-only execution gate yet.
- CLI summaries intentionally avoid printing private source bodies or private projection contents.

## Future Work

- v0.17.1: prompt-context mode activation.
- v0.17.2: explicit skill invocation surface.
- v0.17.3: skill proposal router.
- v0.17.4: read-only execution gate.

## Checklist

- [x] Public terminology uses generic Personal Runtime CLI concepts.
- [x] Personal Directory is optional.
- [x] Local root comes from env/config.
- [x] Paths are redacted by default.
- [x] CLI does not print private source bodies.
- [x] CLI does not activate modes or grant capabilities.
- [x] OCEL shape added.
- [x] ContextHistory adapter added.
- [x] PIG/OCPX lightweight report support added.
- [x] Public tests use dummy data only.

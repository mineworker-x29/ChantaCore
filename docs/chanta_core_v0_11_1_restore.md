# ChantaCore v0.11.1 Restore

## Version

ChantaCore v0.11.1 - Read-only Verification Skills.

## Purpose

v0.11.1 adds read-only verification skills on top of the v0.11.0
`VerificationService`. The skills observe local state and record the result as
OCEL-native verification objects.

The canonical source remains OCEL event/object/relation records. No canonical
JSONL verification store is introduced. Markdown remains a human-readable view
or inspection target only and is not made canonical.

## Added File

The release adds:

- `src/chanta_core/verification/read_only_skills.py`

It exports:

- `ReadOnlyVerificationSkillSpec`
- `ReadOnlyVerificationSkillOutcome`
- `ReadOnlyVerificationSkillService`

## Skills

The service registers local read-only skills:

- `verify_file_exists`
- `verify_path_type`
- `verify_tool_available`
- `verify_runtime_python_info`
- `verify_ocel_object_type_exists`
- `verify_ocel_event_activity_exists`
- `verify_materialized_view_warning`
- `verify_tool_registry_view_warning`

Each skill records:

- `VerificationTarget`
- `VerificationRun`
- `VerificationEvidence`
- `VerificationResult`

Runs are completed, failed, or skipped through the existing verification
lifecycle. Passed and failed results still require evidence IDs.

## Allowed Observation Operations

v0.11.1 permits only read-only observations:

- `Path.exists()`
- `Path.is_file()`
- `Path.is_dir()`
- `shutil.which(...)`
- `sys.version`
- `sys.executable`
- `platform.platform()`
- read-only OCEL query or caller-provided fallback lists
- read-only text inspection of generated Markdown views

`verify_tool_available` resolves a command path but does not execute the tool.

## Forbidden Boundary

v0.11.1 does not implement:

- shell execution;
- network calls;
- file writes;
- file deletion or permission mutation;
- runtime `ToolDispatcher` mutation;
- tool blocking;
- tool input or output mutation;
- permission grants;
- sandbox behavior;
- process outcome evaluation;
- semantic retrieval or embeddings;
- external connectors, MCP, plugins, or marketplace loading;
- async runtime;
- UI.

Process outcome evaluation remains future v0.11.2 work.

## PIG / OCPX Reporting

PIG reports include lightweight read-only verification skill counts:

- read-only verification skill run count
- file existence verification count
- tool availability verification count
- OCEL shape verification count
- materialized view warning verification count
- read-only verification passed / failed counts

These are reporting counts only. They are not process outcome evaluation.

## Restore Checklist

- `read_only_skills.py` exists.
- All read-only skill specs set `read_only=True`.
- Each skill records evidence and result through `VerificationService`.
- Each skill starts and completes/fails/skips a verification run.
- No shell/network/write behavior is introduced.
- No permission/grant/sandbox behavior is introduced.
- No process outcome evaluation is introduced.
- PIG report exposes read-only verification skill counts.

## Restore / Verification Commands

Representative tests:

```powershell
.\.venv\Scripts\python.exe -m pytest `
  tests\test_imports.py `
  tests\test_read_only_verification_skill_models.py `
  tests\test_read_only_verification_skills.py `
  tests\test_read_only_verification_ocel_flow.py `
  tests\test_read_only_verification_boundaries.py `
  tests\test_verification_models.py `
  tests\test_verification_service.py `
  tests\test_verification_history_adapter.py `
  tests\test_verification_ocel_shape.py `
  tests\test_verification_boundaries.py `
  tests\test_pig_reports.py
```

Smoke script:

```powershell
.\.venv\Scripts\python.exe scripts\test_read_only_verification_skills.py
```

## Remaining Limitations

- No process outcome evaluation yet.
- No permission/grant/sandbox model yet.
- No external connector verification yet.
- No semantic retrieval.
- No UI.

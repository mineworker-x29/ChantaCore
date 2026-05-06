# ChantaCore v0.11.0 Restore

## Version

ChantaCore v0.11.0 - Verification Contract Foundation.

## Purpose

v0.11.0 adds an OCEL-native verification contract substrate. It defines
verification contracts, targets, requirements, runs, evidence, and results as
structured runtime facts.

The canonical source remains OCEL event/object/relation records. No canonical
JSONL verification store is introduced. Markdown remains a human-readable
materialized view mechanism only and is not made canonical by this release.

## Added Package

The release adds `src/chanta_core/verification/`:

- `__init__.py`
- `ids.py`
- `errors.py`
- `models.py`
- `service.py`
- `history_adapter.py`

## Models

The active verification object models are:

- `VerificationContract`
- `VerificationTarget`
- `VerificationRequirement`
- `VerificationRun`
- `VerificationEvidence`
- `VerificationResult`

These are represented in OCEL with object types:

- `verification_contract`
- `verification_target`
- `verification_requirement`
- `verification_run`
- `verification_evidence`
- `verification_result`

`VerificationResult` enforces the first contract rule: statuses `passed` and
`failed` require at least one evidence ID. `inconclusive`, `skipped`, and
`error` may exist without evidence.

## Service

`VerificationService` records verification facts through `TraceService` and
`OCELStore`.

It supports:

- registering, updating, and deprecating contracts;
- registering targets and requirements;
- starting, completing, failing, and skipping runs;
- recording evidence;
- recording results;
- attaching a result to a process instance as an observation link.

The service records OCEL events such as:

- `verification_contract_registered`
- `verification_contract_updated`
- `verification_contract_deprecated`
- `verification_target_registered`
- `verification_requirement_registered`
- `verification_run_started`
- `verification_run_completed`
- `verification_run_failed`
- `verification_run_skipped`
- `verification_evidence_recorded`
- `verification_result_recorded`

Optional attachment events may include:

- `verification_result_attached_to_process`

## Boundary

v0.11.0 is observation, not reasoning. It defines and records verification
contracts, evidence, and results, but it does not decide real-world file, tool,
or runtime state.

The LLM must not be treated as the source of truth for file, tool, or runtime
state. Actual read-only verification skills are future v0.11.1 work.

Process outcome evaluation is future v0.11.2 work.

This release does not implement:

- actual read-only verification skills;
- automatic file checks;
- automatic tool availability checks;
- runtime diagnostics checks;
- process outcome evaluation;
- permission or grant models;
- sandbox behavior;
- tool blocking;
- hook enforcement;
- semantic retrieval or embeddings;
- external connectors, MCP, plugins, or skill marketplace behavior;
- async runtime;
- UI;
- external dependencies.

## Context Projection

`verification_results_to_history_entries(...)` converts provided
`VerificationResult` objects into prompt-facing `ContextHistoryEntry` values.
It does not retrieve verification facts from OCEL automatically.

Verification history entries use `source="verification"` and preserve refs for:

- result ID
- run ID
- contract ID
- target ID
- evidence IDs

## PIG / OCPX Reporting

PIG reports include lightweight verification substrate counts:

- verification contract count
- target count
- requirement count
- run count
- evidence count
- result count
- passed / failed / inconclusive / skipped / error counts
- result distribution by contract type
- result distribution by target type

This is reporting only. It is not process outcome scoring or conformance
evaluation.

## Restore Checklist

- `src/chanta_core/verification/` exists.
- All verification models expose `to_dict()`.
- ID helpers use stable verification prefixes.
- `VerificationResult` rejects `passed` or `failed` without evidence IDs.
- `VerificationService` emits OCEL records.
- OCEL object types for contracts, targets, requirements, runs, evidence, and
  results are used.
- Verification result history adapter exists.
- PIG report exposes verification counts.
- No read-only verification skills are introduced.
- No canonical verification JSONL store is introduced.
- Markdown is not canonical.

## Restore / Verification Commands

Representative tests:

```powershell
.\.venv\Scripts\python.exe -m pytest `
  tests\test_imports.py `
  tests\test_verification_models.py `
  tests\test_verification_service.py `
  tests\test_verification_history_adapter.py `
  tests\test_verification_ocel_shape.py `
  tests\test_verification_boundaries.py `
  tests\test_pig_reports.py
```

Smoke script:

```powershell
.\.venv\Scripts\python.exe scripts\test_verification_contracts.py
```

## Remaining Limitations

- No read-only verification skills yet.
- No automatic file/tool/runtime checks yet.
- No process outcome evaluation yet.
- No permission/grant/sandbox model yet.
- No UI.

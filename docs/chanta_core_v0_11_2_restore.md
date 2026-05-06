# ChantaCore v0.11.2 Restore

## Version

ChantaCore v0.11.2 - Process Outcome Evaluation.

## Purpose

ChantaCore v0.11.2 adds OCEL-native process outcome evaluation.

Outcome evaluation is evidence-based and deterministic. It consumes existing
`VerificationResult` records and their evidence references, then records the
derived process outcome as OCEL objects and events.

The canonical source remains OCEL event/object/relation records. No canonical
JSONL outcome store is introduced. Markdown remains a human-readable
materialized view mechanism only and is not made canonical by this release.

## Added Package

The release adds `src/chanta_core/outcomes/`:

- `__init__.py`
- `ids.py`
- `errors.py`
- `models.py`
- `service.py`
- `history_adapter.py`

## Models

The active process outcome models are:

- `ProcessOutcomeContract`
- `ProcessOutcomeCriterion`
- `ProcessOutcomeTarget`
- `ProcessOutcomeSignal`
- `ProcessOutcomeEvaluation`

They are represented in OCEL with object types:

- `process_outcome_contract`
- `process_outcome_criterion`
- `process_outcome_target`
- `process_outcome_signal`
- `process_outcome_evaluation`

`ProcessOutcomeEvaluation` validates that `success`, `partial_success`, and
`failed` statuses have at least one signal ID or verification result ID.

If provided, score-like fields must be in the `0.0` to `1.0` range:

- `score`
- `confidence`
- `evidence_coverage`

## Service

`ProcessOutcomeEvaluationService` records outcome facts through `TraceService`
and `OCELStore`.

It supports:

- registering, updating, and deprecating outcome contracts;
- registering criteria;
- registering targets;
- recording signals;
- evaluating from a provided `VerificationResult` list;
- recording evaluations directly;
- attaching an evaluation to a process instance as an observation link.

The service records OCEL events such as:

- `process_outcome_contract_registered`
- `process_outcome_contract_updated`
- `process_outcome_contract_deprecated`
- `process_outcome_criterion_registered`
- `process_outcome_target_registered`
- `process_outcome_signal_recorded`
- `process_outcome_evaluation_started`
- `process_outcome_evaluation_recorded`
- `process_outcome_evaluation_failed`
- `process_outcome_evaluation_skipped`

Optional attachment events may include:

- `process_outcome_attached_to_process`

## Deterministic Evaluation Policy

Outcome evaluation consumes existing `VerificationResult` records and the evidence
references carried by those results. The evaluation policy is deterministic:
it counts passed, failed, inconclusive, skipped, and error verification results;
calculates pass rate, evidence coverage, score, and confidence; and then assigns
an outcome status from those values and the configured thresholds.

Default strict thresholds are:

- `min_required_pass_rate = 1.0`
- `min_evidence_coverage = 1.0`

Status selection:

- no verification results -> `inconclusive`
- all skipped results -> `skipped`
- error-only results -> `error`
- failed verification results -> `failed`
- thresholds met -> `success`
- some passed results with insufficient coverage -> `partial_success`
- otherwise -> `inconclusive`

The policy does not call an LLM judge and does not inspect the world directly.
It only evaluates the provided verification facts.

## OCEL Relations

The outcome service records best-effort object-centric relations where the
current OCEL APIs allow them:

- criterion belongs to contract
- evaluation uses contract
- evaluation evaluates target
- signal supports evaluation
- signal/evaluation derives from verification results
- evaluation is based on verification evidence references when available
- target/evaluation can be associated with session, turn, message, or process
  context

## Boundary

v0.11.2 evaluates process outcomes only. It does not enforce or repair runtime
behavior.

This release does not implement:

- permission grants;
- sandbox behavior;
- tool blocking;
- tool input or output mutation;
- hook enforcement;
- shell execution;
- network calls;
- LLM judge calls;
- automatic retry or replan;
- automatic memory promotion;
- automatic policy update;
- semantic retrieval or embeddings;
- external connectors, MCP, plugins, or skill marketplace behavior;
- async runtime;
- UI;
- external dependencies.

## Context Projection

`process_outcome_evaluations_to_history_entries(...)` converts provided
`ProcessOutcomeEvaluation` objects into prompt-facing `ContextHistoryEntry`
values. It does not retrieve outcome facts from OCEL automatically.

Outcome history entries use `source="process_outcome"` and preserve refs for:

- evaluation ID
- contract ID
- target ID
- signal IDs
- verification result IDs

Failed, needs-review, and error outcomes receive higher priority than success
entries.

## PIG / OCPX Reporting

PIG reports include lightweight process outcome counts:

- process outcome contract count
- criterion count
- target count
- signal count
- evaluation count
- success / partial success / failed / inconclusive / needs review / error
  counts
- distribution by contract type
- distribution by target type
- average evidence coverage
- average outcome score

This is reporting only. It does not perform automatic policy, skill, retry,
replan, or memory updates.

## Restore Checklist

- `src/chanta_core/outcomes/` exists.
- All outcome models expose `to_dict()`.
- ID helpers use stable process outcome prefixes.
- Evaluation status validation is active.
- Score, confidence, and evidence coverage range validation is active.
- `ProcessOutcomeEvaluationService` emits OCEL records.
- OCEL object types for contracts, criteria, targets, signals, and evaluations
  are used.
- Deterministic evaluation from `VerificationResult` lists works.
- Outcome history adapter exists.
- PIG report exposes outcome counts.
- No permission enforcement is introduced.
- No runtime mutation, tool blocking, retry, replan, memory promotion, or policy
  update is introduced.
- No canonical outcome JSONL store is introduced.
- Markdown is not canonical.

## Restore / Verification Commands

Representative tests:

```powershell
.\.venv\Scripts\python.exe -m pytest `
  tests\test_imports.py `
  tests\test_process_outcome_models.py `
  tests\test_process_outcome_service.py `
  tests\test_process_outcome_history_adapter.py `
  tests\test_process_outcome_ocel_shape.py `
  tests\test_process_outcome_boundaries.py `
  tests\test_verification_models.py `
  tests\test_verification_service.py `
  tests\test_pig_reports.py
```

Smoke script:

```powershell
.\.venv\Scripts\python.exe scripts\test_process_outcome_evaluation.py
```

Full compatibility should also include the v0.11.0 verification tests,
v0.11.1 read-only verification tests, and the v0.10.x substrate tests.

## Remaining Limitations

- v0.12.x permission scope, grant, and sandbox layers
- later recommendation and policy feedback loops
- deeper PIG/OCPX outcome analysis

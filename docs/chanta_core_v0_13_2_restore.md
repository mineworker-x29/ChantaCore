# ChantaCore v0.13.2 Restore Notes

Version: v0.13.2
Name: ChantaCore v0.13.2 - Delegation Conformance

This document is a restore-grade record. It describes enough of the v0.13.2
implementation to reconstruct the feature without chat history.

## Restore Goal

v0.13.2 adds structural delegation conformance. It checks whether delegation,
sidechain context, and summary return records obey the boundaries established in
v0.13.0 and v0.13.1.

Canonical state remains OCEL:

- contracts are OCEL objects
- rules are OCEL objects
- runs are OCEL objects
- findings are OCEL objects
- results are OCEL objects
- registration, run lifecycle, findings, and results are OCEL events

JSONL is not canonical conformance persistence.
Markdown is only a human-readable restore note.

## Files Added Or Modified

Primary implementation:

- `src/chanta_core/delegation/conformance.py`
- `src/chanta_core/delegation/ids.py`
- `src/chanta_core/delegation/errors.py`
- `src/chanta_core/delegation/history_adapter.py`
- `src/chanta_core/delegation/__init__.py`

Report/read-model integration:

- `src/chanta_core/pig/reports.py`
- `src/chanta_core/pig/inspector.py`

Script:

- `scripts/test_delegation_conformance.py`

Tests:

- `tests/test_delegation_conformance_models.py`
- `tests/test_delegation_conformance_service.py`
- `tests/test_delegation_conformance_history_adapter.py`
- `tests/test_delegation_conformance_ocel_shape.py`
- `tests/test_delegation_conformance_boundaries.py`
- `tests/test_imports.py`
- `tests/test_pig_reports.py`

Version/doc:

- `pyproject.toml`
- `src/chanta_core/__init__.py`
- `docs/chanta_core_v0_13_2_restore.md`

## Models

Implemented in `src/chanta_core/delegation/conformance.py`.

Dataclasses:

- `DelegationConformanceContract`
- `DelegationConformanceRule`
- `DelegationConformanceRun`
- `DelegationConformanceFinding`
- `DelegationConformanceResult`

All models are frozen dataclasses and expose `to_dict()`.

## ID Helpers

Implemented in `src/chanta_core/delegation/ids.py`.

Required helpers and prefixes:

- `new_delegation_conformance_contract_id()` -> `delegation_conformance_contract:...`
- `new_delegation_conformance_rule_id()` -> `delegation_conformance_rule:...`
- `new_delegation_conformance_run_id()` -> `delegation_conformance_run:...`
- `new_delegation_conformance_finding_id()` -> `delegation_conformance_finding:...`
- `new_delegation_conformance_result_id()` -> `delegation_conformance_result:...`

The implementation uses `uuid4()` like the delegation and sidechain helpers.

## Errors

Implemented in `src/chanta_core/delegation/errors.py`.

Required classes:

- `DelegationConformanceError`
- `DelegationConformanceContractError`
- `DelegationConformanceRuleError`
- `DelegationConformanceRunError`
- `DelegationConformanceFindingError`
- `DelegationConformanceResultError`

All inherit from `DelegationError`.

## Model Fields

### DelegationConformanceContract

Fields:

- `contract_id`
- `contract_name`
- `contract_type`
- `description`
- `status`
- `severity`
- `created_at`
- `updated_at`
- `contract_attrs`

Allowed `contract_type` values:

- `delegation_structure`
- `sidechain_context`
- `permission_boundary`
- `transcript_boundary`
- `return_envelope`
- `safety_reference`
- `manual`
- `other`

Allowed `status` values:

- `active`
- `draft`
- `deprecated`
- `archived`
- `withdrawn`

Allowed severities:

- `info`
- `low`
- `medium`
- `high`
- `critical`

### DelegationConformanceRule

Fields:

- `rule_id`
- `contract_id`
- `rule_type`
- `description`
- `required`
- `severity`
- `expected_value`
- `status`
- `rule_attrs`

Allowed `rule_type` values:

- `packet_exists`
- `delegated_run_uses_packet`
- `sidechain_derived_from_packet`
- `no_full_parent_transcript`
- `no_permission_inheritance`
- `summary_only_return`
- `no_full_child_transcript`
- `safety_refs_preserved`
- `allowed_capabilities_respected`
- `parent_child_link_exists`
- `required_packet_fields_present`
- `return_envelope_exists`
- `isolation_mode_allowed`
- `manual`
- `other`

### DelegationConformanceRun

Fields:

- `run_id`
- `contract_id`
- `packet_id`
- `delegated_run_id`
- `sidechain_context_id`
- `return_envelope_id`
- `status`
- `started_at`
- `completed_at`
- `run_attrs`

Allowed statuses:

- `started`
- `completed`
- `failed`
- `skipped`
- `error`

### DelegationConformanceFinding

Fields:

- `finding_id`
- `run_id`
- `rule_id`
- `rule_type`
- `status`
- `severity`
- `message`
- `subject_type`
- `subject_ref`
- `evidence_refs`
- `created_at`
- `finding_attrs`

Allowed statuses:

- `passed`
- `failed`
- `warning`
- `skipped`
- `inconclusive`
- `error`

### DelegationConformanceResult

Fields:

- `result_id`
- `run_id`
- `contract_id`
- `status`
- `score`
- `confidence`
- `passed_finding_ids`
- `failed_finding_ids`
- `warning_finding_ids`
- `skipped_finding_ids`
- `reason`
- `created_at`
- `result_attrs`

Allowed statuses:

- `passed`
- `failed`
- `needs_review`
- `inconclusive`
- `skipped`
- `error`

Validation:

- `score` must be `None` or within `[0.0, 1.0]`
- `confidence` must be `None` or within `[0.0, 1.0]`

## Service

Service:

- `DelegationConformanceService`

Primary methods:

- `register_contract`
- `register_rule`
- `register_default_rules`
- `start_run`
- `record_finding`
- `record_result`
- `complete_run`
- `fail_run`
- `skip_run`
- `evaluate_delegation_conformance`

The service performs deterministic structural checks only. It does not execute
subagents, call `AgentRuntime`, call an LLM, dispatch tools, execute shell or
network actions, mutate packet/sidechain/run/envelope inputs, auto-fix failures,
or enforce runtime behavior.

Constructor:

- `trace_service: TraceService | None = None`
- `ocel_store: OCELStore | None = None`

Constructor behavior follows the earlier delegation services:

- supplied `trace_service` is used directly
- supplied `ocel_store` is wrapped with `TraceService(ocel_store=...)`
- neither supplied creates default `TraceService()`

## Service Method Details

### register_contract

Creates a `DelegationConformanceContract`, records
`delegation_conformance_contract_registered`, and returns the contract.

### register_rule

Creates a `DelegationConformanceRule`, records
`delegation_conformance_rule_registered`, relates the rule to the contract with
`belongs_to_contract`, and returns the rule.

### register_default_rules

Registers the default rule set under a contract. Default severities are:

- `packet_exists`: `critical`
- `delegated_run_uses_packet`: `high`
- `sidechain_derived_from_packet`: `high`
- `no_full_parent_transcript`: `critical`
- `no_permission_inheritance`: `critical`
- `summary_only_return`: `high`
- `no_full_child_transcript`: `critical`
- `safety_refs_preserved`: `medium`
- `required_packet_fields_present`: `high`

### start_run

Creates a `DelegationConformanceRun` with `status="started"`, records
`delegation_conformance_run_started`, and relates the run to the contract and
checked packet/run/sidechain/envelope IDs where supplied.

### record_finding

Creates a `DelegationConformanceFinding`, records
`delegation_conformance_finding_recorded`, relates the finding to the run and
rule, and relates the finding to the checked subject when a subject ref is
available.

### record_result

Creates a `DelegationConformanceResult`, records
`delegation_conformance_result_recorded`, and relates result to run and
contract. Finding IDs are included as event-object relations when supplied.

### complete_run / fail_run / skip_run

Return updated immutable run records through `dataclasses.replace()` and record:

- `delegation_conformance_run_completed`
- `delegation_conformance_run_failed`
- `delegation_conformance_run_skipped`

These methods only record lifecycle state. They do not enforce runtime behavior.

### evaluate_delegation_conformance

Starts a run, evaluates each active rule deterministically, records one finding
per rule, records one result, completes the run, and returns the result.

Important input behavior:

- `DelegationPacket` is read only
- `DelegatedProcessRun` is read only
- `SidechainContext` is read only
- `SidechainReturnEnvelope` is read only
- no input object is mutated
- no auto-fix path is present

## Default Rules

`register_default_rules()` registers:

- `packet_exists`
- `delegated_run_uses_packet`
- `sidechain_derived_from_packet`
- `no_full_parent_transcript`
- `no_permission_inheritance`
- `summary_only_return`
- `no_full_child_transcript`
- `safety_refs_preserved`
- `required_packet_fields_present`

## Rule Semantics

`packet_exists`:

- passes when `packet` is present
- fails when missing

`delegated_run_uses_packet`:

- passes when delegated run references the packet ID
- fails on mismatched packet ID
- inconclusive when packet or run is missing

`sidechain_derived_from_packet`:

- passes when sidechain context references the packet ID
- fails on mismatch
- inconclusive when packet or sidechain is missing

`no_full_parent_transcript`:

- passes when sidechain `contains_full_parent_transcript` is false
- fails when true
- inconclusive when sidechain is missing

`no_permission_inheritance`:

- passes when delegated run and/or sidechain have `inherited_permissions=False`
- fails if either present subject has permission inheritance true
- inconclusive if both subjects are missing

`summary_only_return` and `no_full_child_transcript`:

- pass when return envelope exists and `contains_full_child_transcript=False`
- fail when true
- inconclusive when return envelope is missing

`safety_refs_preserved`:

- passes when packet has no safety refs
- passes when all packet safety refs appear in `sidechain_context.safety_ref_ids`
- warns when packet has safety refs but sidechain is missing or refs are absent

`required_packet_fields_present`:

- passes when packet exists and has a non-empty `goal`
- fails otherwise

## Result Derivation

Evaluation starts a conformance run, records one finding per active rule, records
one result, then completes the run.

Result policy:

- any required failed finding -> `failed`
- no required failures but warnings/errors -> `needs_review`
- required inconclusive findings -> `inconclusive`
- all required findings passed -> `passed`
- no active required checks -> `skipped`

Score:

- `passed_required / total_required`
- `None` when there are no required findings

Confidence:

- mirrors score when score is known

## OCEL Object Types

Required object types:

- `delegation_conformance_contract`
- `delegation_conformance_rule`
- `delegation_conformance_run`
- `delegation_conformance_finding`
- `delegation_conformance_result`

## OCEL Event Activities

Required events:

- `delegation_conformance_contract_registered`
- `delegation_conformance_rule_registered`
- `delegation_conformance_run_started`
- `delegation_conformance_run_completed`
- `delegation_conformance_run_failed`
- `delegation_conformance_run_skipped`
- `delegation_conformance_finding_recorded`
- `delegation_conformance_result_recorded`

Event attrs include:

- `observability_only=True`
- `delegation_conformance_structural_only=True`
- `runtime_effect=False`
- `enforcement_enabled=False`

## Relation Intent

Object-object relation intent:

- rule belongs to contract
- run uses contract
- run checks packet
- run checks delegated run
- run checks sidechain context
- run checks return envelope
- finding belongs to run
- finding checks rule
- result is result of run
- result uses contract

## History Adapter

Added helpers in `src/chanta_core/delegation/history_adapter.py`:

- `delegation_conformance_findings_to_history_entries`
- `delegation_conformance_results_to_history_entries`

Behavior:

- `source="delegation_conformance"`
- `role="context"`
- refs include finding/result/run/contract/rule/subject/evidence IDs
- failed findings and failed/needs_review results have high priority

## PIG/OCPX Report Support

`src/chanta_core/pig/reports.py` exposes `delegation_conformance_summary`:

- `delegation_conformance_contract_count`
- `delegation_conformance_rule_count`
- `delegation_conformance_run_count`
- `delegation_conformance_finding_count`
- `delegation_conformance_result_count`
- `delegation_conformance_passed_count`
- `delegation_conformance_failed_count`
- `delegation_conformance_needs_review_count`
- `delegation_conformance_inconclusive_count`
- `delegation_conformance_failed_finding_count`
- `delegation_conformance_warning_finding_count`
- `delegation_conformance_by_rule_type`
- `average_delegation_conformance_score`

The text report includes a `Delegation Conformance` section.

`src/chanta_core/pig/inspector.py` includes the same summary in `pig_summary`
and `inspection_attrs`.

## Public Imports

`src/chanta_core/delegation/__init__.py` exports:

- `DelegationConformanceContract`
- `DelegationConformanceRule`
- `DelegationConformanceRun`
- `DelegationConformanceFinding`
- `DelegationConformanceResult`
- `DelegationConformanceService`
- `delegation_conformance_findings_to_history_entries`
- `delegation_conformance_results_to_history_entries`

`tests/test_imports.py` imports and asserts those symbols.

## Tests Added

`tests/test_delegation_conformance_models.py` verifies:

- ID prefixes
- `to_dict()` output for all models
- score/confidence validation

`tests/test_delegation_conformance_service.py` verifies:

- contract/rule events are recorded
- default rules are registered
- good packet/run/sidechain/envelope passes
- missing packet creates failed/inconclusive findings
- parent transcript violation fails
- permission inheritance violation fails
- full child transcript violation fails
- missing sidechain safety refs creates `needs_review`
- packet and sidechain inputs are not auto-fixed

`tests/test_delegation_conformance_history_adapter.py` verifies:

- findings/results convert to `ContextHistoryEntry`
- source is `delegation_conformance`
- refs include expected IDs
- failed/review items have high priority

`tests/test_delegation_conformance_ocel_shape.py` verifies:

- conformance object types exist
- conformance event activities exist
- result relations exist

`tests/test_delegation_conformance_boundaries.py` verifies:

- no active runtime execution imports/calls
- structural-only event markers are present

## Boundary Guarantees

v0.13.2 does not:

- execute subagents
- call `AgentRuntime` for child runs
- call LLM
- execute tools
- execute shell commands
- call network
- mutate `DelegationPacket`
- mutate `SidechainContext`
- auto-fix failures
- inherit parent permissions
- implement runtime enforcement
- implement a `ToolDispatcher` gate
- implement external connector/MCP/plugin delegation
- add async worker
- add UI

## Verification Commands

Install:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

Targeted tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_imports.py tests\test_delegation_conformance_models.py tests\test_delegation_conformance_service.py tests\test_delegation_conformance_history_adapter.py tests\test_delegation_conformance_ocel_shape.py tests\test_delegation_conformance_boundaries.py
```

Full tests:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Script:

```powershell
.\.venv\Scripts\python.exe scripts\test_delegation_conformance.py
```

Observed during implementation:

- targeted conformance/import/PIG tests: `27 passed`
- acceptance subset: `198 passed`
- full pytest: `575 passed`, `1 skipped`, `3 warnings`
- smoke script printed `status=passed` and `score=1.0`
- `scripts/test_llm_client.py` exited with code `0`

The three warnings were unrelated invalid JSONL row warnings in edit proposal,
process job, and process schedule store tests.

## Editable Install Note

Command:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

The first sandboxed attempt failed with network/build dependency access
restriction while fetching setuptools. An approved escalated rerun installed:

- `chanta-core==0.13.2`

It replaced the previous editable install:

- `chanta-core==0.13.1`

## Git Hygiene Observed

Commands:

```powershell
git status --short
git status --ignored --short data .pytest-tmp
git ls-files | findstr "data"
git ls-files | findstr ".sqlite"
git ls-files | findstr ".env"
```

Observed:

- `data/` ignored
- `.pytest-tmp/` ignored
- no tracked `data` files
- tracked `.sqlite` match was only `tests/test_ocel_export_sqlite.py`
- tracked `.env` match was only `.env.example`
- `note.md` did not exist

## Future Work

- v0.14.x external layer entry
- later active subagent runtime only after conformance and safety boundaries are
  mature

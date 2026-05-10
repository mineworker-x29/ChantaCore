# ChantaCore v0.17.5 Restore Document

Version name: ChantaCore v0.17.5 - Execution Provenance & Result Envelope

## Purpose

v0.17.5 adds a generic Execution Envelope framework. It wraps already-produced explicit invocation results and gated invocation results into a standard provenance and result envelope.

The envelope service does not execute skills. It does not grant capabilities, call an LLM, execute shell/network/write/MCP/plugin operations, promote outputs to memory/persona, or create a line-delimited execution store.

By default, the envelope stores preview/hash/ref snapshots rather than full input or output bodies.

## Implemented Files

- `src/chanta_core/execution/__init__.py`
- `src/chanta_core/execution/ids.py`
- `src/chanta_core/execution/errors.py`
- `src/chanta_core/execution/models.py`
- `src/chanta_core/execution/envelope_service.py`
- `src/chanta_core/execution/history_adapter.py`
- `src/chanta_core/pig/reports.py`
- `tests/test_execution_envelope_models.py`
- `tests/test_execution_envelope_service.py`
- `tests/test_execution_envelope_gated_invocation.py`
- `tests/test_execution_envelope_redaction.py`
- `tests/test_execution_envelope_history_adapter.py`
- `tests/test_execution_envelope_ocel_shape.py`
- `tests/test_execution_envelope_boundaries.py`
- `tests/test_imports.py`
- `pyproject.toml`
- `src/chanta_core/__init__.py`

## Public API / Model Surface

New models:

- `ExecutionEnvelope`
- `ExecutionProvenanceRecord`
- `ExecutionInputSnapshot`
- `ExecutionOutputSnapshot`
- `ExecutionArtifactRef`
- `ExecutionOutcomeSummary`

New service:

- `ExecutionEnvelopeService`

New helpers:

- `hash_payload`
- `preview_payload`
- `redact_sensitive_fields`
- `summarize_status`

New history adapters:

- `execution_envelopes_to_history_entries`
- `execution_outcome_summaries_to_history_entries`
- `execution_provenance_records_to_history_entries`

## Service Behavior

`ExecutionEnvelopeService.wrap_explicit_invocation_result` creates:

- execution envelope
- input snapshot
- output snapshot
- provenance record
- outcome summary

`ExecutionEnvelopeService.wrap_gated_invocation_result` additionally records gate request, gate decision, and gate result references when available.

The service only wraps existing result objects. It does not call skill invocation or gate execution methods.

## Snapshot Policy

Input and output snapshots store:

- preview
- hash
- reference identifier when available
- redacted field list

Defaults:

- `full_input_stored=False`
- `full_output_stored=False`

Sensitive keys are redacted from previews:

- `password`
- `token`
- `secret`
- `api_key`
- `private_key`
- `credential`

## OCEL Shape

Object types:

- `execution_envelope`
- `execution_provenance_record`
- `execution_input_snapshot`
- `execution_output_snapshot`
- `execution_artifact_ref`
- `execution_outcome_summary`

Events:

- `execution_envelope_created`
- `execution_provenance_recorded`
- `execution_input_snapshot_recorded`
- `execution_output_snapshot_recorded`
- `execution_artifact_ref_recorded`
- `execution_outcome_summary_recorded`
- `execution_envelope_completed`
- `execution_envelope_blocked`
- `execution_envelope_failed`
- `execution_envelope_skipped`

Relations:

- provenance belongs to envelope
- input snapshot belongs to envelope
- output snapshot belongs to envelope
- artifact ref belongs to envelope
- outcome summary summarizes envelope
- envelope references explicit invocation request/result when available
- envelope references gate request/decision/result when available
- envelope references proposal/capability/permission/session/sandbox/risk identifiers when available

## PIG / OCPX Report Support

The PIG skill usage summary includes:

- `execution_envelope_count`
- `execution_provenance_record_count`
- `execution_input_snapshot_count`
- `execution_output_snapshot_count`
- `execution_artifact_ref_count`
- `execution_outcome_summary_count`
- `execution_completed_count`
- `execution_blocked_count`
- `execution_failed_count`
- `execution_skipped_count`
- `execution_by_kind`
- `execution_by_skill_id`
- `execution_with_gate_count`
- `execution_without_gate_count`
- `execution_full_input_stored_count`
- `execution_full_output_stored_count`

Expected default full snapshot counts are zero.

## Restore Procedure

1. Install the package in editable mode:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

2. Run targeted tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_execution_envelope_models.py tests\test_execution_envelope_service.py tests\test_execution_envelope_gated_invocation.py tests\test_execution_envelope_redaction.py tests\test_execution_envelope_history_adapter.py tests\test_execution_envelope_ocel_shape.py tests\test_execution_envelope_boundaries.py
```

3. Run the full suite:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

4. Check public hygiene with generic private-boundary tokens only:

```powershell
rg -n "private_persona_name|private_user_name|<LOCAL_PRIVATE_ROOT>" src tests docs README.md pyproject.toml
```

Expected result: no public private-content matches.

## Test Coverage

Covered behavior:

- model serialization
- explicit invocation completed wraps to completed envelope
- gate blocked wraps to blocked envelope with `execution_performed=False`
- gate allowed and invocation completed wraps to completed envelope
- provenance includes gate and invocation references
- input snapshot stores preview/hash with full input disabled
- output snapshot stores preview/hash/ref with full output disabled
- sensitive fields are redacted from previews
- envelope service does not execute skills
- no LLM/shell/network/write/MCP/plugin execution
- OCEL objects/events/relations
- ContextHistory adapters
- PIG/OCPX lightweight counts

## Known Limitations

- Envelope service does not execute skills.
- No production audit export yet.
- No reviewed proposal-to-execution flow yet.
- The envelope currently standardizes explicit and gated skill invocation results first.

## Future Work

- Broader execution envelope use.
- Reviewed proposal-to-execution flow.
- Production audit export.

## Checklist

- [x] Execution Envelope framework added.
- [x] Explicit invocation wrapping works.
- [x] Gated invocation wrapping works.
- [x] Redaction works.
- [x] Full input storage remains disabled by default.
- [x] Full output storage remains disabled by default.
- [x] Provenance references are preserved.
- [x] OCEL shape added.
- [x] ContextHistory adapter added.
- [x] PIG/OCPX lightweight report support added.
- [x] No skill execution is added to envelope service.
- [x] No LLM/shell/network/write/MCP/plugin execution is added.

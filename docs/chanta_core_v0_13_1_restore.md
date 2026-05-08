# ChantaCore v0.13.1 Restore Notes

Version: v0.13.1
Name: ChantaCore v0.13.1 - Sidechain Context

This document is a restore-grade record of the v0.13.1 implementation. It
records what was added, how it is persisted, what must stay forbidden, and how
to verify that the implementation did not cross the runtime boundary.

## Restore Goal

v0.13.1 adds packet-derived sidechain context for delegated process work.

Sidechain context is not active subagent execution. It is a bounded context
artifact built from an existing `DelegationPacket`, recorded as OCEL objects and
events, and optionally connected to a `DelegatedProcessRun`.

Canonical state remains OCEL:

- sidechain contexts are OCEL objects
- context entries are OCEL objects
- snapshots are OCEL objects
- return envelopes are OCEL objects
- lifecycle and boundary records are OCEL events
- lineage is represented through OCEL relations

JSONL is not canonical sidechain persistence.
Markdown is not canonical sidechain persistence.

## Files Added Or Modified

Primary implementation:

- `src/chanta_core/delegation/sidechain.py`
- `src/chanta_core/delegation/ids.py`
- `src/chanta_core/delegation/errors.py`
- `src/chanta_core/delegation/history_adapter.py`
- `src/chanta_core/delegation/__init__.py`

Report/read-model integration:

- `src/chanta_core/pig/reports.py`
- `src/chanta_core/pig/inspector.py`
- `src/chanta_core/ocpx/loader.py`

Script:

- `scripts/test_sidechain_context.py`

Tests:

- `tests/test_sidechain_context_models.py`
- `tests/test_sidechain_context_service.py`
- `tests/test_sidechain_context_history_adapter.py`
- `tests/test_sidechain_context_ocel_shape.py`
- `tests/test_sidechain_context_boundaries.py`
- `tests/test_imports.py`
- `tests/test_pig_reports.py`

Version/doc:

- `pyproject.toml`
- `src/chanta_core/__init__.py`
- `docs/chanta_core_v0_13_1_restore.md`

## ID Helpers

Implemented in `src/chanta_core/delegation/ids.py`.

Required helpers and prefixes:

- `new_sidechain_context_id()` -> `sidechain_context:...`
- `new_sidechain_context_entry_id()` -> `sidechain_context_entry:...`
- `new_sidechain_context_snapshot_id()` -> `sidechain_context_snapshot:...`
- `new_sidechain_return_envelope_id()` -> `sidechain_return_envelope:...`

The implementation uses `uuid4()`, consistent with v0.13.0 delegation IDs.

## Errors

Implemented in `src/chanta_core/delegation/errors.py`.

Required classes:

- `SidechainContextError`
- `SidechainContextEntryError`
- `SidechainContextSnapshotError`
- `SidechainReturnEnvelopeError`

All inherit from `DelegationError`.

## Sidechain Models

All sidechain models live in `src/chanta_core/delegation/sidechain.py`.
They are frozen dataclasses and expose `to_dict()`.

### SidechainContext

Purpose:

- Represents an isolated packet-derived context for delegated work.
- It is derived from `DelegationPacket`.
- It may point to a `DelegatedProcessRun`.
- It must not include full parent transcript or inherited permissions.

Fields:

- `sidechain_context_id`
- `packet_id`
- `delegated_run_id`
- `parent_session_id`
- `child_session_id`
- `parent_process_instance_id`
- `child_process_instance_id`
- `context_type`
- `isolation_mode`
- `status`
- `created_at`
- `entry_ids`
- `safety_ref_ids`
- `contains_full_parent_transcript`
- `inherited_permissions`
- `context_attrs`

Allowed `context_type` values:

- `delegation`
- `subagent`
- `verification`
- `analysis`
- `review`
- `manual`
- `other`

Allowed `isolation_mode` values:

- `packet_only`
- `sidechain`
- `external`
- `other`

Allowed `status` values:

- `created`
- `ready`
- `sealed`
- `archived`
- `error`

Hard invariants:

- `contains_full_parent_transcript` must be `False`
- `inherited_permissions` must be `False`

The model raises `SidechainContextError` if either invariant is violated.

### SidechainContextEntry

Purpose:

- Represents one item of packet-derived sidechain context.
- Entries are intentionally granular so safety refs and structured packet data
  can be inspected independently.

Fields:

- `entry_id`
- `sidechain_context_id`
- `entry_type`
- `title`
- `content`
- `content_ref`
- `payload`
- `source_kind`
- `source_ref`
- `priority`
- `created_at`
- `entry_attrs`

Allowed `entry_type` values:

- `goal`
- `context_summary`
- `structured_input`
- `object_ref`
- `allowed_capability`
- `expected_output_schema`
- `termination_condition`
- `permission_ref`
- `sandbox_ref`
- `risk_ref`
- `outcome_ref`
- `instruction`
- `manual`
- `other`

### SidechainContextSnapshot

Purpose:

- Captures a summary view of a sidechain context and its entry IDs.
- It is a record, not a mutable context store.

Fields:

- `snapshot_id`
- `sidechain_context_id`
- `packet_id`
- `delegated_run_id`
- `created_at`
- `entry_ids`
- `entry_count`
- `summary`
- `snapshot_attrs`

### SidechainReturnEnvelope

Purpose:

- Summary-only return envelope for sidechain work.
- It may reference evidence/recommendations/failure data.
- It must not carry the full child transcript.

Fields:

- `envelope_id`
- `sidechain_context_id`
- `delegated_run_id`
- `packet_id`
- `status`
- `summary`
- `output_payload`
- `evidence_refs`
- `recommendation_refs`
- `failure`
- `contains_full_child_transcript`
- `created_at`
- `envelope_attrs`

Allowed statuses:

- `completed`
- `failed`
- `cancelled`
- `skipped`
- `inconclusive`

Hard invariant:

- `contains_full_child_transcript` must be `False`

The model raises `SidechainReturnEnvelopeError` if this invariant is violated.

## SidechainContextService

Implemented in `src/chanta_core/delegation/sidechain.py`.

Constructor:

- `trace_service: TraceService | None = None`
- `ocel_store: OCELStore | None = None`

The constructor follows the same pattern as `DelegatedProcessRunService`.

### create_sidechain_context_from_packet

Signature:

- `packet: DelegationPacket`
- `delegated_run: DelegatedProcessRun | None = None`
- `child_session_id: str | None = None`
- `child_process_instance_id: str | None = None`
- `context_type: str = "delegation"`
- `isolation_mode: str = "packet_only"`
- `context_attrs: dict[str, Any] | None = None`

Behavior:

- creates a `SidechainContext`
- derives packet/run/session/process IDs from the packet and optional run
- sets `entry_ids=[]`
- builds `safety_ref_ids` from:
  - `permission_request_ids`
  - `session_permission_resolution_ids`
  - `workspace_write_sandbox_decision_ids`
  - `shell_network_pre_sandbox_decision_ids`
  - `process_outcome_evaluation_ids`
- forces `contains_full_parent_transcript=False`
- forces `inherited_permissions=False`
- sets `context_attrs["packet_metadata_only"] = True`
- sets `context_attrs["runtime_effect"] = False`
- records `sidechain_context_created`
- records `sidechain_parent_transcript_excluded`
- records `sidechain_permission_inheritance_prevented`
- returns the context

It must not execute a child runtime.

### add_context_entry

Creates one `SidechainContextEntry` and records:

- `sidechain_context_entry_added`

It relates the entry to the sidechain context through:

- `belongs_to_sidechain_context`

### build_entries_from_packet

Creates packet-derived entries for:

- goal
- context summary when present
- structured inputs when present
- object refs
- allowed capabilities
- expected output schema when present
- termination conditions when present
- permission request IDs
- session permission resolution IDs
- workspace write sandbox decision IDs
- shell/network pre-sandbox decision IDs
- process outcome evaluation IDs

Safety mapping:

- `permission_request_ids` -> `permission_ref`
- `session_permission_resolution_ids` -> `permission_ref`
- `workspace_write_sandbox_decision_ids` -> `sandbox_ref`
- `shell_network_pre_sandbox_decision_ids` -> `risk_ref`
- `process_outcome_evaluation_ids` -> `outcome_ref`

When any safety refs exist, it records:

- `sidechain_safety_refs_attached`

It must not create entries for:

- full parent transcript
- full parent session history
- full child transcript

### mark_context_ready

Returns an updated immutable context with:

- `status="ready"`
- supplied `entry_ids` if provided

Records:

- `sidechain_context_ready`

### seal_context

Returns an updated immutable context with:

- `status="sealed"`

Records:

- `sidechain_context_sealed`

### archive_context

Returns an updated immutable context with:

- `status="archived"`

Records:

- `sidechain_context_archived`

### mark_context_error

This helper was added because the required OCEL activity list includes
`sidechain_context_error`.

Behavior:

- returns an updated immutable context with `status="error"`
- records failure data in `context_attrs["failure"]`
- records `sidechain_context_error`

It is still model-only and does not perform conformance or runtime execution.

### build_snapshot

Creates a `SidechainContextSnapshot` from a context and entry list.

Records:

- `sidechain_context_snapshot_created`

Relations:

- snapshot of sidechain context
- packet object relation where available
- delegated run relation where available

### record_return_envelope

Creates a `SidechainReturnEnvelope`.

Behavior:

- accepts status, summary, output payload, evidence refs, recommendation refs,
  and failure data
- forces `contains_full_child_transcript=False`
- records `sidechain_return_envelope_recorded`
- relates envelope to sidechain context
- relates envelope to delegated run when provided

It must not attach a full child transcript.

## OCEL Object Types

Required object types:

- `sidechain_context`
- `sidechain_context_entry`
- `sidechain_context_snapshot`
- `sidechain_return_envelope`

Object attrs should include each model's `to_dict()` content plus:

- `object_key`
- `display_name`
- `contains_full_parent_transcript=False` for sidechain contexts
- `inherited_permissions=False` for sidechain contexts
- `contains_full_child_transcript=False` for return envelopes

## OCEL Event Activities

Required event activities:

- `sidechain_context_created`
- `sidechain_context_ready`
- `sidechain_context_sealed`
- `sidechain_context_archived`
- `sidechain_context_error`
- `sidechain_context_entry_added`
- `sidechain_context_snapshot_created`
- `sidechain_return_envelope_recorded`
- `sidechain_parent_transcript_excluded`
- `sidechain_permission_inheritance_prevented`
- `sidechain_safety_refs_attached`

Event attrs include:

- `runtime_event_type`
- `source_runtime = "chanta_core"`
- `observability_only = True`
- `sidechain_context_model_only = True`
- `runtime_effect = False`
- `enforcement_enabled = False`

These markers are important. If a sidechain event has active runtime effect or
enforcement enabled, v0.13.1 has crossed its boundary.

## OCEL Relation Intent

Expected event-object relations:

- sidechain context object
- sidechain context entry object
- sidechain context snapshot object
- sidechain return envelope object
- packet object
- delegated run object where available
- parent session where available
- child session where available
- parent process where available
- child process where available

Expected object-object relation intent:

- sidechain context derived from delegation packet
- sidechain context belongs to delegated run
- sidechain context references parent/child session
- sidechain context references parent/child process
- sidechain context entry belongs to sidechain context
- snapshot is snapshot of sidechain context
- return envelope is return of sidechain context
- return envelope is return of delegated run where available

The implementation uses placeholder OCEL objects only for session/process
objects where required by relation shape.

## ContextHistory Adapter

Implemented in `src/chanta_core/delegation/history_adapter.py`.

Required helpers:

- `sidechain_contexts_to_history_entries`
- `sidechain_context_entries_to_history_entries`
- `sidechain_context_snapshots_to_history_entries`
- `sidechain_return_envelopes_to_history_entries`

Expected behavior:

- `source = "sidechain_context"`
- `role = "context"`
- refs include sidechain context ID
- refs include entry/snapshot/envelope IDs where applicable
- refs include packet ID
- refs include delegated run ID where available
- refs include parent/child session IDs where available
- failed envelopes get high priority
- inconclusive envelopes get high/medium priority
- safety ref entries get high/medium priority
- goal/context summary entries get medium priority
- snapshots get low/medium priority

The adapter operates on supplied objects only. It does not query OCEL.

## PIG/OCPX Report Support

Implemented in:

- `src/chanta_core/pig/reports.py`
- `src/chanta_core/pig/inspector.py`

The report exposes `sidechain_summary` with:

- `sidechain_context_count`
- `sidechain_context_entry_count`
- `sidechain_context_snapshot_count`
- `sidechain_return_envelope_count`
- `sidechain_ready_count`
- `sidechain_sealed_count`
- `sidechain_error_count`
- `sidechain_parent_transcript_excluded_count`
- `sidechain_permission_inheritance_prevented_count`
- `sidechain_safety_ref_count`
- `sidechain_context_by_type`
- `sidechain_context_by_isolation_mode`

The human report includes a `Sidechain Context` section.

The inspector includes:

- `pig_summary["sidechain_summary"]`
- `inspection_attrs["sidechain_summary"]`
- one text line for sidechain context count

No delegation conformance scoring belongs to v0.13.1.

## OCPX Loader Correction

While validating full pytest after v0.13.1, one existing test failed:

- `tests/test_process_instance_runtime.py::test_process_instance_runtime_shape`

Root cause:

- v0.13.0 had introduced `_merge_event_rows()` in `OCPXLoader`.
- It sorted merged rows by timestamp and event ID.
- Several runtime events can share the same timestamp.
- Sorting timestamp ties by event ID changed the process view activity order.

Fix:

- `_merge_event_rows()` now preserves source fetch order and removes duplicate
  event IDs.

Reasoning:

- `fetch_events_by_object(..., qualifier="process_context")` already returns
  process events in timestamp order.
- Parent/child relation groups are appended afterward.
- Preserving group order keeps legacy process views stable while still allowing
  sidechain/delegation relation views to merge extra events.

Verification:

- `tests/test_process_instance_runtime.py`
- `tests/test_sidechain_context_ocel_shape.py`
- `tests/test_delegation_ocel_shape.py`
- `tests/test_pig_reports.py`

All passed after the correction.

## Public Imports

`src/chanta_core/delegation/__init__.py` exports:

- `SidechainContext`
- `SidechainContextEntry`
- `SidechainContextSnapshot`
- `SidechainReturnEnvelope`
- `SidechainContextService`
- `sidechain_contexts_to_history_entries`
- `sidechain_context_entries_to_history_entries`
- `sidechain_context_snapshots_to_history_entries`
- `sidechain_return_envelopes_to_history_entries`

`tests/test_imports.py` imports and asserts these symbols.

## Script

`scripts/test_sidechain_context.py` is a smoke script.

It should:

- create a `DelegatedProcessRunService`
- create a `SidechainContextService` using the same trace service
- create a `DelegationPacket`
- create a `DelegatedProcessRun`
- create sidechain context from packet
- build packet-derived entries
- mark context ready
- seal context
- build snapshot
- record summary-only return envelope
- print IDs, status, entry count, and boundary flags

Observed output shape during restore:

- `context_status=sealed`
- `entry_count=12`
- `contains_full_parent_transcript=False`
- `inherited_permissions=False`
- `contains_full_child_transcript=False`

The exact UUIDs vary per run.

## Boundary Tests

`tests/test_sidechain_context_boundaries.py` verifies no active runtime execution
imports or calls exist in `src/chanta_core/delegation/sidechain.py`.

Forbidden active behavior:

- `AgentRuntime` call
- child runtime execution
- subagent execution
- LLM call
- tool execution
- shell execution
- network execution
- file write outside normal OCEL persistence
- permission inheritance
- full parent transcript copy
- full child transcript return
- conformance check
- external connector/MCP/plugin loading

Required boundary data:

- `contains_full_parent_transcript=False`
- `contains_full_child_transcript=False`
- `inherited_permissions=False`
- `sidechain_context_model_only`

Some forbidden concepts appear as required field names or docs/tests. The
implementation must not use them as active behavior.

## Acceptance Tests

First run sidechain tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_sidechain_context_models.py tests\test_sidechain_context_service.py tests\test_sidechain_context_history_adapter.py tests\test_sidechain_context_ocel_shape.py tests\test_sidechain_context_boundaries.py
```

Observed result:

- `9 passed`

Then run imports, PIG, and v0.13.0 regression:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_imports.py tests\test_pig_reports.py tests\test_delegation_models.py tests\test_delegated_process_run_service.py tests\test_delegation_history_adapter.py tests\test_delegation_ocel_shape.py tests\test_delegation_boundaries.py
```

Observed result:

- `25 passed`

Then run the full v0.13.1 acceptance subset from the prompt.

Observed result:

- `186 passed`

Then run full pytest:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

First full run:

- `562 passed`
- `1 failed`
- `1 skipped`
- `3 warnings`

Failure was the OCPX loader ordering issue described above.

After the `_merge_event_rows()` correction:

- `563 passed`
- `1 skipped`
- `3 warnings`

Warnings:

- invalid JSONL row warnings in unrelated edit proposal, process job, and
  process schedule store tests

## Editable Install

Command:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

First attempt failed under sandbox network restrictions while resolving build
dependencies:

- `WinError 10013`
- no setuptools version could be fetched

Approved escalated rerun succeeded:

- installed `chanta-core==0.13.1`
- previous editable install `chanta-core==0.13.0` was uninstalled
- new editable wheel installed successfully

## LLM Script

Command:

```powershell
.\.venv\Scripts\python.exe scripts\test_llm_client.py
```

Observed result during v0.13.1 restore:

- exit code `0`
- no output

This script is not required for sidechain correctness. Sidechain tests do not
depend on LM Studio or any LLM.

## Versioning

For v0.13.1:

- `pyproject.toml` version is `0.13.1`
- `src/chanta_core/__init__.py` has `__version__ = "0.13.1"`

## Git Hygiene

Commands run:

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

The worktree contains many intended untracked/modified v0.12.3, v0.13.0, and
v0.13.1 files. These are implementation files and tests, not generated runtime
artifacts.

## Non-Goals

v0.13.1 intentionally does not implement:

- delegation conformance
- active subagent runtime execution
- AgentRuntime child invocation
- async worker dispatch
- UI
- external connector/MCP/plugin sidechains
- canonical JSONL sidechain store
- full transcript transfer
- permission inheritance
- tool execution
- shell/network execution
- LLM execution

Future work:

- v0.13.2 Delegation Conformance
- later active subagent runtime only after conformance and safety boundaries are
  mature

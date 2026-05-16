# ChantaCore v0.13.0 Restore Notes

Version: v0.13.0
Name: ChantaCore v0.13.0 - Delegated Process Run Foundation

This document is a restore-grade record of the v0.13.0 implementation. It is
intended to let a future session reconstruct the feature from code, tests, and
architecture rules without relying on chat history.

## Restore Goal

v0.13.0 adds the delegated process run foundation. Delegation is represented as
process structure only. A parent run can create a packet, create a delegated run
record, advance lifecycle state, record a result envelope, and record parent/child
links. It must not execute the child.

Canonical persistence remains OCEL:

- delegation state is represented as OCEL objects
- lifecycle is represented as OCEL events
- references and lineage are represented as OCEL relations

JSONL is not canonical delegation persistence.
Markdown is not canonical delegation persistence.

## Files Added Or Modified

Primary package:

- `src/chanta_core/delegation/__init__.py`
- `src/chanta_core/delegation/ids.py`
- `src/chanta_core/delegation/errors.py`
- `src/chanta_core/delegation/models.py`
- `src/chanta_core/delegation/service.py`
- `src/chanta_core/delegation/history_adapter.py`

Compatibility/package files:

- `src/chanta_core/delegation/packet.py`
- `src/chanta_core/delegation/result.py`

Report/read-model integration:

- `src/chanta_core/ocpx/loader.py`
- `src/chanta_core/pig/reports.py`
- `src/chanta_core/pig/inspector.py`

Script:

- `scripts/test_delegated_process_run.py`

Tests:

- `tests/test_delegation_models.py`
- `tests/test_delegated_process_run_service.py`
- `tests/test_delegation_history_adapter.py`
- `tests/test_delegation_ocel_shape.py`
- `tests/test_delegation_boundaries.py`
- `tests/test_imports.py`
- `tests/test_pig_reports.py`

Version/doc:

- `pyproject.toml`
- `src/chanta_core/__init__.py`
- `docs/versions/v0.13/chanta_core_v0_13_0_restore.md`

## ID Helpers

Implemented in `src/chanta_core/delegation/ids.py`.

Required helpers and prefixes:

- `new_delegation_packet_id()` -> `delegation_packet:...`
- `new_delegated_process_run_id()` -> `delegated_process_run:...`
- `new_delegation_result_id()` -> `delegation_result:...`
- `new_delegation_link_id()` -> `delegation_link:...`

The implementation uses `uuid4()` because that matches the local helper style.

## Errors

Implemented in `src/chanta_core/delegation/errors.py`.

Required classes:

- `DelegationError`
- `DelegationPacketError`
- `DelegatedProcessRunError`
- `DelegationResultError`
- `DelegationLinkError`

All model validation errors inherit from `DelegationError`.

## Models

All models are frozen dataclasses in
`src/chanta_core/delegation/models.py` and expose `to_dict()`.

### DelegationPacket

Purpose:

- A bounded, packet-only request description for delegated process work.
- It may contain summaries, structured inputs, object references, and IDs of
  existing safety/permission/outcome records.
- It must not contain the full parent transcript.

Fields:

- `packet_id`
- `packet_name`
- `parent_session_id`
- `parent_turn_id`
- `parent_message_id`
- `parent_process_instance_id`
- `goal`
- `context_summary`
- `structured_inputs`
- `object_refs`
- `allowed_capabilities`
- `expected_output_schema`
- `termination_conditions`
- `permission_request_ids`
- `session_permission_resolution_ids`
- `workspace_write_sandbox_decision_ids`
- `shell_network_pre_sandbox_decision_ids`
- `process_outcome_evaluation_ids`
- `created_at`
- `packet_attrs`

Validation and boundary behavior:

- `goal` is required.
- `packet_attrs["contains_full_parent_transcript"]` is forced to `False` when
  absent or different.

### DelegatedProcessRun

Purpose:

- Represents a delegated process run object.
- It is a model-only process object in v0.13.0.
- It does not call a child runtime.

Fields:

- `delegated_run_id`
- `packet_id`
- `parent_session_id`
- `child_session_id`
- `parent_process_instance_id`
- `child_process_instance_id`
- `delegation_type`
- `isolation_mode`
- `status`
- `requested_at`
- `started_at`
- `completed_at`
- `failed_at`
- `requester_type`
- `requester_id`
- `allowed_capabilities`
- `inherited_permissions`
- `run_attrs`

Allowed `delegation_type` values:

- `subprocess`
- `subagent`
- `verification`
- `analysis`
- `review`
- `manual`
- `other`

Allowed `isolation_mode` values:

- `none`
- `packet_only`
- `sidechain_pending`
- `sidechain`
- `external`
- `other`

Allowed `status` values:

- `created`
- `requested`
- `started`
- `completed`
- `failed`
- `cancelled`
- `skipped`

Important invariant:

- `inherited_permissions` must be `False`.

The model raises `DelegatedProcessRunError` if permission inheritance is true.

### DelegationResult

Purpose:

- Summary/result envelope for a delegated run.
- It records output payload, evidence refs, recommendations, and failure data.
- It is not a full child transcript.

Fields:

- `result_id`
- `delegated_run_id`
- `packet_id`
- `status`
- `output_summary`
- `output_payload`
- `evidence_refs`
- `recommendation_refs`
- `failure`
- `created_at`
- `result_attrs`

Allowed statuses:

- `completed`
- `failed`
- `cancelled`
- `skipped`
- `inconclusive`

### DelegationLink

Purpose:

- Parent/child session and process linkage for delegated work.
- The link is structural, not executable.

Fields:

- `link_id`
- `delegated_run_id`
- `parent_process_instance_id`
- `child_process_instance_id`
- `parent_session_id`
- `child_session_id`
- `relation_type`
- `created_at`
- `link_attrs`

Allowed `relation_type` values:

- `delegated_to`
- `forked_delegation`
- `manual_link`
- `other`

## Service

Implemented in `src/chanta_core/delegation/service.py`.

Service name:

- `DelegatedProcessRunService`

Constructor:

- `trace_service: TraceService | None = None`
- `ocel_store: OCELStore | None = None`

If `trace_service` is not supplied and `ocel_store` is supplied, the service
creates `TraceService(ocel_store=ocel_store)`.

If neither is supplied, it creates a default `TraceService()`.

### Public Methods

Required methods:

- `create_delegation_packet(...)`
- `create_delegated_process_run(...)`
- `request_delegated_process_run(run=..., reason=None)`
- `start_delegated_process_run(run=..., reason=None)`
- `complete_delegated_process_run(run=..., reason=None)`
- `fail_delegated_process_run(run=..., failure=None, reason=None)`
- `cancel_delegated_process_run(run=..., reason=None)`
- `skip_delegated_process_run(run=..., reason=None)`
- `record_delegation_result(...)`
- `record_delegation_link(...)`

Lifecycle methods use `dataclasses.replace()` to return updated immutable model
instances. They do not mutate in place.

### Packet Creation

`create_delegation_packet(...)`:

- creates a `DelegationPacket`
- records `delegation_packet_created`
- forces `contains_full_parent_transcript=False`
- stores permission/sandbox/risk/outcome refs as IDs
- records permission context reference event when permission refs exist
- records safety context reference event when workspace/shell/outcome refs exist
- returns the packet

It must not copy raw parent transcript.

### Delegated Run Creation

`create_delegated_process_run(...)`:

- creates a `DelegatedProcessRun`
- sets `status="created"`
- sets `requested_at=utc_now_iso()`
- sets `inherited_permissions=False`
- records `delegated_process_run_created`
- returns the run

It must not instantiate or call `AgentRuntime`.

### Lifecycle Recording

Lifecycle methods record only OCEL events:

- requested -> `delegated_process_requested`
- started -> `delegated_process_started`
- completed -> `delegated_process_completed`
- failed -> `delegated_process_failed`
- cancelled -> `delegated_process_cancelled`
- skipped -> `delegated_process_skipped`

No lifecycle method dispatches tools, calls an LLM, executes shell/network, or
starts a child worker.

### Result Recording

`record_delegation_result(...)`:

- creates a `DelegationResult`
- records `delegation_result_recorded`
- relates result to delegated run and packet
- returns the result

### Link Recording

`record_delegation_link(...)`:

- creates a `DelegationLink`
- records `delegation_link_recorded`
- relates link to delegated run
- includes parent/child session and process references where available
- returns the link

## OCEL Object Types

Required object types:

- `delegation_packet`
- `delegated_process_run`
- `delegation_result`
- `delegation_link`

Object attrs should include the corresponding `to_dict()` plus:

- `object_key`
- `display_name`
- `contains_full_parent_transcript=False` for packets
- `inherited_permissions=False` for delegated runs

## OCEL Event Activities

Required event activities:

- `delegation_packet_created`
- `delegated_process_run_created`
- `delegated_process_requested`
- `delegated_process_started`
- `delegated_process_completed`
- `delegated_process_failed`
- `delegated_process_cancelled`
- `delegated_process_skipped`
- `delegation_result_recorded`
- `delegation_link_recorded`
- `delegation_permission_context_referenced`
- `delegation_safety_context_referenced`

Event attrs include:

- `runtime_event_type`
- `source_runtime = "chanta_core"`
- `observability_only = True`
- `delegation_model_only = True`
- `runtime_effect = False`
- `enforcement_enabled = False`

These fields are important. If `runtime_effect` or `enforcement_enabled`
becomes true, v0.13.0 has crossed its boundary.

## OCEL Relation Intent

Event-object relations should include, where available:

- packet object
- delegated run object
- result object
- link object
- parent session
- child session
- parent process
- child process
- parent turn
- parent message
- permission request object
- session permission resolution object
- workspace write sandbox decision object
- shell/network pre-sandbox decision object
- process outcome evaluation object

Object-object relation intent:

- delegated run uses packet
- delegation result is result of delegated run
- delegation link links delegated run
- delegated run references parent/child session
- delegated run references parent/child process
- packet references permission requests
- packet references session permission resolutions
- packet references workspace write sandbox decisions
- packet references shell/network decisions
- packet references process outcome evaluations

The current implementation uses best-effort placeholders for known external
objects when relation targets are referenced.

## OCPX Loader Note

`src/chanta_core/ocpx/loader.py` was extended so session/process views can include
delegation-related events via:

- `parent_session`
- `child_session`
- `parent_process`
- `child_process`

The helper `_merge_event_rows()` merges event rows from several relation queries
and removes duplicates. During v0.13.1 restore, this helper was corrected to
preserve each source query's order rather than sorting ties by event ID, because
same-timestamp sorting disturbed legacy process runtime view sequence tests.

## ContextHistory Adapter

Implemented in `src/chanta_core/delegation/history_adapter.py`.

Required helpers:

- `delegation_packets_to_history_entries`
- `delegated_process_runs_to_history_entries`
- `delegation_results_to_history_entries`

Expected behavior:

- `source = "delegation"`
- `role = "context"`
- refs include packet/run/result IDs
- packet refs include parent session/process and permission/sandbox/risk/outcome refs
- run refs include parent/child session and process IDs
- failed results have high priority
- inconclusive results have high/medium priority
- requested/started/completed runs have medium priority
- created runs have low priority

The adapter operates on supplied objects only. It does not query OCEL.

## PIG/OCPX Report Support

Implemented in `src/chanta_core/pig/reports.py` and
`src/chanta_core/pig/inspector.py`.

The report exposes `delegation_summary` with:

- `delegation_packet_count`
- `delegated_process_run_count`
- `delegation_result_count`
- `delegation_link_count`
- `delegated_process_created_count`
- `delegated_process_requested_count`
- `delegated_process_started_count`
- `delegated_process_completed_count`
- `delegated_process_failed_count`
- `delegated_process_cancelled_count`
- `delegated_process_skipped_count`
- `delegation_packet_created_count`
- `delegation_result_recorded_count`
- `delegation_link_recorded_count`
- `delegation_by_type`
- `delegation_by_isolation_mode`
- `delegation_permission_reference_count`
- `delegation_safety_reference_count`

The human report includes a `Delegated Process Runs` section.

No delegation conformance scoring belongs to v0.13.0.

## Public Imports

`src/chanta_core/delegation/__init__.py` exports:

- `DelegationPacket`
- `DelegatedProcessRun`
- `DelegationResult`
- `DelegationLink`
- `DelegatedProcessRunService`
- `delegation_packets_to_history_entries`
- `delegated_process_runs_to_history_entries`
- `delegation_results_to_history_entries`

`tests/test_imports.py` should import and assert these symbols.

## Script

`scripts/test_delegated_process_run.py` is a smoke script.

It should:

- create a `DelegatedProcessRunService`
- create a packet with goal, summary, structured inputs, capabilities, and dummy refs
- create a delegated run
- mark requested
- mark started
- record result
- mark completed
- record link
- print IDs and statuses

It must not require LM Studio.
It must not call `AgentRuntime`.
It must not execute a subagent.

## Boundary Tests

`tests/test_delegation_boundaries.py` verifies the package remains model-only.

Forbidden active behavior:

- `AgentRuntime` call
- child runtime execution
- subagent execution
- LLM call
- tool execution
- shell/network execution
- file write outside normal OCEL persistence
- permission inheritance
- full parent transcript copy
- sidechain context implementation
- conformance check
- external connector/MCP/plugin loading

Some forbidden words may appear in tests/docs as strings. They must not appear
as active implementation behavior.

## Acceptance Tests

Targeted v0.13.0 tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_imports.py tests\test_delegation_models.py tests\test_delegated_process_run_service.py tests\test_delegation_history_adapter.py tests\test_delegation_ocel_shape.py tests\test_delegation_boundaries.py tests\test_pig_reports.py
```

During the v0.13.0 work, the broad acceptance subset passed:

- `176 passed`

During the later v0.13.1 restore pass, the combined acceptance subset passed:

- `186 passed`

The full local suite after v0.13.1 passed:

- `563 passed`
- `1 skipped`
- `3 warnings`

The warnings were unrelated invalid JSONL-row warnings in store tests.

## Versioning

For v0.13.0 itself:

- `pyproject.toml` version should be `0.13.0`
- `src/chanta_core/__init__.py` should expose `__version__ = "0.13.0"`

Note: after v0.13.1, those files correctly move to `0.13.1`.

## Git Hygiene

Generated runtime files must remain ignored:

- `data/`
- `.pytest-tmp/`
- `.venv/`
- `*.sqlite`
- `*.sqlite3`
- `.env`
- `.env.*` except `.env.example`
- `__pycache__/`
- `*.pyc`
- `src/chanta_core.egg-info/`

Observed during v0.13.1 restore pass:

- `data/` ignored
- `.pytest-tmp/` ignored
- tracked `.sqlite` match was only `tests/test_ocel_export_sqlite.py`
- tracked `.env` match was only `.env.example`

## Non-Goals

v0.13.0 intentionally does not implement:

- sidechain context
- delegation conformance
- active subagent runtime execution
- async worker dispatch
- UI
- external connector/MCP/plugin delegation
- permission inheritance
- transcript copying
- active safety enforcement

Future work:

- v0.13.1 Sidechain Context
- v0.13.2 Delegation Conformance

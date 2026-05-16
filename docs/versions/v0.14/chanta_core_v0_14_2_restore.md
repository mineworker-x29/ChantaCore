# ChantaCore v0.14.2 Restore Notes

## Version

ChantaCore v0.14.2 adds the External Adapter Review Queue.

This version creates OCEL-native review queue records for external assimilation candidates. It allows candidates to be queued for review, checked against a default safety checklist, annotated with findings, and given non-activating review decisions.

v0.14.2 does not activate external capabilities. A decision such as `approved_for_design` is a design-review record only.

## Architectural Boundary

Canonical persistence remains OCEL-based.

External adapter review queue state is represented by OCEL event, object, and relation records. Markdown views remain non-canonical materialized views. JSONL is not introduced as canonical persistence for review queue state.

Review decisions are records, not runtime commands. They do not mutate candidates, grant permissions, create sandbox decisions, register runtime tools, or enable execution.

## Package Extension

The implementation extends `src/chanta_core/external/`.

New file:

- `review.py`

Updated files:

- `__init__.py`
- `ids.py`
- `errors.py`
- `history_adapter.py`

Reporting support is extended in:

- `src/chanta_core/pig/reports.py`
- `src/chanta_core/pig/inspector.py`

## New Models

`ExternalAdapterReviewQueue` represents an OCEL-backed review queue.

Key fields:

- `queue_id`
- `queue_name`
- `queue_type`
- `status`
- `created_at`
- `updated_at`
- `item_ids`
- `queue_attrs`

`ExternalAdapterReviewItem` represents a candidate review item in a queue.

Key fields:

- `item_id`
- `queue_id`
- `candidate_id`
- `descriptor_id`
- `source_id`
- `risk_note_ids`
- `priority`
- `review_status`
- `assigned_reviewer`
- `created_at`
- `updated_at`
- `item_attrs`

`approved_for_design` on a review item is not activation.

`ExternalAdapterReviewChecklist` represents checklist state for a review item.

Key fields:

- `checklist_id`
- `item_id`
- `checklist_type`
- `required_checks`
- `completed_checks`
- `failed_checks`
- `status`
- `created_at`
- `updated_at`
- `checklist_attrs`

`ExternalAdapterReviewFinding` records review findings.

Key fields:

- `finding_id`
- `item_id`
- `finding_type`
- `status`
- `severity`
- `message`
- `source_kind`
- `source_ref`
- `created_at`
- `finding_attrs`

`ExternalAdapterReviewDecision` records the review decision.

Key fields:

- `decision_id`
- `item_id`
- `queue_id`
- `candidate_id`
- `decision`
- `decided_by`
- `decision_reason`
- `finding_ids`
- `checklist_id`
- `activation_allowed`
- `runtime_registration_allowed`
- `execution_enabled_after_decision`
- `created_at`
- `decision_attrs`

In v0.14.2, the decision flags must remain:

- `activation_allowed=False`
- `runtime_registration_allowed=False`
- `execution_enabled_after_decision=False`

## OCEL Objects

v0.14.2 introduces these OCEL object types:

- `external_adapter_review_queue`
- `external_adapter_review_item`
- `external_adapter_review_checklist`
- `external_adapter_review_finding`
- `external_adapter_review_decision`

Review items reference external assimilation candidates and external capability descriptors by ID. They do not modify those candidate or descriptor objects.

Review decisions reference the reviewed item and candidate. They explicitly record non-activation fields so downstream inspection can detect that no runtime enablement was allowed.

## OCEL Events

The review service records these event activities:

- `external_adapter_review_queue_created`
- `external_adapter_review_item_created`
- `external_adapter_review_item_assigned`
- `external_adapter_review_item_status_updated`
- `external_adapter_review_checklist_created`
- `external_adapter_review_checklist_updated`
- `external_adapter_review_finding_recorded`
- `external_adapter_review_finding_resolved`
- `external_adapter_review_decision_recorded`
- `external_adapter_review_decision_marked_non_activating`

The requested activities below are reserved by the design boundary and may be added by future queue lifecycle operations:

- `external_adapter_review_queue_updated`
- `external_adapter_review_queue_closed`

Object relation intent:

- review item belongs to queue
- review item reviews candidate
- review item reviews descriptor
- review item references risk note
- checklist belongs to review item
- finding belongs to review item
- finding may derive from risk note
- decision decides review item
- decision references candidate
- decision may use checklist
- decision may be based on findings

## Service Behavior

`ExternalAdapterReviewService` supports:

- `create_review_queue`
- `create_review_item`
- `assign_review_item`
- `update_review_item_status`
- `build_default_checklist_for_candidate`
- `update_checklist`
- `record_finding`
- `resolve_finding`
- `record_decision`

The service creates immutable updated representations for assignment, status update, checklist update, and finding resolution. It does not mutate the candidate as a side effect.

`create_review_item` creates a pending review item from an `ExternalAssimilationCandidate`. If a candidate appears execution-enabled, the service can record warning attributes on the review item, but it does not enable or disable the candidate.

`record_decision` records a non-activating decision and records `external_adapter_review_decision_marked_non_activating`.

## Default Checklist

The default checklist includes:

- `descriptor_has_name`
- `descriptor_has_type`
- `candidate_disabled`
- `execution_disabled`
- `review_status_pending`
- `risk_notes_reviewed`
- `permissions_declared_or_empty`
- `no_runtime_activation`

Checklist evaluation is deterministic.

A disabled candidate completes `candidate_disabled` and `execution_disabled`.

An execution-enabled fixture fails `execution_disabled`, but the service does not mutate the candidate.

Missing descriptor name or type fails the descriptor checks.

`no_runtime_activation` is completed because this service records review state only.

## Explicit Non-Goals

v0.14.2 does not do the following:

- no external capability activation
- no setting `candidate.execution_enabled=True`
- no setting `candidate.activation_status=active`
- no candidate mutation as a side effect of review decisions
- no external tool execution
- no external skill execution
- no plugin dynamic loading
- no MCP connection
- no network calls
- no URL fetch
- no git clone
- no pip or npm install
- no external code import
- no `ToolDispatcher` mutation
- no `SkillExecutor` mutation
- no `AgentRuntime` active capability integration
- no permission auto-grant
- no sandbox decision auto-creation
- no LLM classifier
- no LLM reviewer
- no Markdown-to-review import
- no canonical JSONL review queue store
- no async worker
- no UI

## Context History

`src/chanta_core/external/history_adapter.py` provides these review adapters:

- `external_adapter_review_items_to_history_entries`
- `external_adapter_review_findings_to_history_entries`
- `external_adapter_review_decisions_to_history_entries`

The adapter source is `external_adapter_review`.

Refs include queue IDs, item IDs, candidate IDs, descriptor IDs, risk note IDs, finding IDs, decision IDs, and checklist IDs where available.

Priority behavior:

- high or critical findings receive high priority
- `needs_more_info` decisions receive high or medium-high priority
- rejected decisions receive elevated priority
- `approved_for_design` decisions receive medium priority
- pending review items receive medium priority

The adapter does not retrieve from OCEL automatically. It only adapts supplied objects.

## PIG/OCPX Report Support

PIG report attrs include review queue fields under `external_capability_summary`.

The summary includes:

- `external_adapter_review_queue_count`
- `external_adapter_review_item_count`
- `external_adapter_review_checklist_count`
- `external_adapter_review_finding_count`
- `external_adapter_review_decision_count`
- `external_review_pending_count`
- `external_review_in_review_count`
- `external_review_needs_more_info_count`
- `external_review_approved_for_design_count`
- `external_review_rejected_count`
- `external_review_open_finding_count`
- `external_review_high_risk_finding_count`
- `external_review_critical_risk_finding_count`
- `external_review_non_activating_decision_count`
- `external_review_runtime_activation_count`

For v0.14.2, `external_review_runtime_activation_count` should normally be `0`.

The PI substrate inspector also surfaces review item count and runtime activation count in its external capability summary.

## Tests

v0.14.2 adds:

- `tests/test_external_adapter_review_models.py`
- `tests/test_external_adapter_review_service.py`
- `tests/test_external_adapter_review_checklist.py`
- `tests/test_external_adapter_review_history_adapter.py`
- `tests/test_external_adapter_review_ocel_shape.py`
- `tests/test_external_adapter_review_boundaries.py`

Existing tests updated:

- `tests/test_imports.py`
- `tests/test_pig_reports.py`

The optional script is:

- `scripts/test_external_adapter_review_queue.py`

## Restore Procedure

1. Confirm version metadata:
   - `pyproject.toml` version is `0.14.2`.
   - `src/chanta_core/__init__.py` `__version__` is `0.14.2`.
2. Confirm `src/chanta_core/external/review.py` exists.
3. Confirm review exports from `chanta_core.external`:
   - `ExternalAdapterReviewQueue`
   - `ExternalAdapterReviewItem`
   - `ExternalAdapterReviewChecklist`
   - `ExternalAdapterReviewFinding`
   - `ExternalAdapterReviewDecision`
   - `ExternalAdapterReviewService`
4. Run external adapter review tests:
   - `tests/test_external_adapter_review_models.py`
   - `tests/test_external_adapter_review_service.py`
   - `tests/test_external_adapter_review_checklist.py`
   - `tests/test_external_adapter_review_history_adapter.py`
   - `tests/test_external_adapter_review_ocel_shape.py`
   - `tests/test_external_adapter_review_boundaries.py`
5. Run `tests/test_imports.py` and `tests/test_pig_reports.py`.
6. Run `scripts/test_external_adapter_review_queue.py`.
7. Confirm review decisions leave:
   - `activation_allowed=False`
   - `runtime_registration_allowed=False`
   - `execution_enabled_after_decision=False`
8. Confirm candidates remain disabled and are not mutated by review decisions.
9. Confirm no Markdown review import exists.
10. Confirm no generated runtime files are tracked.

## Validation Snapshot

During implementation validation, the acceptance test subset passed and full pytest passed:

- acceptance subset: `239 passed`
- full pytest: `616 passed, 1 skipped`
- review script: passed

These counts may change as later versions add tests.

## Future Work

- v0.14.3 MCP / Plugin Descriptor Skeleton
- v0.14.4 External OCEL Import Candidate
- Later activation only after an explicit safety and conformance layer

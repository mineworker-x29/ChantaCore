# ChantaCore v0.18.3 Restore Document

Version name: ChantaCore v0.18.3 - Controlled Result Promotion Candidate

## Purpose

v0.18.3 adds a review-only workflow for turning execution envelope results into promotion candidates.

Promotion candidates are not canonical memory, persona, overlay, context, or workspace summary records. They are pending review records that preserve preview, hash, and reference information from execution outputs.

## Scope

Implemented public concepts:

- Execution Result Promotion Policy
- Execution Result Promotion Candidate
- Execution Result Promotion Review Request
- Execution Result Promotion Decision
- Execution Result Promotion Finding
- Execution Result Promotion Result
- Controlled Promotion Workflow
- CLI promotion surface
- OCEL object/event/relation support
- ContextHistory adapter support
- PIG/OCPX lightweight report counts

## Candidate Rules

Candidate creation:

- is review-only;
- does not write memory;
- does not update persona;
- does not update personal overlay;
- uses preview, hash, and reference fields;
- does not copy full raw output bodies;
- starts as `pending_review`;
- sets `canonical_promotion_enabled=false`;
- sets `promoted=false`.

The default policy allows review candidates for context history, memory, personal overlay, persona source, workspace summary, manual note, process pattern, and other generic target kinds.

Denied target kinds include canonical memory, canonical persona, direct overlay write, and direct file write.

## Review

Supported review decisions:

- `approved_for_later_promotion`
- `rejected`
- `no_action`
- `needs_more_info`
- `archive`
- `error`

`approved_for_later_promotion` is not immediate promotion. It records only that a later controlled workflow may consider the candidate.

`no_action` is valid and records that no promotion action should be taken.

## CLI

```powershell
chanta-cli promotion candidate-from-envelope <envelope_id> --target memory_candidate
chanta-cli promotion candidate-from-envelope --envelope-json-file envelope.json --target memory_candidate
chanta-cli promotion list
chanta-cli promotion show <candidate_id>
chanta-cli promotion review <candidate_id> --decision no_action
```

The CLI emits summaries only. It does not perform canonical promotion.

## Future Work

- workspace read summarization pipeline;
- workbench pending review UI;
- actual controlled promotion in a later version, if ever enabled.

## Restore-Grade Policy Addendum

### Implemented Files

Primary implementation:

- `src/chanta_core/execution/promotion.py`
- `src/chanta_core/execution/history_adapter.py`
- `src/chanta_core/execution/__init__.py`
- `src/chanta_core/cli/main.py`
- `src/chanta_core/pig/reports.py`

Tests:

- `tests/test_execution_result_promotion_models.py`
- `tests/test_execution_result_promotion_service.py`
- `tests/test_execution_result_promotion_cli.py`
- `tests/test_execution_result_promotion_history_adapter.py`
- `tests/test_execution_result_promotion_ocel_shape.py`
- `tests/test_execution_result_promotion_boundaries.py`

### Public API / Model Surface

Models:

- `ExecutionResultPromotionPolicy`
- `ExecutionResultPromotionCandidate`
- `ExecutionResultPromotionReviewRequest`
- `ExecutionResultPromotionDecision`
- `ExecutionResultPromotionFinding`
- `ExecutionResultPromotionResult`

Service:

- `ExecutionResultPromotionService`

Key service methods:

- `create_default_policy`
- `create_candidate_from_envelope`
- `create_review_request`
- `record_decision`
- `record_finding`
- `record_result`
- `review_candidate`
- `list_candidates`
- `show_candidate`
- `render_candidate_summary`

### Persistence and Canonical State

Promotion candidates are review records only. They are not canonical memory,
persona, overlay, profile, source, or workspace summary records.

Required invariants:

```text
canonical_promotion_enabled=False
promoted=False
```

Candidate previews are bounded and hashed. Full raw execution output bodies are
not copied into candidates by default.

### OCEL Shape

Object types:

- `execution_result_promotion_policy`
- `execution_result_promotion_candidate`
- `execution_result_promotion_review_request`
- `execution_result_promotion_decision`
- `execution_result_promotion_finding`
- `execution_result_promotion_result`

Events:

- `execution_result_promotion_policy_registered`
- `execution_result_promotion_candidate_created`
- `execution_result_promotion_review_requested`
- `execution_result_promotion_decision_recorded`
- `execution_result_promotion_finding_recorded`
- `execution_result_promotion_result_recorded`

Expected relations:

- candidate derives from execution envelope/output snapshot/outcome summary when supplied;
- review request targets candidate;
- decision belongs to review request and candidate;
- result summarizes candidate review;
- findings belong to candidate or review request.

### CLI Surface

```powershell
chanta-cli promotion candidate-from-envelope <envelope_id> --target memory_candidate
chanta-cli promotion candidate-from-envelope --envelope-json-file envelope.json --target memory_candidate
chanta-cli promotion list
chanta-cli promotion show <candidate_id>
chanta-cli promotion review <candidate_id> --decision no_action
```

The CLI does not perform canonical promotion. `approved_for_later_promotion`
means a later controlled workflow may consider the candidate; it is not an
immediate write.

### Restore Procedure

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pytest tests\test_execution_result_promotion_models.py tests\test_execution_result_promotion_service.py tests\test_execution_result_promotion_cli.py tests\test_execution_result_promotion_history_adapter.py tests\test_execution_result_promotion_ocel_shape.py tests\test_execution_result_promotion_boundaries.py
.\.venv\Scripts\python.exe -m pytest
```

### Restore Checklist

- [ ] Candidate creation from an envelope records preview/hash/ref only.
- [ ] Direct canonical memory/persona/overlay/file-write targets are denied.
- [ ] `no_action` is a valid review decision.
- [ ] `approved_for_later_promotion` does not promote immediately.
- [ ] CLI list/show/review paths are controlled and summary-oriented.
- [ ] OCEL promotion objects/events/relations are recorded.
- [ ] ContextHistory adapter entries are generated.
- [ ] Boundary tests confirm no memory, persona, overlay, workspace, shell, network, MCP, or plugin mutation.

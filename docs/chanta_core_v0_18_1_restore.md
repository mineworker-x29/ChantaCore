# ChantaCore v0.18.1 Restore Document

Version name: ChantaCore v0.18.1 - Reviewed Proposal-to-Execution Bridge, Read-only First

## Purpose

v0.18.1 adds a generic Reviewed Proposal-to-Execution Bridge. It connects approved skill proposal review decisions to explicit invocation through the read-only execution gate, then optionally records an execution envelope.

This bridge is read-only first. It does not accept natural language, does not execute unreviewed proposals, does not bypass explicit invocation, and does not bypass the execution gate.

## Scope

Implemented public concepts:

- Reviewed Execution Bridge Request
- Reviewed Execution Bridge Decision
- Reviewed Execution Bridge Result
- Reviewed Execution Bridge Violation
- Reviewed Execution Bridge Service
- CLI bridge surface for JSON input
- OCEL object/event/relation support
- ContextHistory adapter support
- PIG/OCPX lightweight report counts

## Supported Bridge Targets

The bridge supports only the read-only workspace skill family:

- `skill:list_workspace_files`
- `skill:read_workspace_text_file`
- `skill:summarize_workspace_markdown`

Unsupported categories:

- `write`
- `shell`
- `network`
- `mcp`
- `plugin`
- `external_capability`
- arbitrary dynamic skill

## Bridge Rules

Only `approved_for_explicit_invocation` review decisions can bridge.

The bridge is denied when:

- review decision is rejected;
- review decision is no-action;
- review decision needs more input;
- review result is not a bridge candidate;
- the proposal still has missing inputs;
- the proposal skill is unsupported or in a denied category.

Gate denial blocks execution and returns `executed=false`, `blocked=true`.

Gate allow runs explicit invocation through `SkillExecutionGateService`, which uses `ExplicitSkillInvocationService` only after the gate allows execution.

## Execution Envelope

If an `ExecutionEnvelopeService` is supplied, the bridge wraps the gated invocation result and records:

- proposal id;
- review decision id;
- review result id where available;
- explicit invocation refs;
- gate refs;
- execution envelope id.

The envelope is observational and provenance-oriented. It does not grant capabilities and does not execute skills by itself.

## CLI

Proposal/review persistence is not yet available. The testable CLI forms are:

```powershell
chanta-cli skill bridge --bridge-json-file bridge.json
```

or:

```powershell
chanta-cli skill bridge --proposal-json-file proposal.json --review-json-file review.json
```

The CLI does not accept raw natural-language execution requests. If only an id is supplied, it returns a controlled diagnostic explaining that persistence is not available.

## OCEL Shape

Object types:

- `reviewed_execution_bridge_request`
- `reviewed_execution_bridge_decision`
- `reviewed_execution_bridge_result`
- `reviewed_execution_bridge_violation`

Events:

- `reviewed_execution_bridge_requested`
- `reviewed_execution_bridge_decision_recorded`
- `reviewed_execution_bridge_allowed`
- `reviewed_execution_bridge_denied`
- `reviewed_execution_bridge_invocation_requested`
- `reviewed_execution_bridge_gate_completed`
- `reviewed_execution_bridge_executed`
- `reviewed_execution_bridge_blocked`
- `reviewed_execution_bridge_result_recorded`
- `reviewed_execution_bridge_violation_recorded`

Relations include bridge request to proposal/review, bridge decision to request, bridge result to request, bridge result to explicit invocation result, bridge result to gate result, bridge result to execution envelope, and bridge violation to request.

## PIG/OCPX Report Keys

Added skill usage summary keys:

- `reviewed_execution_bridge_request_count`
- `reviewed_execution_bridge_decision_count`
- `reviewed_execution_bridge_result_count`
- `reviewed_execution_bridge_violation_count`
- `reviewed_execution_bridge_allowed_count`
- `reviewed_execution_bridge_denied_count`
- `reviewed_execution_bridge_executed_count`
- `reviewed_execution_bridge_blocked_count`
- `reviewed_execution_bridge_needs_more_input_count`
- `reviewed_execution_bridge_unsupported_count`
- `reviewed_execution_bridge_by_skill_id`
- `reviewed_execution_bridge_violation_by_type`

## Boundary Guarantees

- No unreviewed proposal execution.
- No rejected proposal execution.
- No no-action proposal execution.
- No needs-more-input proposal execution.
- No write, shell, network, MCP, plugin, or external capability bridge.
- No permission grants are created.
- No natural-language automatic execution is introduced.
- No `ToolDispatcher` mutation is introduced.
- No `SkillExecutor` mutation is introduced.
- No LLM classifier is called.
- No JSONL canonical bridge store is created.
- No private content is included.

## Restore Procedure

1. Install the package in editable mode:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

2. Run targeted tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_reviewed_execution_bridge_models.py tests\test_reviewed_execution_bridge_service.py tests\test_reviewed_execution_bridge_cli.py tests\test_reviewed_execution_bridge_history_adapter.py tests\test_reviewed_execution_bridge_ocel_shape.py tests\test_reviewed_execution_bridge_boundaries.py tests\test_reviewed_execution_bridge_workspace_read.py
```

3. Run the full suite:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Known Limitations

- No write, shell, network, MCP, plugin, or external capability bridge.
- No natural-language automatic execution.
- No approval UI beyond CLI/service.
- No proposal/review persistence lookup yet; file-based JSON input is the current CLI path.

## Checklist

- [x] ReviewedExecutionBridge models added.
- [x] ReviewedExecutionBridgeService added.
- [x] Approved complete read-only proposals can bridge.
- [x] Rejected/no-action/needs-more-input proposals do not bridge.
- [x] Missing inputs block execution.
- [x] Unsupported skill categories are denied.
- [x] SkillExecutionGateService is used.
- [x] ExplicitSkillInvocationService is reached only through the gate.
- [x] Gate denial blocks execution.
- [x] Gate allow executes explicit invocation.
- [x] Execution envelope support added.
- [x] Proposal/review/gate/invocation/envelope refs are preserved.
- [x] OCEL support added.
- [x] ContextHistory adapter support added.
- [x] PIG/OCPX counts added.
- [x] CLI bridge surface added.

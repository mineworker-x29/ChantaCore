# ChantaCore v0.17.4 Restore Document

Version name: ChantaCore v0.17.4 - Permission-aware Execution Gate, Read-only First

## Purpose

v0.17.4 adds a generic Skill Execution Gate for explicit read-only skill invocations. The gate evaluates an explicit `skill_id` and structured input before execution. It is not natural-language execution and does not infer a skill from arbitrary user text.

The initial supported allowlist is the read-only workspace skill family:

- `skill:list_workspace_files`
- `skill:read_workspace_text_file`
- `skill:summarize_workspace_markdown`

Unsupported, write, shell, network, MCP, plugin, and external capability skills are blocked by the gate. Permission and session permission denial metadata blocks execution when provided.

## Implemented Files

- `src/chanta_core/skills/execution_gate.py`
- `src/chanta_core/skills/ids.py`
- `src/chanta_core/skills/errors.py`
- `src/chanta_core/skills/history_adapter.py`
- `src/chanta_core/skills/__init__.py`
- `src/chanta_core/cli/main.py`
- `src/chanta_core/pig/reports.py`
- `tests/test_skill_execution_gate_models.py`
- `tests/test_skill_execution_gate_service.py`
- `tests/test_skill_execution_gate_workspace_read.py`
- `tests/test_skill_execution_gate_cli.py`
- `tests/test_skill_execution_gate_history_adapter.py`
- `tests/test_skill_execution_gate_ocel_shape.py`
- `tests/test_skill_execution_gate_boundaries.py`
- `tests/test_imports.py`
- `pyproject.toml`
- `src/chanta_core/__init__.py`

## Public API / Model Surface

New models:

- `ReadOnlyExecutionGatePolicy`
- `SkillExecutionGateRequest`
- `SkillExecutionGateDecision`
- `SkillExecutionGateFinding`
- `SkillExecutionGateResult`

New service:

- `SkillExecutionGateService`

New ID helpers:

- `new_read_only_execution_gate_policy_id`
- `new_skill_execution_gate_request_id`
- `new_skill_execution_gate_decision_id`
- `new_skill_execution_gate_finding_id`
- `new_skill_execution_gate_result_id`

## Service Behavior

`SkillExecutionGateService.evaluate_gate` enforces a narrow read-only policy:

- explicit skill identifier required
- only read-only workspace skills can be allowed
- unsupported skills are blocked
- write/shell/network/MCP/plugin/external capability categories are blocked
- permission denial metadata blocks execution
- session permission denial metadata blocks execution
- capability unavailable metadata can block execution when policy requires it
- permission context absence is recorded as a warning by default

Default policy:

- `requires_permission_for_read_only=False`
- `allow_without_permission_for_read_only=True`
- `require_capability_available=False`
- `enforce_workspace_boundary=True`

When the gate allows execution, `gate_explicit_invocation` calls `ExplicitSkillInvocationService.invoke_explicit_skill`. When the gate denies, marks unsupported, or needs review, it does not call explicit invocation.

The gate does not create permission grants. Workspace read containment remains enforced by `WorkspaceReadService` through the explicit invocation path.

## CLI Surface

The CLI includes:

```powershell
chanta-cli skill gate-run skill:read_workspace_text_file --root <WORKSPACE_ROOT> --path docs/example.md
```

The command requires an explicit skill identifier. It prints a gate summary. If the gate allows execution, it invokes the explicit read-only skill path. If the gate blocks execution, it returns a controlled diagnostic without running the skill.

## OCEL Shape

Object types:

- `read_only_execution_gate_policy`
- `skill_execution_gate_request`
- `skill_execution_gate_decision`
- `skill_execution_gate_finding`
- `skill_execution_gate_result`

Events:

- `read_only_execution_gate_policy_registered`
- `skill_execution_gate_requested`
- `skill_execution_gate_finding_recorded`
- `skill_execution_gate_decision_recorded`
- `skill_execution_gate_allowed`
- `skill_execution_gate_denied`
- `skill_execution_gate_needs_review`
- `skill_execution_gate_result_recorded`

Relations:

- decision decides gate request
- finding belongs to gate request
- result belongs to gate request
- result uses gate decision
- result references explicit invocation result if executed
- request references capability, permission, session permission, sandbox, and risk identifiers when provided

## Context History

New adapters use `source="skill_execution_gate"`:

- `skill_execution_gate_decisions_to_history_entries`
- `skill_execution_gate_results_to_history_entries`
- `skill_execution_gate_findings_to_history_entries`

Denied, unsupported, and failed findings receive high priority. Allowed read-only decisions receive medium priority.

## PIG / OCPX Report Support

The PIG skill usage summary includes:

- `skill_execution_gate_request_count`
- `skill_execution_gate_decision_count`
- `skill_execution_gate_finding_count`
- `skill_execution_gate_result_count`
- `skill_execution_gate_allowed_count`
- `skill_execution_gate_denied_count`
- `skill_execution_gate_needs_review_count`
- `skill_execution_gate_unsupported_count`
- `skill_execution_gate_executed_count`
- `skill_execution_gate_blocked_count`
- `skill_execution_gate_by_skill_id`
- `skill_execution_gate_finding_by_type`

## Restore Procedure

1. Install the package in editable mode:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

2. Run targeted tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_skill_execution_gate_models.py tests\test_skill_execution_gate_service.py tests\test_skill_execution_gate_workspace_read.py tests\test_skill_execution_gate_cli.py tests\test_skill_execution_gate_history_adapter.py tests\test_skill_execution_gate_ocel_shape.py tests\test_skill_execution_gate_boundaries.py
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

- default policy contains read-only workspace skill allowlist
- read-only workspace skill allowed by default
- permission context absence records warning
- policy requiring permission blocks or needs review without permission
- permission denial blocks execution
- session permission denial blocks execution
- unsupported skill denied
- write/shell/network/MCP/plugin skill denied
- gate-run calls explicit invocation only after allow
- denied gate does not call explicit invocation
- workspace read boundaries remain with the workspace read service
- no natural-language execution
- no LLM/shell/network/MCP/plugin/write execution
- no permission grant creation
- OCEL objects/events/relations
- ContextHistory adapters
- PIG/OCPX lightweight counts

## Known Limitations

- No general tool gate yet.
- No write/shell/network execution gate.
- No autonomous routing.
- No full execution provenance envelope yet.

## Future Work

- v0.17.5: execution provenance envelope.
- Later: broader permission-aware gates.
- Later: reviewed proposal-to-execution flow.

## Checklist

- [x] Execution gate applies only to explicit skill invocation.
- [x] Default allowlist is read-only workspace skill family.
- [x] Unsupported skills are denied.
- [x] Write/shell/network/MCP/plugin skills are denied.
- [x] Permission denial blocks execution.
- [x] Session permission denial blocks execution.
- [x] Permission absence warning or needs-review behavior follows policy.
- [x] Denied gate does not execute explicit invocation.
- [x] Allowed gate calls explicit invocation.
- [x] Workspace read boundaries are preserved.
- [x] CLI `gate-run` is present.
- [x] OCEL shape added.
- [x] ContextHistory adapter added.
- [x] PIG/OCPX lightweight report support added.
- [x] No permission grant creation is added.
- [x] No LLM/shell/network/MCP/plugin/write execution is added.
